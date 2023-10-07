# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import subprocess

import afwf_shell.api as afwf_shell

from ..os_platform import IS_WINDOWS


@dataclasses.dataclass
class Item(afwf_shell.Item):
    """
    Common item class for all datasets.
    """
    def enter_handler(self):
        """
        By default, Enter = open url in browser.
        """
        if IS_WINDOWS:
            subprocess.run(["start", self.arg], shell=True)
        else:
            subprocess.run(["open", self.arg])

    def ctrl_a_handler(self):
        """
        By default, Ctrl + A = copy url to clipboard.
        """
        import pyperclip

        pyperclip.copy(self.arg)


SEP_LIST = "!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/'"


def preprocess_query(query: str) -> str:
    """
    Tokenize query string, remove all special characters.

    This method is used to preprocess query before searching.

    Example:

        >>> preprocess_query("  hello + world, alice & bob! ")
        "hello world alice bob"
    """
    query = query.strip()
    if not query:
        query = "*"
    else:
        for char in SEP_LIST:
            query = query.replace(char, " ")
        words = [word for word in query.split(" ") if word.strip()]
        query = " ".join(words)
    return query


def print_creating_index(ui: afwf_shell.UI):
    """
    Print a message to tell user that we are creating index.

    This method is used when we need to create or recreate the index.
    """
    items = [
        afwf_shell.Item(
            uid="uid",
            title="Creating index, it may takes 1-2 minutes ...",
            subtitle="please wait, don't press any key",
        )
    ]
    ui.print_items(items=items)


def another_event_loop_until_print_items(ui: afwf_shell.UI):
    """
    Manually run one round of event loop all the way until ``print_items`` action.

    This method is used to skip the ``process_input`` action, so that we can manually
    print pre-defined items.
    """
    ui.move_to_end()
    ui.clear_items()
    ui.clear_query()
    ui.print_query()
