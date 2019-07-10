import asyncio, collections, aiohttp, random, itertools, re, sys, json
from aiohttp_socks import SocksConnector, SocksVer
from aiohttp_socks.errors import SocksError, SocksConnectionError


PROXIES = [('51.15.153.1', 50345)]
PROXIES_ITER = itertools.cycle(PROXIES)

USE_PROXY = 'SOCKS'
FETCH_ATTEMPTS = 3
FETCH_TIMEOUT = 10

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.122 Safari/537.36 Vivaldi/2.3.1440.61",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
]


class ProxySession:
    def __init__(self):
        pass

    def get_random_proxy_params(self, use_proxy=None):
        if not use_proxy:
            connector = None
            proxy_url = None
        elif use_proxy.startswith('HTTP'):
            connector = None
            proxy = next(PROXIES_ITER)
            if len(proxy) == 2:
                host, port = proxy
                proxy_url = f'http://{host}:{port}'
            elif len(proxy) == 4:
                host, port, username, password = proxy
                proxy_url = f'http://{username}:{password}@{host}:{port}'
        elif use_proxy.startswith('SOCKS'):
            proxy = next(PROXIES_ITER)
            if len(proxy) == 2:
                host, port = proxy
                username = password = None
            elif len(proxy) == 4:
                host, port, username, password = proxy
            connector = SocksConnector(SocksVer.SOCKS5, host, port, username=username, password=password)
            proxy_url = None
        return connector, proxy_url
    
    def get_proxy_params(self, proxy_url):
        schema, username, password, host, port = re.match('(.*?)://(?:(.*?):(.*?)@)?(.*?):(\d+)', proxy_url).groups()
        port = int(port)
        if schema.startswith('http'):
            connector = None
            proxy_url = proxy_url
        elif schema.startswith('socks'):
            connector = SocksConnector(SocksVer.SOCKS5, host, port, username=username, password=password)
            proxy_url = None
        return connector, proxy_url


    async def fetch(self, method, url, attempts=FETCH_ATTEMPTS, use_proxy=USE_PROXY, *args, **kwargs):
        for attempt in range(attempts):
            # print(attempt, url)
            try:
                if use_proxy in ('SOCKS', 'HTTP'):
                    connector, proxy_url = self.get_random_proxy_params(use_proxy)
                elif '://' in use_proxy:
                    connector, proxy_url = self.get_proxy_params(use_proxy)

                # if attempt == attempts - 1:
                #     connector = None
                #     proxy_url = None

                async with aiohttp.ClientSession(connector=connector) as session:
                    ua = random.choice(USER_AGENTS)
                    headers = {'User-Agent': ua}
                    kwargs_headers = kwargs.pop('headers', {}) or {}
                    headers.update(kwargs_headers)

                    # print(url, attempt)
                    response = await session.request(
                        method,
                        url,
                        headers=headers,
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=FETCH_TIMEOUT),
                        *args,
                        **kwargs
                    )
                    # print(response)
                    
                    return await response.read()
            except (asyncio.TimeoutError, SocksError, SocksConnectionError, aiohttp.client_exceptions.ClientError, aiohttp.client_exceptions.ServerDisconnectedError) as e:
            # except ValueError as e:
                if attempt == attempts - 1:
                    raise e
                else:
                    continue
        
    
    async def get(self, url, *args, **kwargs):
        return await self.fetch('get', url, *args, **kwargs)

    async def post(self, url, *args, **kwargs):
        return await self.fetch('post', url, *args, **kwargs)


def chunkify(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

