# -*- coding: utf-8 -*-

import typing as T
import re
import random
import dataclasses

import sayt.api as sayt
import afwf_shell.api as afwf_shell
from bs4 import BeautifulSoup

from ..http import get_html_with_cache
from ..paths import dir_findref_home
from ._utils import (
    Item,
    preprocess_query,
    print_creating_index,
    another_event_loop_until_print_items,
)


DATASET_NAME = "boto3"

_dir_home = dir_findref_home.joinpath(DATASET_NAME)
_dir_home.mkdir(parents=True, exist_ok=True)

dir_index = _dir_home.joinpath(".index")
dir_cache = _dir_home.joinpath(".cache")


# ------------------------------------------------------------------------------
# Section 1. Download dataset
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class AWSService:
    """
    AWS Service data model.

    :param name: it is the clickable text in the boto3 document homepage sidebar.
        For example, for Identity Access Management, the url is
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html,
        the clickable text in the sidebar is "IAM".
    :param href_name: the last part of the document url.
        For example, for Elastic Block Storage service, the url is
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html,
        the last part is "iam".
    :param doc_url: the boto3 document url, for example, the IAM document url is
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
    """

    name: str = dataclasses.field()
    href_name: str = dataclasses.field()
    doc_url: str = dataclasses.field()


def extract_aws_service_list_from_home_page(html: str) -> T.List[AWSService]:
    """
    Get all AWS Service boto3 api homepage from the boto3 doc homepage,
    from its sidebar.

    :param html: the boto3 doc homepage html content.

    :return: a list of AWS Service data model.
    """
    aws_service_list = list()
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", class_="current")
    for a in ul.find_all("a", class_="reference internal"):
        # make sure the link is an aws service link
        if "#" not in a.attrs["href"]:
            href_name = a.attrs["href"]
            name = a.text
            doc_url = f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{href_name}"
            aws_service = AWSService(
                name=name,
                href_name=href_name,
                doc_url=doc_url,
            )
            # print(aws_service)
            aws_service_list.append(aws_service)
    return aws_service_list


def get_aws_service_list_from_home_page() -> T.List[AWSService]:
    """
    get all AWS Service boto3 api homepage from the boto3 doc homepage,
    from its sidebar.
    """
    url_available_services = "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html"
    html = get_html_with_cache(url_available_services)
    aws_service_list = extract_aws_service_list_from_home_page(html)
    return aws_service_list


def extract_service_id_from_service_page(soup: BeautifulSoup) -> str:
    """
    Given an AWS Service boto3 API documentation webpage HTML,
    extract the string token that used to create boto3 client.

    Example:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
        is the IAM document, the content of the page is the ``html``.
    - It returns ``iam``, the argument in ``boto3.client("iam")``.

    :param soup: BeautifulSoup object created by the AWS service document page html content
    :return: the AWS service id for boto3 client
    """
    # locate the following HTML content
    #
    # import boto3
    #
    # client = boto3.client('iam')
    div_client = soup.find("div", class_="highlight-default notranslate")
    service_id = None
    # extract the service id
    pattern = re.compile("client = boto3.client\('[\d\D]*'\)")
    for line in div_client.text.split("\n"):
        res = re.findall(pattern, line)
        if len(res):
            service_id = res[0].split("'")[1]
    return service_id


@dataclasses.dataclass
class Record:
    """
    Output for downloader.

    :param type: "client" means it is a client method,
        "pagi" means it is a paginator method.
    :param service_id: for example, "iam" is the argument for boto3.client("iam")
    :param service_name: for example, "IAM" is the text on the document page side bar
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
    :param method: for example, "create_role" is the method name
    """

    type: str = dataclasses.field()
    service_id: str = dataclasses.field()
    service_name: str = dataclasses.field()
    method: str = dataclasses.field()
    url: str = dataclasses.field()


def extract_records_from_aws_service_page(
    soup: BeautifulSoup,
    service_id: str,
    service_name: str,
) -> T.List[Record]:
    """
    Given an AWS service page like https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html
    extract all client methods and paginator methods.
    """
    records = list()

    # extract client methods
    # locate the "Client" section
    section = soup.find("section", id="client")
    if section is not None:
        for a in section.find_all("a", class_="reference internal"):
            try:
                href = a.attrs["href"]
                method_name = a.text.strip()
                api_url = f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{href}"
                record = Record(
                    type="client",
                    service_id=service_id,
                    service_name=service_name,
                    method=method_name,
                    url=api_url,
                )
                records.append(record)
            except:
                pass

    # extract paginator methods
    # locate the "Paginators" section
    section = soup.find("section", id="paginators")
    if section is not None:
        for a in section.find_all("a", class_="reference internal"):
            try:
                href = a.attrs["href"]
                method_name = a.text.strip()
                api_url = f"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/{href}"
                record = Record(
                    type="pagi",
                    service_id=service_id,
                    service_name=service_name,
                    method=method_name,
                    url=api_url,
                )
                records.append(record)
            except:
                pass
    return records


def get_record_list_from_boto3_website(
    first_n_service: int = 999,
    random_first_n: bool = False,
) -> T.List[Record]:
    aws_service_list = get_aws_service_list_from_home_page()
    records = list()
    if random_first_n:
        random.shuffle(aws_service_list)
    if first_n_service:
        aws_service_list = aws_service_list[:first_n_service]
    for aws_service in aws_service_list:
        html = get_html_with_cache(aws_service.doc_url)
        soup = BeautifulSoup(html, "html.parser")
        service_id = extract_service_id_from_service_page(soup)
        _records = extract_records_from_aws_service_page(
            soup, service_id, aws_service.name
        )
        records.extend(
            extract_records_from_aws_service_page(soup, service_id, aws_service.name)
        )
    return records


# ------------------------------------------------------------------------------
# Section 2. Search Engine
# ------------------------------------------------------------------------------
def downloader(
    first_n_service: int = 999,
    random_first_n: bool = False,
) -> T.List[T.Dict[str, T.Any]]:
    records = get_record_list_from_boto3_website(first_n_service, random_first_n)
    return [dataclasses.asdict(record) for record in records]


def cache_key_def(
    download_kwargs: sayt.T_KWARGS,
    context: sayt.T_CONTEXT,
):
    return ["findref-boto3"]


def extractor(
    record: sayt.T_RECORD,
    download_kwargs: sayt.T_KWARGS,
    context: sayt.T_CONTEXT,
) -> sayt.T_RECORD:
    doc = {
        "type": record["type"],
        "srv": record["service_name"],
        "srv_ng": record["service_name"],
        "srv_id": record["service_id"],
        "srv_id_ng": record["service_id"],
        "meth": record["method"],
        "meth_ng": record["method"],
        "url": record["url"],
    }
    return doc


fields = [
    sayt.KeywordField(
        name="type",
        stored=True,
        field_boost=3.0,
    ),
    sayt.TextField(
        name="srv",
        stored=True,
        field_boost=2.0,
    ),
    sayt.TextField(
        name="srv_id",
        stored=True,
        field_boost=2.0,
    ),
    sayt.TextField(
        name="meth",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="srv_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=2.0,
    ),
    sayt.NgramWordsField(
        name="srv_id_ng",
        stored=True,
        minsize=2,
        maxsize=6,
        field_boost=2.0,
    ),
    sayt.NgramWordsField(
        name="meth_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.StoredField(
        name="url",
    ),
]


dataset = sayt.RefreshableDataSet(
    downloader=downloader,
    cache_key_def=cache_key_def,
    extractor=extractor,
    fields=fields,
    dir_index=dir_index,
    dir_cache=dir_cache,
    cache_expire=30 * 24 * 3600,
)


def search(query: str, refresh_data: bool = False) -> T.List[Item]:
    query = preprocess_query(query)
    docs = dataset.search(
        download_kwargs={},
        query=query,
        refresh_data=refresh_data,
        limit=50,
        simple_response=True,
    )
    return [
        Item(
            uid=doc["url"],
            title="{} | {}.{}".format(
                doc["type"],
                doc["srv_id"].lower(),
                doc["meth"],
            ),
            subtitle=doc["url"],
            arg=doc["url"],
            autocomplete="{} {} {}".format(
                doc["type"],
                doc["srv_id"].lower(),
                doc["meth"],
            ),
            variables=doc,
        )
        for doc in docs
    ]


def handler(query: str, ui: afwf_shell.UI):
    # create index for the first time
    if dir_index.exists() is False:
        print_creating_index(ui)
        items = search(query)
        another_event_loop_until_print_items(ui)
        return items

    # rebuild the index with latest data, triggered by a query ends with "!~"
    if query.strip().endswith("!~"):
        print_creating_index(ui)
        query = query.strip()[:-2]
        items = search(query, refresh_data=True)
        ui.line_editor.press_backspace(n=2)
        another_event_loop_until_print_items(ui)
        return items

    return search(query)


def main():
    """
    Search Boto3 AWS Python SDK reference.

    Search boto3 API input output reference in https://boto3.amazonaws.com/v1/documentation/api/latest/index.html.
    """
    afwf_shell.debugger.enable()
    afwf_shell.debugger.path_log_txt.unlink(missing_ok=True)
    ui = afwf_shell.UI(handler=handler)
    ui.run()
