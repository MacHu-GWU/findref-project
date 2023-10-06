
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
Usage example::

    # install
    $ pip install findref

    # search AWS CDK Python reference
    $ cdk-python

    # then you can:
    # type service name resource name to search, it support fuzzy search, ngram search
    # hit CTRL + E or UP to move item selection up
    # hit CTRL + R to scroll item selection up
    # hit CTRL + D or DOWN to move item selection up
    # hit CTRL + F to scroll item selection up
    # hit CTRL + H or LEFT to move query input cursor to the left
    # hit CTRL + L or RIGHT to move query input cursor to the right
    # hit CTRL + G to move query input cursor to the previous word
    # hit CTRL + K to move query input cursor to the next word
    # hit CTRL + X to clear the query input
    # hit BACKSPACE to delete query input backward
    # hit DELETE to delete query input forward
    # hit Enter to jump to open the reference in web browser


.. _install:

Install
------------------------------------------------------------------------------

``findref`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install findref

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade findref
