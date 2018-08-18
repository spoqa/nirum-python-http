Nirum HTTP transport for Python
===============================

.. image:: https://api.travis-ci.com/nirum-lang/nirum-python-http.svg?branch=master
   :target: https://travis-ci.com/nirum-lang/nirum-python-http
   :alt: Build status

.. image:: https://badge.fury.io/py/nirum-http.svg
   :target: https://pypi.org/project/nirum-http/
   :alt: Latest PyPI version

This package provides an HTTP transport for nirum-python_.

.. code-block:: python

   from yourservice import YourService_Client
   from nirum_http import HttpTransport

   transport = HttpTransport('https://service-host/')
   client = YourService_Client(transport)

Since ``HttpTransport`` utilizes requests_ library under the hood, it can take
a `session object`_ as well:

.. code-block:: python

   from requests import Session

   session = Session()
   session.auth = ('user', 'password')
   transport = HttpTransport('https://service-host/', session=session)

.. _nirum-python: https://github.com/nirum-lang/nirum-python
.. _requests: http://python-requests.org/
.. _session object: http://docs.python-requests.org/en/master/user/advanced/#session-objects

.. include:: CHANGES.rst
