import mongotriggers
import pymongo
import pytest
import threading


@pytest.fixture
def connection(request):
    conn = pymongo.MongoClient(host='localhost', port=27017)
    def fin():
        conn.close()
    request.addfinalizer(fin)
    return conn


@pytest.fixture
def trigger(connection):
    mongotrigger = mongotriggers.MongodTrigger(connection)
    return mongotrigger


def test_single_insert(connection, trigger, capsys):
    def insert(op_doc):
        print('insert')
    trigger.register_insert_trigger(insert, 'test', 'insert_trigger')
    thread = threading.Thread(target=trigger.listen_start)
    thread.start()
    connection['test']['insert_trigger'].insert({'a': 1})
    
    out, err = capsys.readouterr()
    assert out == 'insert'


def test_single_update(trigger, capsys):
    def update(op_doc):
        print('update')
    trigger.register_update_trigger(update, 'test', 'update_trigger')
#    trigger.run()


def test_single_delete(trigger, capsys):
    def delete(op_doc):
        print('delete')
    trigger.register_delete_trigger(delete, 'test', 'delete_trigger')
#    trigger.run()
