
.. .. image:: https://readthedocs.org/projects/findref/badge/?version=latest
    :target: https://findref.readthedocs.io/en/latest/
    :alt: Documentation Status

.. .. image:: https://github.com/MacHu-GWU/findref-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/findref-project/actions?query=workflow:CI

.. .. image:: https://codecov.io/gh/MacHu-GWU/findref-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/findref-project

.. image:: https://img.shields.io/pypi/v/findref.svg
    :target: https://pypi.python.org/pypi/findref

.. image:: https://img.shields.io/pypi/l/findref.svg
    :target: https://pypi.python.org/pypi/findref

.. image:: https://img.shields.io/pypi/pyversions/findref.svg
    :target: https://pypi.python.org/pypi/findref

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/findref-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/findref-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://findref.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://findref.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/findref-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/findref-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/findref-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/findref#files


Welcome to ``findref`` Documentation
==============================================================================


Usage Example
------------------------------------------------------------------------------
::

    # install
    $ pip install findref

    # enter the dataset name
    $ tf # Terraform reference
    $ cdk-python # AWS CDK Python reference
    $ boto3 # AWS boto3 Python SDK reference

Then you can enter your query to search, it support fuzzy search, ngram search.

It will ask you to wait for building the search index for the first time. After that, it will be very fast to search.

The dataset will be updated automatically every 30 days. You can also use ``!~`` followed by any query to force update the dataset. For example ``tf``, then ``aws s3 bucket!~``.

**Keyboard shortcuts**:

- hit ``Ctrl + E`` or ``UP`` to move item selection up.
- hit ``Ctrl + R`` to scroll item selection up.
- hit ``Ctrl + D`` or ``DOWN`` to move item selection up.
- hit ``Ctrl + F`` to scroll item selection up.
- hit ``Ctrl + H`` or ``LEFT`` to move query input cursor to the left (this won't work on Windows).
- hit ``Ctrl + L`` or ``RIGHT`` to move query input cursor to the right.
- hit ``Ctrl + G`` to move query input cursor to the previous word.
- hit ``Ctrl + K`` to move query input cursor to the next word.
- hit ``Ctrl + X`` to clear the query input.
- hit ``BACKSPACE`` to delete query input backward.
- hit ``DELETE`` to delete query input forward.
- hit ``Enter`` to **open the reference in web browser**.
- hit ``Ctrl + A`` to copy the url to clipboard.


Request for New Dataset
------------------------------------------------------------------------------
You can `create a new issue <https://github.com/MacHu-GWU/findref-project/issues/new>`_ and add the ``new dataset`` label to request for a new dataset. Please leave your comments and show me the link to the dataset you want to add.


Supported Dataset
------------------------------------------------------------------------------


Terraform Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support AWS, Azure, GCP.

.. image:: https://github.com/MacHu-GWU/findref-project/assets/6800411/189175f1-dcf1-4e21-bd7e-c416e5f7ede7


AWS CDK Python Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://github.com/MacHu-GWU/findref-project/assets/6800411/87f83c34-c81b-4d1f-968c-2c1867172d33



AWS boto3 Python SDK Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://github.com/MacHu-GWU/findref-project/assets/6800411/7cd2244f-f734-4bac-8690-ad5aadbcb0f4


.. _install:

Install
------------------------------------------------------------------------------

``findref`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install findref

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade findref
