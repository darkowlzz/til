from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import TextAreaField, TextField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha import RecaptchaField
from flask_bootstrap import Bootstrap
from src.dbHelper.dbHelper import DBHelper
from src.apikeys import ORCHESTRATE_KEY
from pokemonNames.pokemonNames import PokemonNames


DEBUG = True
SECRET_KEY = 'secret'

RECAPTCHA_PUBLIC_KEY = '6Lf7jP0SAAAAAKDw2YOCMgkwbXfNO3-SG2yf1cTH'
RECAPTCHA_PRIVATE_KEY = '6Lf7jP0SAAAAAKHYkfIMAGQSMMV_FNnpIeolOM0K'


class TILForm(Form):

    tilText = TextAreaField('TIL', validators=[DataRequired()])
    tilNick = TextField('@')
    test = DEBUG
    if not test:
        recaptcha = RecaptchaField()


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    Bootstrap(app)
    db = DBHelper(ORCHESTRATE_KEY)
    randName = PokemonNames()

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
    def submit(form=None):
        if request.method == 'POST':
            form = TILForm()
            if form.validate_on_submit():
                til_text = request.form['tilText']
                if request.form['tilNick'] == '':
                    til_nick = 'Anonymous ' + randName.get_random_name()
                else:
                    til_nick = request.form['tilNick']
                db.saveTIL(til_text, til_nick)
                flash('TIL shared successfully!')
                return redirect(url_for("today"))
            else:
                return render_template('submit/tilForm.html', form=form)
        else:
            if form is None:
                form = TILForm()
            return render_template('submit/tilForm.html',
                                   form=form)

    @app.route('/about')
    def about():
        return render_template('about/about.html')

    return app


app = create_app()

if __name__ == '__main__':
    create_app().run()
