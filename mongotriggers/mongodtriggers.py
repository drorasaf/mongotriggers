from pymongo import CursorType
import time


class MongodTrigger(object):

    def __init__(self, conn, since=None):
        self._oplog = conn.local.oplog.rs
        self._verify_mongod_with_oplog(conn)
        self._callbacks = []
        self.keep_listening = True
        if since is None:
            query = {'fromMigrate': {'$exists': False}}
            self._start_time = self._oplog.find(query).sort('$natural', -1)[0]['ts']
        else:
            self._start_time = since

    def _verify_mongod_with_oplog(self, conn):
        if conn.is_mongos:
            raise TypeError('Connection must be mongod, but it is mongos')
        if not conn.is_primary:
            raise TypeError('Connection must be primary, but it is not')
        doc = self._oplog.find_one()
        if doc is None:
            raise TypeError('Connection must have oplog enable, try restart service as '
                            'replica set of a single server, for more details see '
                            'https://jira.mongodb.org/browse/SERVER-12039')

    def _generate_namespace(self, db_name, collection_name):
        # allow partial namespace
        assert db_name and collection_name
        return db_name + '.' + collection_name

    def register_insert_trigger(self, func, db_name=None, collection_name=None):
        ns = self._generate_namespace(db_name, collection_name)
        callback = {'op': 'i', 'ns': ns, 'func': func}
        self._callbacks.append(callback)

    def register_update_trigger(self, func, db_name=None, collection_name=None):
        ns = self._generate_namespace(db_name, collection_name)
        callback = {'op': 'u', 'ns': ns, 'func': func}
        self._callbacks.append(callback)

    def register_delete_trigger(self, func, db_name=None, collection_name=None):
        ns = self._generate_namespace(db_name, collection_name)
        callback = {'op': 'd', 'ns': ns, 'func': func}
        self._callbacks.append(callback)

    def unregister_insert_trigger(self, func, db_name=None, collection_name=None):
        self.unregister_op_trigger('i', func, db_name, collection_name)

    def unregister_update_trigger(self, func, db_name=None, collection_name=None):
        self.unregister_op_trigger('u', func, db_name, collection_name)

    def unregister_delete_trigger(self, func, db_name=None, collection_name=None):
        self.unregister_op_trigger('d', func, db_name, collection_name)

    def unregister_op_trigger(self, op, func, db_name=None, collection_name=None):
        ns = self._generate_namespace(db_name, collection_name)
        for callback in self._callbacks:
            if ns == callback['ns'] and op == callback['op']:
                self._callbacks.remove(callback)

    def stop_tailing(self):
        self.keep_listening = False

    def start_tailing(self):
        # remove shard operations
        query = {'fromMigrate': {'$exists': False}, 'ts': {'$gt': self._start_time}}

        tailable_cur = self._oplog.find(query,
                                        cursor_type=CursorType.TAILABLE_AWAIT).sort('$natural', 1)
        while tailable_cur.alive:
            try:
                op = tailable_cur.next()
                self._invoke_callbacks(op)
            except StopIteration:
                if not self.keep_listening:
                    break
                # change it to be configurable
                time.sleep(1)

    # add option to regex namespaces
    def _invoke_callbacks(self, op_doc):
        for callback in self._callbacks:
            if op_doc['ns'] == callback['ns'] and op_doc['op'] == callback['op']:
                callback['func'](op_doc)
