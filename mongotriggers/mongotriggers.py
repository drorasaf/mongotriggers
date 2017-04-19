from .mongodtriggers import MongodTrigger
import threading

"""Class for manipulating notifications from MongoDB """


class MongoTrigger(object):

    def __init__(self, conn, since=None):
        """Creates MongoTriggers instance

        The object uses a defered context to provide notification on a
        different context to avoid exploiting the caller thread/process

        Args:
            conn (MongoClient) - connection on which triggers will be fired
            since (datetime) - the last timestamp to start listening from
        """
        self.trigger = MongodTrigger(conn, since)
        self.thread = None

    def tail_oplog(self):
        """Listens to oplog and fire the registered callbacks """
        if self.thread:
            raise OSError("unable to tail using more than 1 thread")

        self.thread = threading.Thread(target=self.trigger.start_tailing)
        self.thread.start()

    def stop_tail(self):
        """Stops listening to the oplog, no callbacks after calling this """
        self.trigger.stop_tailing()
        self.thread.join()
        self.thread = None

    def register_op_trigger(self, func, db_name=None, collection_name=None):
        """Watches the specified database and collections for any changes

        Args:
            func (callback): function to be invoked when any operation occurs
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.register_insert_trigger(func, db_name, collection_name)
        self.trigger.register_update_trigger(func, db_name, collection_name)
        self.trigger.register_delete_trigger(func, db_name, collection_name)

    def register_insert_trigger(self, func, db_name=None, collection_name=None):
        """Adds an insert callback to the specified namespace

        Args:
            func (callback): callback to execute when an insert operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.register_insert_trigger(func, db_name, collection_name)

    def register_update_trigger(self, func, db_name=None, collection_name=None):
        """Adds ann update callback to the specified namespace

        Args:
            func (callback): callback to execute when an update operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.register_update_trigger(func, db_name, collection_name)

    def register_delete_trigger(self, func, db_name=None, collection_name=None):
        """Adds a delete callback to the specified namespace

        Args:
            func (callback): callback to execute when a delete operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.register_delete_trigger(func, db_name, collection_name)

    def unregister_op_trigger(self, func, db_name=None, collection_name=None):
        """Removes all callbacks from the specified namespace

        Args:
            func (callback): callback to disable when any operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.unregister_insert_trigger(func, db_name, collection_name)
        self.trigger.unregister_update_trigger(func, db_name, collection_name)
        self.trigger.unregister_delete_trigger(func, db_name, collection_name)

    def unregister_insert_trigger(self, func, db_name=None, collection_name=None):
        """Removes an insert callback from the specified namespace

        Args:
            func (callback): callback to disable when an insert operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.unregister_insert_trigger(func, db_name, collection_name)

    def unregister_update_trigger(self, func, db_name=None, collection_name=None):
        """Removes an update callback from the specified namespace

        Args:
            func (callback): callback to disable when an insert operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.unregister_update_trigger(func, db_name, collection_name)

    def unregister_delete_trigger(self, func, db_name=None, collection_name=None):
        """Removes a delete callback from the specified namespace

        Args:
            func (callback): callback to disable when an insert operation occur
            db_name (str): name of Mongo database to watch for changes
            collection_name (str): name of Mongo collection to watch for changes
        """
        self.trigger.unregister_delete_trigger(func, db_name, collection_name)
