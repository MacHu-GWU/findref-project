# -*- coding: utf-8 -*-

"""
This module implements the command line interface.
"""

import fire

from .ui import main as ui_main

def main():
    fire.Fire(ui_main)
