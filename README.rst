=============
MongoTriggers
=============
.. image:: https://api.travis-ci.org/drorasaf/mongotriggers.svg?branch=master
        :target: https://travis-ci.org/drorasaf/mongotriggers

.. image:: https://coveralls.io/repos/github/drorasaf/mongotriggers/badge.svg?branch=master
        :target: https://coveralls.io/github/drorasaf/mongotriggers?branch=master

.. image:: https://img.shields.io/pypi/v/mongotriggers.svg
        :target: https://pypi.python.org/pypi/mongotriggers

.. image:: https://img.shields.io/pypi/dm/mongotriggers.svg
        :target: https://pypi.python.org/pypi/mongotriggers

.. image:: https://readthedocs.org/projects/mongotriggers/badge/?version=latest
        :target: http://mongotriggers.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

What is this?
-------------
mongodb-triggers is a light-weight library to allow real live changes notification.
This is similar to triggers in SQL. This capability can be found both in Java and JavaScript(MeteorJS)

What is it good for?
====================
Modern applications have become near real-time response and updates, this leads to the requirement that any changes done in the data to be propagated up to the top level of the application as soon as possible.

In order to allow this to happen, any changes in the databases must be notified, similar project that use this method is https://github.com/meteor/meteor.

More Documentation can be found at http://mongotriggers.readthedocs.io

Installation
============

Installer is available on PyPI. You can install it through pip::

    $ pip install mongotriggers

Why should I use it?
====================
The best functionality is the one that another one is maintaining for you, as well as 100% code coverage.
This package follows best practices as published by MongoDB: 
- https://www.mongodb.com/blog/post/tailing-mongodb-oplog-sharded-clusters
- https://www.mongodb.com/blog/post/pitfalls-and-workarounds-for-tailing-the-oplog-on-a-mongodb-sharded-cluster  

How to use?
===========
Let's assume the system in development is a financial one, and every deletion in the database is extremely important, so we would like to notified for each deletion.


.. code-block:: python

 from mongotriggers import MongoTrigger
 from pymongo import MongoClient

 def notify_manager(op_document):
     print ('wake up! someone is adding me money')

 client = MongoClient(host='localhost', port=27017)
 triggers = MongoTrigger(conn)
 triggers.register_op_trigger(notify_manager, 'my_account', 'my_transactions')

 triggers.tail_oplog()
 client['my_account']['my_transactions'].insert_one({"balance": 1000})
 triggers.stop_tail()


Keep in mind that it is meant to run in a defered context in order to run endlessly until it is cancelled.

Testing
=======
In order to develop, the additional requirements are:

- pytest
- pytest-cov
- tox

All packages can be installed using pip.
The easiest way to run the tests is to run tox.
