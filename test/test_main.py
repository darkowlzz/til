import sys
sys.path.append('../src')
import main

app = main.app.test_client()


def test_home():
    '''testing /'''
    rv = app.get('/')
    assert 'A place to share your TIL' in rv.data


def test_today():
    '''testing /today'''
    rv = app.get('/today')
    assert 'What people have learnt' in rv.data


def test_submit_get():
    '''testing /submit (GET)'''
    rv = app.get('/submit')
    assert 'Enter your TIL' in rv.data


def test_submit_post():
    '''test /submit (POST)'''
    rv = app.post('/submit', data=dict(
        til='learnt flask'
    ), follow_redirects=True)
    assert 'Enter your TIL' not in rv.data
    assert 'Submitted TIL' in rv.data
    assert 'learnt flask' in rv.data


def test_about():
    '''testing /about'''
    rv = app.get('/about')
    assert 'About TIL' in rv.data
