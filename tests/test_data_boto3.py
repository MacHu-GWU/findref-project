# -*- coding: utf-8 -*-

from findref.data.boto3 import get_record_list_from_boto3_website
from rich import print as rprint

def test():
    records = get_record_list_from_boto3_website(first_n_service=3, random_first_n=True)
    rprint(records)


if __name__ == "__main__":
    from findref.tests import run_cov_test

    run_cov_test(__file__, "findref.data.boto3", preview=False)
