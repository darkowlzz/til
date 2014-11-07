from flask import Flask, render_template, request
from src.dbHelper.dbHelper import DBHelper
from src.apikeys import ORCHESTRATE_KEY


def create_app():
    app = Flask(__name__)
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
            db.saveTIL(request.form['til'], 'anon')
            return render_template('submit/submitted.html',
                                   text=request.form['til'])
        else:
            return render_template('submit/tilForm.html')

    @app.route('/about')
    def about():
        return render_template('about/about.html')

    return app

app = create_app()

if __name__ == '__main__':
    create_app().run(debug=True)
