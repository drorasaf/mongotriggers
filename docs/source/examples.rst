Examples
========

Simple
------

This example provides the simplest option for using the package.

.. code-block:: python

    from mongotrigger import MongoTrigger
    from pymongo import MongoClient

    def notify_manager(op_document):
        print ('wake up! someone is adding me money')
        triggers.stop_tail()

    client = MongoClient(host='localhost', port=27017)
    triggers = MongoTrigger(client)
    triggers.register_insert_trigger(notify_manager, 'my_account', 'my_transactions')
    triggers.tail_oplog()
    conn['my_account']['my_transactions'].insert_one({"balance": 1000})


Tail from certain point in time
-------------------------------

This example provides explanations on how to start listening only from a certain point in time,
usually this will be helpful when persistency is required.

.. code-block:: python

    from mongotrigger import MongoTrigger
    from pymongo import MongoClient
    from bson.timestamp import Timestamp

    def notify_manager(op_document):
        print ('wake up! someone is adding me money')
        triggers.stop_tail()
 
    client = MongoClient(host='localhost', port=27017)
    now = Timestamp(datetime.datetime.utcnow(), 0)
    triggers = MongoTrigger(client, since=now)
    triggers.register_insert_trigger(notify_manager, 'my_account', 'my_transactions')
    triggers.tail_oplog()
    conn['my_account']['my_transactions'].insert_one({"balance": 1000})
