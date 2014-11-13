import os

from src.main import create_app

os.environ['ORCHESTRATE_KEY'] = '1de49651-92d0-4f7c-ae0b-ee92506a55f4'
os.environ['RECAPTCHA_PUBLIC_KEY'] = '6Lf7jP0SAAAAAKDw2YOCMgkwbXfNO3-SG2yf1cTH'
os.environ['RECAPTCHA_PRIVATE_KEY'] = \
    '6Lf7jP0SAAAAAKHYkfIMAGQSMMV_FNnpIeolOM0K'
os.environ['SECRET_KEY'] = 'tilsecret'
os.environ['TEST'] = 'False'
os.environ['DEBUG'] = 'True'

# Create a test client
app = create_app().test_client()


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
    assert 'Share your TIL' in rv.data


def test_submit_post():
    '''test /submit (POST)'''
    rv = app.post('/submit', data=dict(
        til='learnt flask',
        nick='nosetest',
    ), follow_redirects=True)
    assert 'TIL shared successfully!' not in rv.data


def test_about():
    '''testing /about'''
    rv = app.get('/about')
    assert 'About TIL' in rv.data
