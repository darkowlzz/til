import porc

API_KEY = '1de49651-92d0-4f7c-ae0b-ee92506a55f4'
PROD_STATS = 'stats'
PROD_TIL = 'til'
TEST_STATS = 'test_stats'
TEST_TIL = 'test_til'

client = porc.Client(API_KEY)

def getNextID(test=False):
    if test:
        item = client.get(TEST_STATS, 'data')
    else:
        item = client.get(PROD_STATS, 'data')
    item.raise_for_status()
    item['idCounter'] += 1
    client.put(item.collection, item.key, item.json, item.ref).raise_for_status()
    return item['idCounter']

def getIDIndex(test=False):
    if test:
        item = client.get(TEST_STATS, 'data')
    else:
        item = client.get(PROD_STATS, 'data')
    item.raise_for_status()
    return item['idCounter']

def saveTIL(text='', nick='jimmy', test=False):
    if test:
        uid = getNextID(True)
    else:
        uid = getNextID()
    data = {'id': uid, 'nick': nick, 'text': text}
    if test:
        response = client.put(TEST_TIL, uid, data)
    else:
        response = client.put(PROD_TIL, uid, data)
    response.raise_for_status()
    return True

def getTILbyID(id, test=False):
    if test:
        item = client.get(TEST_TIL, id)
    else:
        item = client.get(PROD_TIL, id)
    item.raise_for_status()
    return item.json

def getRecentTIL(test=False):
    if test:
        pages = client.list(TEST_TIL)
    else:
        pages = client.list(PROD_TIL)
    return pages
