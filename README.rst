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

What is this?
-------------
mongodb-triggers is a light-weight library to allow trigger capabilities with mongodb.
the triggers are similar to ones that can be found in RDBM, although it is not on the server side but on the client side.

What is it good for?
====================
Modern applications have become near real-time response and updates, this leads to the requirement that any changes done in the data to be propagated up to the top level of the application as soon as possible.

In order to allow this to happen, any changes in the databases must be notified, similar project that use this method is https://github.com/meteor/meteor.

Installation
============

PyInstaller is available on PyPI. You can install it through pip::

    $ pip install mongotriggers

How to use?
===========
Let's assume the system in development is a financial one, and every deletion in the database is extremely important, so we would like to notified for each deletion.


.. code-block:: python

 from mongotrigger import MongoTrigger
 from pymongo import MongoClient

 def notify_manager(op_document):
     print ('wake up! someone is stealing money')

 def myfunc():
     client = MongoClient(host='localhost', port=27017)
     triggers = MongoTrigger(conn)
     triggers.register_delete_trigger(notify_manager, 'my_account', 'my_transactions')
     thread = threading.Thread(target=triggers.listen_start)
     thread.start()
    
     // do something impressive
    
     triggers.listen_stop()
     thread.join()

Keep in mind that it is meant to run in a defered context in order to run endlessly until it is cancelled.

API
===
The API functionality includes:

- register_insert_trigger  
- register_update_trigger  
- register_delete_trigger  
- listen_start  
- listen_stop  


Testing
=======
In order to develop, the additional requirements are:

- pytest
- pytest-cov
- tox

All packages can be installed using pip.
The easiest way to run the tests is to run tox.
