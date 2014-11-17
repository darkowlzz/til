import os
import datetime
import time

from flask import (Flask, render_template, request, flash,
                   redirect, url_for, send_from_directory)
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

    til_text = TextAreaField('TIL', validators=[DataRequired()])
    til_nick = TextField('@')
    test = eval(os.environ.get('TEST', '-1'))
    if not test:
        recaptcha = RecaptchaField()


class CommentForm(Form):

    comment_text = TextAreaField('Comment', validators=[DataRequired()])
    comment_nick = TextField('@')
    comment_til_id = TextField('TIL id', validators=[DataRequired()])


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
        result = db.get_til_by_id(int(id))
        try:
            result['time'] = stringify_time(result['time'])
        except:
            pass
        comments_pages = db.get_all_comments(int(id))
        comments_page = comments_pages.next()
        comments = comments_page['results']
        comments = format_results(comments)
        form = CommentForm()
        return render_template('til/til.html', data=result,
                               comments=comments, form=form)

    @app.route('/today')
    def today():
        pages = db.get_recent_til()
        page = pages.next()
        results = page['results']
        results = format_results(results)
        return render_template('today/today.html', data=results, page=2)

    @app.route('/today/<pageno>')
    def today_more(pageno):
        pageno = int(pageno)
        nextpage = pageno + 1
        pages = db.get_recent_til()
        try:
            for i in range(pageno):
                page = pages.next()
        except StopIteration:
            return render_template('today/nomore.html', page=nextpage)
        results = page['results']
        results = format_results(results)
        return render_template('today/today.html', data=results, page=nextpage)

    @app.route('/nomore')
    def nomore():
        return render_template('today/nomore.html')

    @app.route('/submit', methods=['GET', 'POST'])
    def submit(form=None):
        if request.method == 'POST':
            form = TILForm()
            if form.validate_on_submit():
                til_text = request.form['til_text']
                if request.form['til_nick'] == '':
                    til_nick = 'Anonymous ' + randName.get_random_name()
                else:
                    til_nick = request.form['til_nick']
                t = time.localtime()
                time_now = {'hour': t.tm_hour, 'minute': t.tm_min,
                            'second': t.tm_sec, 'year': t.tm_year,
                            'month': t.tm_mon, 'day': t.tm_mday}
                db.save_til(til_text, til_nick, time_now)
                flash('TIL shared successfully!')
                return redirect(url_for('today'))
            else:
                try:
                    if form.til_text.errors:
                        error = 'Error: TIL field is required.'
                        flash(error)
                except:
                    pass
                try:
                    if form.recaptcha.errors:
                        error = 'Error: Invalid word in reCaptcha.'
                        flash(error)
                except:
                    pass
                return render_template('submit/tilForm.html', form=form)
        else:
            if form is None:
                form = TILForm()
            return render_template('submit/tilForm.html', form=form)

    @app.route('/comment', methods=['POST'])
    def comment(form=None):
        if request.method == 'POST':
            form = CommentForm()
            if form.validate_on_submit():
                t = time.localtime()
                time_now = {'hour': t.tm_hour, 'minute': t.tm_min,
                            'second': t.tm_sec, 'year': t.tm_year,
                            'month': t.tm_mon, 'day': t.tm_mday}
                if request.form['comment_nick'] == '':
                    comment_nick = 'Anonymous ' + randName.get_random_name()
                else:
                    comment_nick = request.form['comment_nick']
                comment_text = request.form['comment_text']
                comment_til_id = request.form['comment_til_id']
                r = db.save_comment(comment_til_id, comment_text,
                                    comment_nick, time_now)
                if r:
                    flash('Comment saved!')
                else:
                    flash('Error: Comment failed to save')
                return redirect(request.referrer)
            else:
                flash('Error in comment form')
                return redirect(request.referrer)

    @app.route('/about')
    def about():
        return render_template('about/about.html')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path,
                                   'static', 'images'),
                                   'favicon.ico', mimetype='image/png')

    return app


def format_results(results):  # Write test after moving into a separate module.
    '''Format the results into easily usable form'''
    for index, item in enumerate(results):
        try:
            timeString = stringify_time(item['value']['time'])
            results[index]['value']['time'] = timeString
        except:
            pass
    return results


def stringify_time(dictTime):  # No test. Have to be converted to a package.
    '''Returns stringified time (Hour:Minute - Day Month Year)'''
    dataObj = datetime.date(year=dictTime['year'], month=dictTime['month'],
                            day=dictTime['day'])
    strDate = dataObj.strftime('%d %B %Y')
    timeObj = datetime.time(hour=dictTime['hour'], minute=dictTime['minute'])
    strTime = timeObj.strftime('%H:%M')
    strFullTime = "%s - %s" % (strTime, strDate)
    return strFullTime


app = create_app()

if __name__ == '__main__':
    create_app().run()
