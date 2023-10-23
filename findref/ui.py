# -*- coding: utf-8 -*-

"""
This module implements the terminal UI.
"""

import typing as T
import dataclasses

import sayt.api as sayt
import zelfred.api as zf
from fuzzywuzzy.process import extract

from . import models
from .paths import dir_index, dir_cache


dataset_list = [ds.value for ds in models.DataSetEnum]
dataset_set = set(dataset_list)


@dataclasses.dataclass
class DataSetItem(zf.Item):
    """
    Select a dataset to search.
    """

    @classmethod
    def from_dataset_list(cls, dataset_list: T.List[str]):
        return [
            DataSetItem(
                uid=dataset,
                title=f"🔍 {dataset!r} dataset",
                subtitle="Hit 'Tab' to search this dataset.",
                arg=dataset,
                autocomplete=f"{dataset} ",
            )
            for dataset in dataset_list
        ]


@dataclasses.dataclass
class UrlItem(zf.Item):
    """
    Common item class for all datasets.
    """

    def enter_handler(self, ui: zf.UI):
        """
        By default, Enter = open url in browser.
        """
        zf.open_url(self.arg)

    def ctrl_a_handler(self, ui: zf.UI):
        """
        By default, Ctrl + A = copy url to clipboard.
        """
        import pyperclip

        pyperclip.copy(self.arg)


def handler_for_selecting_dataset(query: str, ui: zf.UI):
    """
    This handler take the query for selecting the dataset to search.
    """
    if query:
        result = extract(query, dataset_list, limit=len(dataset_list))
        return DataSetItem.from_dataset_list([dataset for dataset, _ in result])
    else:
        return DataSetItem.from_dataset_list(dataset_list)


def search(
    dataset: str,
    ds: sayt.DataSet,
    query: str,
    refresh_data: bool = False,
) -> T.List[UrlItem]:
    """
    Search the given dataset and returns the item objects for UI.
    """
    dct_list = ds.search(
        query=query,
        limit=50,
        simple_response=True,
        refresh_data=refresh_data,
        verbose=False,
    )
    doc_class = models.get_doc_class(dataset)
    doc_list = [doc_class.from_dict(dct) for dct in dct_list]
    return [
        UrlItem(
            uid=doc.uid,
            title=doc.title,
            subtitle=doc.subtitle,
            arg=doc.arg,
            autocomplete=f"{dataset} {doc.autocomplete}",
        )
        for doc in doc_list
    ]


def creating_index_items() -> T.List[zf.Item]:
    return [
        zf.Item(
            uid="uid",
            title="Creating index, it may takes 5-30 seconds ...",
            subtitle="please wait, don't press any key",
        )
    ]


def handler_for_searching_reference(dataset: str, query: str, ui: zf.UI):
    """
    This handler search the reference url using the given dataset and query.
    """
    ds = models.create_sayt_dataset(
        dataset=dataset,
        dir_index=dir_index,
        dir_cache=dir_cache,
    )

    # display "creating index ..." message
    if ds.cache_key not in ds.cache:
        ui.run_handler(items=creating_index_items())
        ui.move_to_end()
        ui.clear_items()
        ui.clear_query()
        ui.print_query()
        ui.print_items()

        return search(dataset=dataset, ds=ds, query=query)

    # manually refresh data
    if query.strip().endswith("!~"):
        ui.run_handler(items=creating_index_items())
        ui.move_to_end()
        ui.clear_items()
        ui.clear_query()
        ui.print_query()
        ui.print_items()

        ui.line_editor.press_backspace(n=2)
        return search(
            dataset=dataset,
            ds=ds,
            query=query.strip()[:-2],
            refresh_data=True,
        )

    return search(dataset=dataset, ds=ds, query=query)


def handler(query: str, ui: zf.UI):
    """
    Findref query handler.
    """
    q = zf.Query.from_str(query)
    # example
    # - ""
    # - "  "
    if not q.trimmed_parts:
        return handler_for_selecting_dataset("", ui)
    # example
    # - "${dataset}${space}"
    # - "boto3 "
    # - "boto3 s3 bucket"
    elif (q.trimmed_parts[0] in dataset_set) and (len(q.parts) > 1):
        dataset = q.trimmed_parts[0]
        new_query = " ".join(q.parts[1:])
        if not new_query:
            new_query = "*"
        return handler_for_searching_reference(dataset, new_query, ui)
    # example
    # - "dataset name query"
    else:
        return handler_for_selecting_dataset(" ".join(q.trimmed_parts), ui)


def main():
    zf.debugger.enable()
    zf.debugger.path_log_txt.unlink(missing_ok=True)
    ui = zf.UI(handler=handler, capture_error=False)
    ui.run()
