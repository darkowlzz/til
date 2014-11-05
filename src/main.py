from flask import Flask, url_for, render_template, request
from dbHelper.dbHelper import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home/home.html')

@app.route('/today')
def today():
    pages = getRecentTIL()
    page = pages.next()
    results = page['results']
    results.reverse()
    return render_template('today/today.html', data=results)

@app.route('/today/<pageno>')
def today_more(pageno):
    pass

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        saveTIL(request.form['til'], 'anon')
        return render_template('submit/submitted.html', text=request.form['til'])
    else:
        return render_template('submit/tilForm.html')

@app.route('/about')
def about():
    return render_template('about/about.html')

if __name__ == '__main__':
    app.run(debug=True)
