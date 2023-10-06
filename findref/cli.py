# -*- coding: utf-8 -*-

import fire

from .data.boto3 import main as boto3_main
from .data.cdk_python import main as cdk_python_main


def run_boto3():
    fire.Fire(boto3_main)


def run_cdk_python():
    fire.Fire(cdk_python_main)


def run_cdk_ts():
    raise NotImplementedError


def run_cdk_java():
    raise NotImplementedError
