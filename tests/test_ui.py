# -*- coding: utf-8 -*-

from pprint import pprint
import zelfred.api as zf
from findref.models import DataSetEnum
from findref.ui import (
    handler,
    handler_for_selecting_dataset as hdl1,
    handler_for_searching_reference as hdl2,
)


def test():
    ui = zf.UI(handler=handler)

    items = hdl1(DataSetEnum.airflow, ui)
    assert DataSetEnum.airflow in items[0].title

    items = hdl2(DataSetEnum.airflow, "amazon s3", ui, 3, _test=True)
    # pprint(items)

    items = hdl2(DataSetEnum.boto3, "s3 put object", ui, 3, _test=True)
    # pprint(items)

    items = hdl2(DataSetEnum.cdk_python, "s3 bucket", ui, 3, _test=True)
    # pprint(items)

    items = hdl2(DataSetEnum.cdk_ts, "s3 bucket", ui, 3, _test=True)
    # pprint(items)

    items = hdl2(DataSetEnum.pyspark, "print schema", ui, 3, _test=True)
    # pprint(items)

    items = hdl2(DataSetEnum.tf, "aws res s3 bucket", ui, 3, _test=True)
    # pprint(items)


if __name__ == "__main__":
    from findref.tests import run_cov_test

    run_cov_test(__file__, "findref.ui", preview=False)
