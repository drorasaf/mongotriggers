Install MongoTriggers
=====================

You can install dask with ``pip``, or by installing from source.

Pip
---

To install MongoTriggers with ``pip``:

*   ``pip install mongotriggers``

Install from Source
-------------------

To install mongotriggers from source, clone the repository from `github
<https://github.com/drorasaf/mongotriggers>`_::

    git clone https://github.com/drorasaf/mongotriggers.git
    cd mongotriggers
    python setup.py install

or use ``pip`` locally if you want to install all dependencies as well::

    pip install -e .

Test
----

Test mongotriggers with ``py.test``::

    cd mongotriggers
    py.test mongotriggers
