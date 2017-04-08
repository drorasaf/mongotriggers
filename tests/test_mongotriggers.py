import bson
import datetime
import mongotriggers
import pymongo
import pytest
import threading
import time


@pytest.fixture
def mongod_no_replica(request):
    conn = pymongo.MongoClient(host='localhost', port=27018)

    def fin():
        conn.close()
    request.addfinalizer(fin)
    return conn


def test_not_replica(mongod_no_replica):
    with pytest.raises(TypeError):
        mongotriggers.MongoTrigger(mongod_no_replica)


@pytest.fixture
def mongos(request):
    conn = pymongo.MongoClient(host='localhost', port=27020)

    def fin():
        conn.close()
    request.addfinalizer(fin)
    return conn


def test_mongos(mongos):
    with pytest.raises(TypeError):
        mongotriggers.MongoTrigger(mongos)


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
    thread = threading.Thread(target=trigger.tail_oplog)
    thread.start()
    func(*argfunc)

    time.sleep(3)
    trigger.stop()
    thread.join()


def test_single_operation(database, trigger, capsys):
    def print_op(op_doc):
        print(op_doc['op'])

    def operation():
        database['any_trigger'].insert({'a': 1})
        database['any_trigger'].update({}, {'a': 2})
        database['any_trigger'].remove({'a': 2})

    trigger.register_op_trigger(print_op, database.name, 'any_trigger')
    basic_trigger(trigger, operation)
    out, err = capsys.readouterr()
    assert out == 'i\nu\nd\n'
    trigger.unregister_op_trigger(print_op, database.name, 'any_trigger')
    basic_trigger(trigger, operation)
    out, err = capsys.readouterr()
    assert out == ''


def test_single_insert(database, trigger, capsys):
    def insert(op_doc):
        print('insert')
    trigger.register_insert_trigger(insert, database.name, 'insert_trigger')
    basic_trigger(trigger, database['insert_trigger'].insert, {'a': 1})
    out, err = capsys.readouterr()
    assert out == 'insert\n'
    trigger.unregister_insert_trigger(insert, database.name, 'insert_trigger')
    basic_trigger(trigger, database['insert_trigger'].insert, {'a': 1})
    out, err = capsys.readouterr()
    assert out == ''


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
    trigger.unregister_update_trigger(update, database.name, 'update_trigger')
    basic_trigger(trigger, operations, database)
    out, err = capsys.readouterr()
    assert out == ''


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
    trigger.unregister_delete_trigger(delete, database.name, 'delete_trigger')
    basic_trigger(trigger, operations, database)
    out, err = capsys.readouterr()
    assert out == ''


def test_tailing_from_specific_date(database, connection, capsys):
    def delete(op_doc):
        print('delete')

    def operation():
        pass

    now = bson.timestamp.Timestamp(datetime.datetime.utcnow(), 0)
    database['delete_trigger'].insert({'a': 3})
    database['delete_trigger'].remove({'a': 3})
    trigger = mongotriggers.MongoTrigger(connection, since=now)
    trigger.register_delete_trigger(delete, database.name, 'delete_trigger')
    basic_trigger(trigger, operation)
    out, err = capsys.readouterr()
    assert out == 'delete\n'
