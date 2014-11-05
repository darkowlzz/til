from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home/home.html')

@app.route('/today')
def today():
    return render_template('today/today.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return render_template('submit/submitted.html', text=request.form['til'])
    else:
        return render_template('submit/tilForm.html')

@app.route('/about')
def about():
    return render_template('about/about.html')

if __name__ == '__main__':
    app.run(debug=True)
