import os

from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import TextAreaField, TextField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha import RecaptchaField
from flask_bootstrap import Bootstrap
from src.dbHelper.dbHelper import DBHelper
from pokemonNames.pokemonNames import PokemonNames

DEBUG = os.environ.get('DEBUG', '-1')
SECRET_KEY = os.environ.get('SECRET_KEY', '-1')

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '-1')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '-1')


class TILForm(Form):

    tilText = TextAreaField('TIL', validators=[DataRequired()])
    tilNick = TextField('@')
    test = eval(os.environ.get('TEST', '-1'))
    if not test:
        recaptcha = RecaptchaField()


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    Bootstrap(app)
    db = DBHelper(os.environ.get('ORCHESTRATE_KEY', '-1'))
    randName = PokemonNames()

    @app.route('/')
    def home():
        return render_template('home/home.html')

    @app.route('/til/<id>')
    def til(id):
        result = db.getTILbyID(int(id))
        return render_template('til/til.html', data=result)

    @app.route('/today')
    def today():
        pages = db.getRecentTIL()
        page = pages.next()
        results = page['results']
        return render_template('today/today.html', data=results, page=2)

    @app.route('/today/<pageno>')
    def today_more(pageno):
        pageno = int(pageno)
        nextpage = pageno + 1
        pages = db.getRecentTIL()
        try:
            for i in range(pageno):
                page = pages.next()
        except StopIteration:
            return render_template('today/nomore.html', page=nextpage)
        results = page['results']
        return render_template('today/today.html', data=results, page=nextpage)

    @app.route('/nomore')
    def nomore():
        return render_template('today/nomore.html')

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
            return render_template('submit/tilForm.html', form=form)

    @app.route('/about')
    def about():
        return render_template('about/about.html')

    return app


app = create_app()

if __name__ == '__main__':
    create_app().run()
