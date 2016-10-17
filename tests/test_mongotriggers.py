import mongotriggers
import pymongo
import pytest
import threading
import time


@pytest.fixture
def connection(request):
    conn = pymongo.MongoClient(host='localhost', port=27017)

    def fin():
        conn.close()
    request.addfinalizer(fin)
    return conn


@pytest.fixture
def trigger(connection):
    mongotrigger = mongotriggers.MongodTrigger(connection, None)
    return mongotrigger


def basic_trigger(trigger, func, *argfunc):
    thread = threading.Thread(target=trigger.listen_start)
    thread.start()
    func(*argfunc)

    time.sleep(1)
    trigger.listen_stop()
    thread.join()


def test_single_insert(connection, trigger, capsys):
    def insert(op_doc):
        print('insert')
    trigger.register_insert_trigger(insert, 'test', 'insert_trigger')
    basic_trigger(trigger, connection['test']['insert_trigger'].insert, {'a': 1})
    out, err = capsys.readouterr()
    assert out == 'insert\n'


def test_single_update(connection, trigger, capsys):
    def update(op_doc):
        print('update')

    def operations(connection):
        connection['test']['update_trigger'].insert({'a': 1})
        connection['test']['update_trigger'].update({}, {'a': 2})

    trigger.register_update_trigger(update, 'test', 'update_trigger')
    basic_trigger(trigger, operations, connection)
    out, err = capsys.readouterr()
    assert out == 'update\n'


def test_single_delete(connection, trigger, capsys):
    def delete(op_doc):
        print('delete')

    def operations(connection):
        connection['test']['delete_trigger'].insert({'a': 3})
        connection['test']['delete_trigger'].remove({'a': 3})

    trigger.register_delete_trigger(delete, 'test', 'delete_trigger')
    basic_trigger(trigger, operations, connection)
    out, err = capsys.readouterr()
    assert out == 'delete\n'
