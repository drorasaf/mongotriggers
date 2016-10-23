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
    mongotrigger = mongotriggers.MongoTrigger(connection)
    return mongotrigger


@pytest.fixture(scope='function')
def database(connection, request):
    def fin():
        connection.drop_database('test')
    request.addfinalizer(fin)
    return connection['test']


def basic_trigger(trigger, func, *argfunc):
    thread = threading.Thread(target=trigger.listen_start)
    thread.start()
    func(*argfunc)

    time.sleep(3)
    trigger.listen_stop()
    thread.join()


def test_single_insert(database, trigger, capsys):
    def insert(op_doc):
        print('insert')
    trigger.register_insert_trigger(insert, database.name, 'insert_trigger')
    basic_trigger(trigger, database['insert_trigger'].insert, {'a': 1})
    out, err = capsys.readouterr()
    assert out == 'insert\n'


def test_single_update(database, trigger, capsys):
    def update(op_doc):
        print('update')

    def operations(database):
        database['update_trigger'].insert({'a': 1})
        database['update_trigger'].update({}, {'a': 2})

    trigger.register_update_trigger(update, database.name, 'update_trigger')
    basic_trigger(trigger, operations, database)
    out, err = capsys.readouterr()
    assert out == 'update\n'


def test_single_delete(database, trigger, capsys):
    def delete(op_doc):
        print('delete')

    def operations(database):
        database['delete_trigger'].insert({'a': 3})
        database['delete_trigger'].remove({'a': 3})

    trigger.register_delete_trigger(delete, database.name, 'delete_trigger')
    basic_trigger(trigger, operations, database)
    out, err = capsys.readouterr()
    assert out == 'delete\n'
