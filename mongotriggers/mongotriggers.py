import pymongo
import threading


# TODO: verify connection is mongod, if mongos, connect to all mongod instead
# TODO: create replicaset trigger which relies on majority of oplogs
class MongodTrigger(threading.Thread):

    def __init__(self, conn):
        # TODO: verify triggering is available using oplog, must be part of replica set
        self._oplog = conn.local.oplog.rs
        self._callbacks = []

    def _generate_namespace(self, db_name, collection_name):
        # TODO: allow partial namespace
        assert db_name and collection_name
        return db_name + '.' + collection_name

    def register_insert_trigger(self, func, db_name=None, collection_name=None):
        # TODO: get op name from pymongo?
        ns = self._generate_namespace(db_name, collection_name)
        callback = {'op': 'i', 'ns': ns, 'func': func}
        self._callbacks.append(callback)

    def register_delete_trigger(self, func, db_name=None, collection_name=None):
        ns = self._generate_namespace(db_name, collection_name)
        callback = {'op': 'd', 'ns': ns, 'func': func}
        self._callbacks.append(callback)

    def register_update_trigger(self, func, db_name=None, collection_name=None):
        ns = self._generate_namespace(db_name, collection_name)
        callback = {'op': 'u', 'ns': ns, 'func': func}
        self._callbacks.append(callback)

    def listen_stop(self):
        self.keep_listening = False
        # XXX: is it possible?
        # self.join()

    # TODO: currently must be created in a defered context
    def listen_start(self):
        self.keep_listening = True
        # remove shard operations
        query = {'fromMigrate': {'$exists': False}}
        while self.keep_listening:
            tailable_cur = self._oplog.find(query, cursor_type=pymongo.CursorType.TAILABLE)
            for op in tailable_cur:
                print (op)
                self._invoke_callbacks(op)

    def _invoke_callbacks(self, op_doc):
        for callback in self._callbacks:
            if op_doc['ns'] == callback['ns'] and op_doc['op'] == callback['op']:
                callback['func'](op_doc)
