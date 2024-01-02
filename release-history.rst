.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.1 (2024-01-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``aws_cloudformation`` dataset.
- Add ``pandas`` dataset.


0.1.3 (2023-10-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Be able to handle delimiter character in user input query.
- Be able to handle single letter in user input query.


0.1.2 (2023-10-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug caused by the logger.


0.1.1 (2023-10-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Removed all "downloading dataset" logic, create another project to publish the dataset every month.
- The initial run (crawl data and build index) is much faster now, it takes 3-10 seconds, and it used to take 10-60 seconds.
- Rework the UI implementation, we no longer need to add a lot of code for adding a new dataset.

**Minor Improvements**

- Use asciinema to record demo.

**Miscellaneous**

- Improve the documentation.


0.0.6 (2023-10-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Hit ``Ctrl + A`` to copy url to clipboard.
- Allow user to use ``!~`` to rebuild the index with the latest data.

**Miscellaneous**

- Minor refactor.


0.0.5 (2023-10-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Lazy install extra dependencies for certain dataset.


0.0.4 (2023-10-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- preprocess query before doing the search, so it can handle more complex query.


0.0.3 (2023-10-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``boto3`` dataset.

**Bugfixes**

- Fix a bug that cannot open URL in Windows.


0.0.2 (2023-10-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix a bug that ``cdk_python`` only pull first data for 50 services.


0.0.1 (2023-10-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release.
- 0.0.X are experimental release. Please don't expect API stability.
- Add ``cdk_python`` dataset.
- Hit ``Enter`` to open the URL in browser.

**Miscellaneous**

- Tested on MacOS
- Tested on Windows
