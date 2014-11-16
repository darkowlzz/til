import porc
import time

from src.dbHelper.dbHelper import DBHelper

ORCHESTRATE_KEY = '1de49651-92d0-4f7c-ae0b-ee92506a55f4'
COLLECTION_STATS = 'til_stats'
COLLECTION_TIL = 'til_til'

db = DBHelper(ORCHESTRATE_KEY)
client = porc.Client(ORCHESTRATE_KEY)


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
    assert 'count' in page.keys()  # count of number of items retrieved


def test_get_til_total_comments():
    '''Testing get_til_total_comments'''
    current_index = db.getIDIndex()
    total_comment = db.get_til_total_comments(current_index)
    assert total_comment == 0


def test_increment_comment_count():
    '''Testing increment_comment_count'''
    current_index = db.getIDIndex()
    result = db.increment_comment_count(current_index)
    assert result is True
    total_comment = db.get_til_total_comments(current_index)
    assert total_comment == 1
    result = db.increment_comment_count(-1)
    assert result is False


def test_decrement_comment_count():
    '''Testing decrement_comment_count'''
    current_index = db.getIDIndex()
    result = db.decrement_comment_count(current_index)
    assert result is True
    total_comment = db.get_til_total_comments(current_index)
    assert total_comment == 0
    result = db.decrement_comment_count(-1)
    assert result is False


def test_save_comment():
    '''Testing save_comment and get_comment'''
    current_index = db.getIDIndex()
    t = time.localtime()
    time_now = {'hour': t.tm_hour, 'minute': t.tm_min, 'second': t.tm_sec,
                'year': t.tm_year, 'month': t.tm_mon, 'day': t.tm_mday}
    db.save_comment(current_index, 'cool!', 'anon piglet', time_now)
    comment_index = '%d-%d' % (current_index, 1)
    item = db.get_comment(comment_index)
    assert item['comment'] == 'cool!'


def test_get_all_comments():
    '''Testing get_all_comments'''
    current_index = db.getIDIndex()
    pages = db.get_all_comments(current_index)
    page = pages.next()
    result = page['results'][0]['value']
    assert result['comment'] == 'cool!'
    assert result['nick'] == 'anon piglet'
