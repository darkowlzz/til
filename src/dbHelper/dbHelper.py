import src.apikeys as keys
import porc

API_KEY = keys.getDBkey()
COLLECTION_STATS = 'til_stats'
COLLECTION_TIL = 'til_til'

client = porc.Client(API_KEY)


def getNextID():
    item = client.get(COLLECTION_STATS, 'data')
    item.raise_for_status()
    item['idCounter'] += 1
    client.put(item.collection, item.key,
               item.json, item.ref).raise_for_status()
    return item['idCounter']


def getIDIndex():
    item = client.get(COLLECTION_STATS, 'data')
    item.raise_for_status()
    return item['idCounter']


def saveTIL(text='', nick='jimmy'):
    uid = getNextID()
    data = {'id': uid, 'nick': nick, 'text': text}
    response = client.put(COLLECTION_TIL, uid, data)
    response.raise_for_status()
    return True


def getTILbyID(id):
    item = client.get(COLLECTION_TIL, id)
    item.raise_for_status()
    return item.json


def getRecentTIL():
    pages = client.list(COLLECTION_TIL)
    return pages
