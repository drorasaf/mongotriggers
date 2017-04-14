Examples
========

Simple
------

This example provide the simplest option for using the package.

.. code-block:: python

    from mongotrigger import MongoTrigger
    from pymongo import MongoClient

    def notify_manager(op_document):
        print ('wake up! someone is adding me money')
        triggers.stop_tail()

    client = MongoClient(host='localhost', port=27017)
    triggers = MongoTrigger(conn)
    triggers.register_insert_trigger(notify_manager, 'my_account', 'my_transactions')
    triggers.tail_oplog()
    conn['my_account']['my_transactions'].insert_one({"balance": 1000})
