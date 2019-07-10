import asyncio
import json
import re

import lxml.html
import pyppeteer

import pandas as pd

file_path = 'tmp.csv'
tmp = pd.read_csv(file_path, sep='\t')

URLS = ['http://'+ x[2:-1] for x in list(tmp['d1'].append(tmp['d2'].append(tmp['d3'])).dropna())]

async def get_metadata_from_url(browser, url):
    page = await browser.newPage()
    await page.setViewport({'width': 1680, 'height': 1050})
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')

    try:
        await page.goto(url, timeout=20000)  # 10 seconds
    except Exception as e:
        return {"url": url, "titles": None, "keywords": None, "error": str(e)}

    html = await page.content()

    tree = lxml.html.fromstring(html)
    
    title = tree.find('.//title')
    if title is not None:
        title = title.text_content().strip()
    
    keywords = tree.find('.//meta[@name="keywords"]')
    if keywords is not None:
        keywords = keywords.attrib.get('content', '').strip()

    await page.close()

    return {
        'url': url,
        'title': title,
        'keywords': keywords,
    }

def chunkify(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

async def main():
    browser = await pyppeteer.launch(
        headless=False,
        args=['--window-size=10,10']
    )

    # # список урлов из файла
    # with open('titles-urls.txt', 'r') as f:
    #     URLS = [line.strip() for line in f.read().split('\n') if line.strip()]

    results = []
    chunks = chunkify(URLS, 10)
    for chunk in chunks:
        tasks = [get_metadata_from_url(browser, url) for url in chunk]
        chunk_results = await asyncio.gather(*tasks)

        for result in chunk_results:
            for k, v in result.items():
                print(f'{k:<10s} {v}')
            print('-' * 80)

        results += chunk_results

    with open('titles-pyppeteer.json', 'w') as f:
        json.dump(results, f)
    print('results saved: titles-pyppeteer.json')

    await browser.close()
    
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        main()
    )
