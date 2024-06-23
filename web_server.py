from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'eventi'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/eventi'

mongo = PyMongo(app)

@app.route('/')
def index():
    return redirect(url_for('retrieve'))

@app.route('/retrieve')
def retrieve():
    partecipanti = mongo.db.partecipanti.find().limit(20)
    return render_template('sample.html', partecipanti=partecipanti)

if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
