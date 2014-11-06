import sys
sys.path.append('../src')
import dbHelper.dbHelper as db
import porc

API_KEY = '1de49651-92d0-4f7c-ae0b-ee92506a55f4'
client = porc.Client(API_KEY)


def test_getNextID():
    '''Testing getNextID'''
    uid = db.getNextID(True)
    assert type(uid) == int
    item = client.get('test_stats', 'data')
    item['idCounter'] -= 1
    client.put(item.collection, item.key,
               item.json, item.ref).raise_for_status()


def test_getIDIndex():
    '''Testing getIDIndex'''
    uid = db.getIDIndex(True)
    assert type(uid) == int


def test_saveTIL():
    '''Testing saveTIL'''
    id_before = db.getIDIndex(True)
    db.saveTIL('learnt flask', 'mike', True)
    id_after = db.getIDIndex(True)
    assert (id_before+1) == id_after


def test_getTILbyID():
    '''Testing getTILbyID'''
    data = db.getTILbyID(5, True)
    assert data['id'] == 5


def test_getRecentTIL():
    '''Testing getRecentTIL'''
    pages = db.getRecentTIL(True)
    page = pages.next()
    assert 'count' in page.keys()
