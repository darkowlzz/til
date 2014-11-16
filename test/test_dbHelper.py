import porc
import time

from src.dbHelper.dbHelper import DBHelper

ORCHESTRATE_KEY = '1de49651-92d0-4f7c-ae0b-ee92506a55f4'
COLLECTION_STATS = 'til_stats'
COLLECTION_TIL = 'til_til'

db = DBHelper(ORCHESTRATE_KEY)
client = porc.Client(ORCHESTRATE_KEY)


def test_get_next_id():
    '''Testing get_next_id'''
    uid = db.get_next_id()
    assert type(uid) == int
    item = client.get('til_stats', 'data')
    item['idCounter'] -= 1
    client.put(item.collection, item.key,
               item.json, item.ref).raise_for_status()


def test_get_id_index():
    '''Testing get_id_index'''
    uid = db.get_id_index()
    assert type(uid) == int


def test_save_til():
    '''Testing save_til'''
    id_before = db.get_id_index()
    db.save_til('learnt flask', 'mike')
    id_after = db.get_id_index()
    assert (id_before + 1) == id_after


def test_get_til_by_id():
    '''Testing get_til_by_id'''
    data = db.get_til_by_id(1)
    assert data['id'] == 1


def test_get_recent_til():
    '''Testing get_recent_til'''
    pages = db.get_recent_til()
    page = pages.next()
    assert 'count' in page.keys()  # count of number of items retrieved


def test_get_next_comment_id():
    '''Testing get_next_comment_id'''
    comment_before = db.get_comment_index()
    next_comment = db.get_next_comment_id()
    assert (comment_before+1) == next_comment


def test_decrement_comment_stats():
    '''Testing decrement_comment_stats'''
    comment_before = db.get_comment_index()
    r = db.decrement_comment_stats()
    assert r is True
    comment_after = db.get_comment_index()
    assert (comment_before-1) == comment_after


def test_get_til_total_comments():
    '''Testing get_til_total_comments'''
    current_index = db.get_id_index()
    total_comment = db.get_til_total_comments(current_index)
    assert total_comment == 0


def test_increment_comment_count():
    '''Testing increment_comment_count'''
    current_index = db.get_id_index()
    result = db.increment_comment_count(current_index)
    assert result is True
    total_comment = db.get_til_total_comments(current_index)
    assert total_comment == 1
    result = db.increment_comment_count(-1)
    assert result is False


def test_decrement_comment_count():
    '''Testing decrement_comment_count'''
    current_index = db.get_id_index()
    result = db.decrement_comment_count(current_index)
    assert result is True
    total_comment = db.get_til_total_comments(current_index)
    assert total_comment == 0
    result = db.decrement_comment_count(-1)
    assert result is False


def test_save_comment():
    '''Testing save_comment and get_comment'''
    current_index = db.get_id_index()
    t = time.localtime()
    time_now = {'hour': t.tm_hour, 'minute': t.tm_min, 'second': t.tm_sec,
                'year': t.tm_year, 'month': t.tm_mon, 'day': t.tm_mday}
    db.save_comment(current_index, 'cool!', 'anon piglet', time_now)
    comment_index = db.get_comment_index()
    item = db.get_comment(comment_index)
    assert item['comment'] == 'cool!'


def test_get_all_comments():
    '''Testing get_all_comments'''
    current_index = db.get_id_index()
    pages = db.get_all_comments(current_index)
    page = pages.next()
    results = page['results']
    result = results[0]['value']
    assert result['comment'] == 'cool!'
    assert result['nick'] == 'anon piglet'
