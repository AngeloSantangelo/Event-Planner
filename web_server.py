from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

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

@app.route('/add_event', methods=['POST'])
def add_event():
    eventi = mongo.db.eventi
    tema = request.form.get('tema')
    data = request.form.get('data')
    prezzo_biglietto = request.form.get('prezzo_biglietto')
    nome_locale = request.form.get('nome_locale')
    artisti_data = request.form.getlist('artisti')
    try:
        # Converting date from GG/MM/AAAA to datetime object
        data = datetime.strptime(data, '%d/%m/%Y').strftime('%d/%m/%Y')
    except ValueError:
        return "Invalid date format. Please use GG/MM/AAAA."
    artisti_details = []
    for artista in artisti_data:
        artista_id, nome_arte, tipo, telefono, prezzo_artista = artista.split('|')
        artisti_details.append({
            '_id': ObjectId(artista_id),
            'nome_arte': nome_arte,
            'tipo': tipo,
            'telefono': telefono,
            'prezzo_artista': int(prezzo_artista)
        })
    evento = {
        'tema': tema,
        'data': data,
        'prezzo_biglietto': prezzo_biglietto,
        'nome_locale': nome_locale,
        'artisti': artisti_details
    }
    eventi.insert_one(evento)
    return render_template('index.html')

@app.route('/query2')
def query2():
    artisti = mongo.db.artisti.find()
    return render_template('query2.html', artisti=artisti)

@app.route('/query3')
def query3():
    eventi = mongo.db.eventi.find()
    risultati = []
    for evento in eventi:
        tema = evento['tema']
        data = evento['data']
        nome_locale = evento['nome_locale']
        prezzo_biglietto = evento['prezzo_biglietto']
        costo_totale_artisti = sum(float(artista['prezzo_artista']) for artista in evento['artisti'])
        risultati.append({
            'tema': tema,
            'data': data,
            'nome_locale': nome_locale,
            'prezzo_biglietto': prezzo_biglietto,
            'costo_totale_artisti': costo_totale_artisti
        })
    return render_template('query3.html', eventi=risultati)

@app.route('/query4')
def query4():
    eventi = mongo.db.eventi.find()
    
    risultati = []
    for evento in eventi:
        numero_partecipanti = len(evento.get('partecipanti', []))
        incasso_totale = numero_partecipanti * evento['prezzo_biglietto']
        evento['numero_partecipanti'] = numero_partecipanti
        evento['incasso_totale'] = incasso_totale
        risultati.append(evento)

    return render_template('query4.html', eventi=risultati)


@app.route('/query10')
def query10():
    eventi = mongo.db.eventi.find()
    risultati = []
    for evento in eventi:
        numero_partecipanti = len(evento.get('partecipanti', []))
        prezzo_biglietto = float(evento['prezzo_biglietto'])
        incasso_totale = prezzo_biglietto * numero_partecipanti
        costo_totale_artisti = sum(float(artista['prezzo_artista']) for artista in evento['artisti'])
        guadagno_veritiero = incasso_totale - costo_totale_artisti
        
        evento['numero_partecipanti'] = numero_partecipanti
        evento['incasso_totale'] = incasso_totale
        evento['costo_totale_artisti'] = costo_totale_artisti
        evento['guadagno_veritiero'] = guadagno_veritiero
        
        risultati.append(evento)
    return render_template('query10.html', eventi=risultati)




if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
