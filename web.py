from flask import Flask, render_template, request, redirect, url_for
import numpy as np

from scraping import scraping_program, edit_program


app = Flask(__name__)

def picked_up():
    messages = [
        "こんにちは",
        "Hi!",
        "Hello world",
    ]
    return np.random.choice(messages)

@app.route('/')
def index():
    title = "ようこそ"
    message = picked_up()
    return render_template('index.html', message=message, title=title)

@app.route('/scraping', methods=['GET', 'POST'])
def scraping():
    year, month, day = scraping_program(request.form['date'])
    if not year:
        return redirect(url_for("index.html"))
    results = edit_program(month, day)
    return render_template('result.html', year=year, month=month, day=day, results=results)

@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        name = request.form['name']
        return render_template('index.html', name=name, title=title)

    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
