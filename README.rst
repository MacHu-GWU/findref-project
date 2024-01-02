
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
``findref`` is an interactive terminal app that can search tech documentation reference. It is Python, cross-platform, easy-to-install, and blazing fast.

.. image:: https://github.com/MacHu-GWU/findref-project/assets/6800411/e7bc899d-cf8b-46ea-84e3-2437e5a65014
    :align: center


Usage Example
------------------------------------------------------------------------------
::

    # install (you need Python3.8+)
    $ pip install findref

    # enter the interactive terminal app
    $ fr

Then you can follow the hint and enter your query to search, it support fuzzy search, ngram search (See 🚀 `supported-dataset`_)

It will ask you to wait for building the search index for the first time. After that, it will be very fast to search.

The dataset will be updated automatically every 30 days. You can also use ``!~`` followed by any query to force update the dataset. For example, if ``tf aws s3 bucket`` doesn't give you result, you can use ``tf aws s3 bucket!~`` to search again on the latest data.

**Keyboard shortcuts**:

- ⬆️: hit ``Ctrl + E`` or ``UP`` to move item selection up.
- ⏫: hit ``Ctrl + R`` to scroll item selection up.
- ⬇️: hit ``Ctrl + D`` or ``DOWN`` to move item selection down.
- ⏬: hit ``Ctrl + F`` to scroll item selection down.
- ⬅️: hit ``Ctrl + H`` or ``LEFT`` to move query input cursor to the left (this won't work on Windows).
- ➡️: hit ``Ctrl + L`` or ``RIGHT`` to move query input cursor to the right.
- ⏪: hit ``Ctrl + G`` to move query input cursor to the previous word.
- ⏩: hit ``Ctrl + K`` to move query input cursor to the next word.
- ↩️: hit ``Ctrl + X`` to clear the query input.
- ◀️: hit ``BACKSPACE`` to delete query input backward.
- ▶️: hit ``DELETE`` to delete query input forward.
- 🌐: hit ``Enter`` to **open the reference in web browser**.
- ✅: hit ``Ctrl + A`` to copy the url to clipboard.
- 🔴: hit ``Ctrl + C`` to quit the app.


Request for New Dataset
------------------------------------------------------------------------------
You can `create a new issue <https://github.com/MacHu-GWU/findref-project/issues/new?assignees=MacHu-GWU&labels=feature&projects=&template=request_for_new_dataset.md&title=%5BNew+Dataset%5D+%3Cthe+name+of+the+dataset%3E>`_ and add the ``new dataset`` label to request for a new dataset. Please leave your comments, show me the link to the dataset you want to add, and provide some sample query and matched url items and ``@MacHu-GWU`` (me).


Request for Enterprise Support
------------------------------------------------------------------------------
findref works for enterprise internal dataset too. If you want a customized version to support your enterprise internal dataset, please follow the instruction in `this ticket <https://github.com/MacHu-GWU/findref-project/issues/new?assignees=MacHu-GWU&labels=enterprise+support&projects=&template=request_for_enterprise_support.md&title=%5BEnterprise+support%5D+%3Cname+of+your+company%3E>`_, our team will contact you soon.


.. _supported-dataset:

Supported Dataset
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


🚀 Airflow Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://asciinema.org/a/616811.svg
    :target: https://asciinema.org/a/616811


🚀 AWS CloudFormation Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
todo


🚀 AWS boto3 Python SDK Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://asciinema.org/a/616817.svg
    :target: https://asciinema.org/a/616817


🚀 AWS CDK Python Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://asciinema.org/a/616818.svg
    :target: https://asciinema.org/a/616818


🚀 AWS CDK TypeScript Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://asciinema.org/a/616819.svg
    :target: https://asciinema.org/a/616819


🚀 PySpark Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. image:: https://asciinema.org/a/616821.svg
    :target: https://asciinema.org/a/616821


🚀 Pandas Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
todo


🚀 Terraform Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support AWS, Azure, GCP.

.. image:: https://asciinema.org/a/616822.svg
    :target: https://asciinema.org/a/616822


.. _install:

Install
------------------------------------------------------------------------------

``findref`` is released on PyPI, so all you need is to:

.. code-block:: console

    # you need Python3.8+
    $ pip install findref

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade findref
