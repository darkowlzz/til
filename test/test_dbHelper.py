import src.dbHelper.dbHelper as db
import apikeys as keys
import porc

API_KEY = keys.getDBkey()
COLLECTION_STATS = 'til_stats'
COLLECTION_TIL = 'til_til'

client = porc.Client(API_KEY)


def test_getNextID():
    '''Testing getNextID'''
    uid = db.getNextID()
    assert type(uid) == int
    item = client.get('til_stats', 'data')
    item['idCounter'] -= 1
    client.put(item.collection, item.key,
               item.json, item.ref).raise_for_status()


def test_getIDIndex():
    '''Testing getIDIndex'''
    uid = db.getIDIndex()
    assert type(uid) == int


def test_saveTIL():
    '''Testing saveTIL'''
    id_before = db.getIDIndex()
    db.saveTIL('learnt flask', 'mike')
    id_after = db.getIDIndex()
    assert (id_before + 1) == id_after


def test_getTILbyID():
    '''Testing getTILbyID'''
    data = db.getTILbyID(1)
    assert data['id'] == 1


def test_getRecentTIL():
    '''Testing getRecentTIL'''
    pages = db.getRecentTIL()
    page = pages.next()
    assert 'count' in page.keys()
