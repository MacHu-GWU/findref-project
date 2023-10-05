# -*- coding: utf-8 -*-

from findref import api


def test():
    _ = api


if __name__ == "__main__":
    from findref.tests import run_cov_test

    run_cov_test(__file__, "findref.api", preview=False)
