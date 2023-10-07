# -*- coding: utf-8 -*-

import typing as T
import subprocess
import dataclasses

import sayt.api as sayt
import afwf_shell.api as afwf_shell
from bs4 import BeautifulSoup

from ..http import get_html_with_cache
from ..paths import dir_findref_home
from ..os_platform import IS_WINDOWS
from ._utils import (
    Item,
    preprocess_query,
    print_creating_index,
    another_event_loop_until_print_items,
)


DATASET_NAME = "cdk_python"

_dir_home = dir_findref_home.joinpath(DATASET_NAME)
_dir_home.mkdir(parents=True, exist_ok=True)

dir_index = _dir_home.joinpath(".index")
dir_cache = _dir_home.joinpath(".cache")

base_url = "https://docs.aws.amazon.com/cdk/api/v2/python"
homepage_url = f"{base_url}/index.html"


@dataclasses.dataclass
class Service:
    name: str
    url: str


def parse_homepage(homepage_html: str) -> T.List[Service]:
    soup = BeautifulSoup(homepage_html, "html.parser")
    section = soup.find("section", id="aws-cdk-python-reference")
    services = list()
    for a in section.find_all("a"):
        if (a.text != "API Reference") and (
            a.attrs.get("title", "") != "Permalink to this heading"
        ):
            name = a.text
            url = "{}/{}".format(base_url, a.attrs["href"])
            service = Service(name, url)
            services.append(service)
    return services


@dataclasses.dataclass
class Link:
    service_name: str
    object_name: str
    object_url: str

    @property
    def is_cfn(self) -> bool:
        return self.object_name.startswith("Cfn")

    @property
    def service_name_facet(self) -> str:
        return self.service_name.replace("aws_cdk.aws_", "").replace("aws_cdk.", "")

    @property
    def object_name_facet(self) -> str:
        return self.object_name


def parse_service_page(service_name: str, service_html: str) -> T.List[Link]:
    """
    Example service page: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda.html
    """
    tag_id = service_name.replace("_", "-").replace(".", "-")
    soup = BeautifulSoup(service_html, "html.parser")
    section = soup.find("section", id=tag_id)
    table = section.find("table")
    if not table:
        return list()
    links = list()
    for tr in table.find_all("tr"):
        td_list = tr.find_all("td")
        a = td_list[0].find("a")
        if not a:
            continue
        if a.attrs.get("title", "") != "Permalink to this heading":
            object_name = a.text
            object_url = "{}/{}".format(base_url, a.attrs["href"])
            link = Link(service_name, object_name, object_url)
            links.append(link)
    return links


def downloader(first_n_service: int = 999) -> T.List[T.Dict[str, T.Any]]:
    homepage_html = get_html_with_cache(homepage_url)
    services = parse_homepage(homepage_html)
    records = list()
    for service in services[:first_n_service]:
        service_html = get_html_with_cache(service.url)
        links = parse_service_page(service.name, service_html)
        for link in links:
            record = dict(
                service=link.service_name_facet,
                object=link.object_name_facet,
                url=link.object_url,
            )
            records.append(record)
    return records


def cache_key_def(
    download_kwargs: sayt.T_KWARGS,
    context: sayt.T_CONTEXT,
):
    return ["findref-cdk_python"]


def extractor(
    record: sayt.T_RECORD,
    download_kwargs: sayt.T_KWARGS,
    context: sayt.T_CONTEXT,
) -> sayt.T_RECORD:
    doc = {
        "srv": record["service"],
        "srv_ng": record["service"],
        "obj": record["object"],
        "obj_ng": record["object"],
        "url": record["url"],
    }
    return doc


fields = [
    sayt.TextField(
        name="srv",
        stored=True,
    ),
    sayt.TextField(
        name="obj",
        stored=True,
    ),
    sayt.NgramWordsField(
        name="srv_ng",
        stored=True,
        minsize=2,
        maxsize=6,
    ),
    sayt.NgramWordsField(
        name="obj_ng",
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
            title="{} - {}".format(doc["srv"], doc["obj"]),
            subtitle=doc["url"],
            arg=doc["url"],
            autocomplete="{} {}".format(doc["srv"], doc["obj"]),
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
    afwf_shell.debugger.enable()
    afwf_shell.debugger.path_log_txt.unlink(missing_ok=True)
    ui = afwf_shell.UI(handler=handler)
    ui.run()
