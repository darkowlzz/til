from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from src.dbHelper.dbHelper import DBHelper
from src.apikeys import ORCHESTRATE_KEY


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    db = DBHelper(ORCHESTRATE_KEY)

    @app.route('/')
    def home():
        return render_template('home/home.html')

    @app.route('/today')
    def today():
        pages = db.getRecentTIL()
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
            if request.form['til'] is "":  # improve me
                return render_template('submit/tilForm.html')
            else:
                til_text = request.form['til']
            if request.form['nick'] is "":
                til_nick = 'anon'
            else:
                til_nick = request.form['nick']
            db.saveTIL(til_text, til_nick)
            return render_template('submit/submitted.html',
                                   text=til_text)
        else:
            return render_template('submit/tilForm.html')

    @app.route('/about')
    def about():
        return render_template('about/about.html')

    return app

app = create_app()

if __name__ == '__main__':
    create_app().run(debug=True)
