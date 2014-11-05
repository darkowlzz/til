import sys
sys.path.append('../src')
import hello

app = hello.app.test_client()

def test_hello():
    """testing /"""
    rv = app.get('/')
    assert 'Hello World' in rv.data
