import porc

COLLECTION_STATS = 'til_stats'
COLLECTION_TIL = 'til_til'


class DBHelper():
    '''Database Helper class

    It consists of helper functions for specific tasks which require
    interaction with the database.
    '''

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = porc.Client(self.api_key)

    def getNextID(self):
        '''Returns an new ID.'''
        item = self.client.get(COLLECTION_STATS, 'data')
        item.raise_for_status()
        item['idCounter'] += 1
        self.client.put(item.collection, item.key,
                        item.json, item.ref).raise_for_status()
        return item['idCounter']

    def getIDIndex(self):
        '''Returns index of current ID.'''
        item = self.client.get(COLLECTION_STATS, 'data')
        item.raise_for_status()
        return item['idCounter']

    def saveTIL(self, text='', nick='jimmy'):
        '''Saves TIL in the database.
        Arguments:
        text -- submitted TIL text
        nick -- nick of the user submitting the TIL
        '''
        uid = self.getNextID()
        data = {'id': uid, 'nick': nick, 'text': text}
        response = self.client.put(COLLECTION_TIL, uid, data)
        response.raise_for_status()
        return True

    def getTILbyID(self, id):
        '''Returns a dictionary with all the TIL data of the given TIL id
        Arguments:
        id -- id of the requested TIL
        '''
        item = self.client.get(COLLECTION_TIL, id)
        item.raise_for_status()
        return item.json

    def getRecentTIL(self):
        '''Returns `pages` containing the saved TIL'''
        pages = self.client.search(COLLECTION_TIL, '*', sort='value.id:desc')
        return pages
