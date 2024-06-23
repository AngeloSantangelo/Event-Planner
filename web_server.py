from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'eventi'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/eventi'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('index.html')
    

@app.route('/retrieveEventiWithArtisti')
def retrieveEventiWithArtisti():
    eventi = mongo.db.eventi.find()
    return render_template('query1.html', eventi=eventi)

if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
