# -*- coding: utf-8 -*-

from findref.data.boto3 import (
    get_html_with_cache,
    DATASET_NAME,
    AWSService,
    extract_service_id_from_service_page,
    extract_aws_service_list_from_home_page,
    get_all_aws_service,
    Record,
    extract_records,
    downloader,
    cache_key_def,
    extractor,
    fields,
    dataset,
    Item,
    search,
    handler,
    main,
)
from rich import print as rprint

# records = downloader(first_n_service=3)
# rprint(records[:10])

# services = get_all_aws_service()
# rprint(services[:10])
