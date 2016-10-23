from pymongo import CursorType
import time


class MongoTrigger(object):
    def __init__(self, conn, listen_time=None):
        # if mongos, connect to all mongod instead
        self.trigger = MongodTrigger(conn, listen_time)

    def register_insert_trigger(self, func, db_name=None, collection_name=None):
        self.trigger.register_insert_trigger(func, db_name, collection_name)

    def register_update_trigger(self, func, db_name=None, collection_name=None):
        self.trigger.register_update_trigger(func, db_name, collection_name)

    def register_delete_trigger(self, func, db_name=None, collection_name=None):
        self.trigger.register_delete_trigger(func, db_name, collection_name)

    def listen_stop(self):
        self.trigger.listen_stop()

    def listen_start(self):
        self.trigger.listen_start()


# create replicaset trigger which relies on majority of oplogs
class MongodTrigger(object):

    def __init__(self, conn, listen_time=None):
        self._oplog = conn.local.oplog.rs
        self._verify_mongod_with_oplog(conn)
        if listen_time is None:
            self._start_time = \
                self._oplog.find({'fromMigrate': {'$exists': False}}).sort('$natural', -1)[0]['ts']
        else:
            self._start_time = listen_time
        self._callbacks = []
        self.keep_listening = True

    def _verify_mongod_with_oplog(self, conn):
        if conn.is_mongos:
            raise TypeError('Connection must be mongod, but it is mongos')
        if not conn.is_primary:
            raise TypeError('Connection must be primary, but it is not')
        doc = self._oplog.find_one()
        if doc is None:
            raise TypeError('Connection must have oplog enable, try restart service as '
                            'replicaset of a single server, for more details see '
                            'https://jira.mongodb.org/browse/SERVER-12039')

    def _generate_namespace(self, db_name, collection_name):
        # allow partial namespace
        assert db_name and collection_name
        return db_name + '.' + collection_name

    def register_insert_trigger(self, func, db_name=None, collection_name=None):
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

    def listen_start(self):
        # remove shard operations
        query = {'fromMigrate': {'$exists': False}}
        if self._start_time:
            query.update({'ts': {'$gt': self._start_time}})

        tailable_cur = self._oplog.find(query,
                                        cursor_type=CursorType.TAILABLE_AWAIT).sort('$natural', 1)
        while tailable_cur.alive and self.keep_listening:
            try:
                op = tailable_cur.next()
                self._invoke_callbacks(op)
            except StopIteration:
                time.sleep(1)

    def _invoke_callbacks(self, op_doc):
        for callback in self._callbacks:
            if op_doc['ns'] == callback['ns'] and op_doc['op'] == callback['op']:
                callback['func'](op_doc)
