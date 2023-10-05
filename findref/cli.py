# -*- coding: utf-8 -*-

import fire
import typing as T
from pathlib import Path

from .data.cdk_python import main as cdk_python_main


def run_cdk_python():
    fire.Fire(cdk_python_main)
