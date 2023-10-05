# -*- coding: utf-8 -*-

from findref.data.cdk_python import (
    get_html_with_cache,
    homepage_url,
    Service,
    parse_homepage,
    Link,
    parse_service_page,
    downloader,
)
from rich import print as rprint

# records = downloader(first_n_service=3)
# rprint(records[:10])

# homepage_html = get_html_with_cache(homepage_url)
# services = parse_homepage(homepage_html)
# print(services)

service_url = "https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda.html"
service_html = get_html_with_cache(service_url)
links = parse_service_page("aws_cdk.aws_lambda", service_html)
print(links)