import asyncio
import json
import html as html3
import random
import os
import re
import sys

import aiofiles
import aiohttp
import lxml.html
from bs4 import BeautifulSoup, UnicodeDammit

from proxysession import ProxySession


CACHE_DIR = '/tmp/titles-parser/'

os.makedirs(CACHE_DIR, exist_ok=True)


def parse_metadata(domain, url, content, how='regex'):
    try:
        html = content.decode('utf-8')
    except UnicodeDecodeError:
        dammit = UnicodeDammit(content)
        html = dammit.unicode_markup

    if how == 'regex':
        title = re.findall(r'<title>\s*([^<]+?)\s*</title>', html, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
        if title:
            title = html3.unescape(title[0])
        
        keywords = re.findall(r'''<meta.*? name=\bkeywords\b.*? content=([^'"><]+)\b.*?/?>''', html, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
        if not keywords:
            keywords = re.findall(r'''<meta.*? content=\b([^'"><]+)\b.*?name=\bkeywords\b.*?/?>''', html, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        if keywords:
            keywords = html3.unescape(keywords[0])
        else:
            keywords = None

    elif how == 'lxml':

        try:
            tree = lxml.html.fromstring(html)
        except Exception as e:
            return {"domain": domain, "url": url, "title": None, "keywords": None, "error": str(e)}

        title = tree.find('.//title')
        if title is not None:
            title = title.text_content().strip()
        
        keywords = tree.find('.//meta[@name="keywords"]')
        if keywords is not None:
            try:
                keywords = keywords.attrib['content'].strip()
            except:
                print(url, 'meta keywords has no content attribute')
                keywords = None

    return {
        'domain': domain,
        'url': url,
        'title': title,
        'keywords': keywords,
    }


async def get_metadata_from_url(session, domain, how='regex'):
    url = domain

    cache_filepath = f'{CACHE_DIR}/{domain}.html'

    if not url.startswith('http'):
        url = f'http://{url}'

    try:
        try:
            async with aiofiles.open(cache_filepath, 'rb') as f:
                content = await f.read()
        except:
            # return
            content = await session.get(url)

        if content:
            async with aiofiles.open(cache_filepath, 'wb') as f:
                await f.write(content)

    except Exception as e:
        return {"domain": domain, "url": url, "title": None, "keywords": None, "error": str(e)}

    result = parse_metadata(domain, url, content, how=how)
    return result


# URLS = [
#     'https://rusvesna.su',
#     'http://alliedmods.net',
#     'http://antislaedcms.ru',
#     'http://ap-fusion.ru',
#     'http://art-gems.ru',
# ]


def chunkify(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


async def get_metadata():
    with open('url_list_v2.csv', 'r') as f:
        domains = [line.strip() for line in f.read().split('\n') if line.strip()]

    try:
        with open('titles-aiohttp.json', 'r') as f:
            results = json.load(f)
    except:
        results = {}

    urls = [domain for domain in domains if domain not in results]
    urls = urls[::-1]

    chunks = list(chunkify(urls, 128))

    session = ProxySession()
    # async with ProxySession() as session:
    for i, chunk in enumerate(chunks, start=1):
        print(f"[{i}/{len(chunks)}] processing the chunk..")
        tasks = [get_metadata_from_url(session, url) for url in chunk]
        chunk_results = await asyncio.gather(*tasks)

        for result in chunk_results:
            domain = result['domain']
            results[domain] = result
            # for k, v in result.items():
            #     print(f'{k:<10s} {v}')
            # print('-' * 80)

        print('saving...', end=' ', flush=True)
        with open('titles-aiohttp.json', 'w') as f:
            json.dump(results, f)
        # print('results saved: titles-aiohttp.json')
        print('OK!')
        


async def fix_titles():
    with open('url_list_v2.csv', 'r') as f:
        domains = [line.strip() for line in f.read().split('\n') if line.strip()]

    try:
        with open('titles-aiohttp.json', 'r') as f:
            results = json.load(f)
    except:
        results = {}

    session = ProxySession()

    # domains = ['05542online.com']

    urls = [domain for domain in domains if not results[domain].get('title') and os.path.exists(f'{CACHE_DIR}/{domain}.html')]
    print(len(urls), 'to process')
    random.shuffle(urls)

    chunks = list(chunkify(urls, 256))

    for i, chunk in enumerate(chunks, start=1):
        # print(f"[{i}/{len(chunks)}] processing the chunk..")
        tasks = [get_metadata_from_url(session, url, how='regex') for url in chunk]
        chunk_results = await asyncio.gather(*tasks)
        
        ok_count = 0
        err_count = 0

        for result in chunk_results:
            if result is None:
                continue

            domain = result['domain']
            # print(result)
            if result.get('title'):
                # print(f'{domain} YEAH:', result['title'][:30] + '...')
                ok_count += 1
            else:
                # print(f'{domain} NO :(')
                err_count += 1
            results[domain] = result

        print(f'got {ok_count}/{len(chunk)} titles! saving...', end=' ', flush=True)
        with open('titles-aiohttp.json', 'w') as f:
            json.dump(results, f)
        print('OK!')


async def download_cache():
    with open('tmp_2_1.csv', 'r') as f:
        domains = [line.strip() for line in f.read().split('\n') if line.strip()]

    with open('titles-aiohttp.json', 'r') as f:
        results = json.load(f)

    # urls = [domain for domain in domains if not os.path.exists(f'{CACHE_DIR}/{domain}.html')]
    urls = [domain for domain in domains if not results[domain].get('title') and not os.path.exists(f'{CACHE_DIR}/{domain}.html')]

    random.shuffle(urls)
    chunks = list(chunkify(urls, 128))

    session = ProxySession()
    # async with ProxySession() as session:
    for i, chunk in enumerate(chunks, start=1):
        print(f"[{i}/{len(chunks)}] processing the chunk..")
        tasks = [get_metadata_from_url(session, url) for url in chunk]
        chunk_results = await asyncio.gather(*tasks)

async def main():
    if len(sys.argv) != 2:
        print('Usage:')
        print('  python3 titles.py <command>\n')
        print('Available commands:')
        print(' - get_metadata')
        print(' - fix_titles')
        print(' - download_cache')
        sys.exit(1)

    if sys.argv[1] == 'get_metadata':
        await get_metadata()
    elif sys.argv[1] == 'fix_titles':
        await fix_titles()
    elif sys.argv[1] == 'download_cache':
        await download_cache()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        main()
    )