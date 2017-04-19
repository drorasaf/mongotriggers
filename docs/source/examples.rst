Examples
========

Simple
------

This example provides the simplest option for using the package.

.. code-block:: python

    from mongotriggers import MongoTrigger
    from pymongo import MongoClient

    def notify_manager(op_document):
        print ('wake up! someone is adding me money')

    client = MongoClient(host='localhost', port=27017)
    triggers = MongoTrigger(client)

    # listens to update/insert/delete, any of these will trigger the callback
    triggers.register_op_trigger(notify_manager, 'my_account', 'my_transactions')
    triggers.tail_oplog()

    # make an operation to simulate interaction
    client['my_account']['my_transactions'].insert_one({"balance": 1000})
    triggers.stop_tail()
   


Tail from certain point in time
-------------------------------

This example provides explanations on how to start listening only from a certain point in time,
usually this will be helpful when persistency is required.

.. code-block:: python

    from mongotriggers import MongoTrigger
    from pymongo import MongoClient
    from bson.timestamp import Timestamp
    import time

    def notify_manager(op_document):
        print ('wake up! someone is adding me money')
 
    client = MongoClient(host='localhost', port=27017)

    # do something in collection to verify it is not called
    client['my_account']['my_transactions'].insert_one({"balance": 1000})
    # long waiting time due to timestamp
    time.sleep(5)
    now = Timestamp(datetime.datetime.utcnow(), 0)
    # will get notified only if event occurred after specified now
    triggers = MongoTrigger(client, since=now)

    triggers.register_op_trigger(notify_manager, 'my_account', 'my_transactions')
    triggers.tail_oplog()

    # write to collection to verify we receive the callback
    client['my_account']['my_transactions'].insert_one({"balance": 1000})
    triggers.stop_tail()
