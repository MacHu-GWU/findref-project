# -*- coding: utf-8 -*-

from findref.data.tf import get_record_list_from_hashicorp_website
from rich import print as rprint


def test():
    records = get_record_list_from_hashicorp_website(skip_clone=True)
    rprint(records[:10])


if __name__ == "__main__":
    from findref.tests import run_cov_test

    run_cov_test(__file__, "findref.data.tf", preview=False)
