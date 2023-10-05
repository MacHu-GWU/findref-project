# -*- coding: utf-8 -*-

import requests
from .cache import cache

HTTP_CACHE_EXPIRE = 24 * 3600  # 24 hours


def get_html_with_cache(url: str) -> str:
    """
    Crawl the URL HTML content, store it to the disk cache.

    :param url: webpage URL
    :return: the HTML
    """
    if url in cache:
        return cache.get(url)
    else:
        html = requests.get(url).text
        cache.set(url, html, expire=HTTP_CACHE_EXPIRE)
        return html
