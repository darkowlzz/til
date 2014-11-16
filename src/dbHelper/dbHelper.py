import porc

from porc.util import Q

COLLECTION_STATS = 'til_stats'
COLLECTION_TIL = 'til_til'
COLLECTION_COMMENTS = 'til_comments'


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
        try:
            uid = self.getNextID()
            data = {'id': uid, 'nick': nick, 'text': text, 'comments': 0}
            response = self.client.put(COLLECTION_TIL, uid, data)
            response.raise_for_status()
            return True
        except:
            return False

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

    def get_til_total_comments(self, id):
        '''Returns total comment of a TIL
        Argument:
        id -- id of TIL object
        '''
        til = self.getTILbyID(id)
        return til['comments']

    def increment_comment_count(self, id):
        '''Increments comment count of a TIL
        Argument:
        id -- id of TIL object.
        Return:
        result -- Boolean result of the transaction.
        '''
        try:
            item = self.client.get(COLLECTION_TIL, id)
            item['comments'] += 1
            self.client.put(item.collection, item.key, item.json, item.ref)
            return True
        except:
            return False

    def decrement_comment_count(self, id):
        '''Decrement comment count of a TIL
        Argument:
        id -- id of TIL object.
        Return:
        result -- Boolean result of the transaction.
        '''
        try:
            item = self.client.get(COLLECTION_TIL, id)
            item['comments'] -= 1
            self.client.put(item.collection, item.key, item.json, item.ref)
            return True
        except:
            return False

    def get_comment(self, id):
        '''Returns a comment object
        Argument:
        id -- id of the comment (<til_id>-<comment_no>, eg: 58-1)
        '''
        comment = self.client.get(COLLECTION_COMMENTS, id)
        comment.raise_for_status()
        return comment.json

    def get_all_comments(self, id):
        '''Returns all the comments of a given TIL id
        Argument:
        id -- TIL id
        '''
        query = Q('tilId', id)
        pages = self.client.search(COLLECTION_COMMENTS, query)
        return pages

    def save_comment(self, id, comment, nick, time):
        '''Saves comment in the database.
        Arguments:
        id      -- id of the TIL
        comment -- comment text
        nick    -- nick of the commenting user
        time    -- time when the comment is made
        '''
        id = int(id)
        try:
            data = {'tilId': id, 'comment': comment,
                    'nick': nick, 'time': time}
            comment_index = self.get_til_total_comments(id)
            comment_key = "%d-%d" % (id, comment_index+1)
            self.client.put(COLLECTION_COMMENTS,
                            comment_key, data).raise_for_status()
            self.increment_comment_count(id)
            return True
        except:
            return False
