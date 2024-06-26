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
    

@app.route('/query1')
def query1():
    eventi = mongo.db.eventi.find()
    return render_template('query1.html', eventi=eventi)

@app.route('/query2', methods=['GET', 'POST'])
def query2():
    if request.method == 'POST':
        eventi = mongo.db.eventi
        tema = request.form.get('tema')
        data = request.form.get('data')
        prezzo_biglietto = request.form.get('prezzo_biglietto')
        nome_locale = request.form.get('nome_locale')
        artisti_data = request.form.getlist('artisti')
        try:
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
    else:
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

@app.route('/query5', methods=['GET', 'POST'])
def query5():
    if request.method == 'POST':
        data_inizio = request.form['data_inizio']
        data_fine = request.form['data_fine']

        # Conversione delle date in oggetti datetime
        data_inizio_dt = datetime.strptime(data_inizio, '%d/%m/%Y')
        data_fine_dt = datetime.strptime(data_fine, '%d/%m/%Y')

        # Trovare gli eventi che si svolgono tra le date specificate
        eventi = []
        for evento in mongo.db.eventi.find():
            data_evento_str = evento.get('data', '')
            if data_evento_str:
                data_evento_dt = datetime.strptime(data_evento_str, '%d/%m/%Y')
                if data_inizio_dt <= data_evento_dt <= data_fine_dt:
                    eventi.append(evento)

        return render_template('query5.html', eventi=eventi, data_inizio=data_inizio, data_fine=data_fine)
    
    return render_template('query5_form.html')


@app.route('/query6', methods=['GET', 'POST'])
def query6():
    if request.method == 'POST':
        budget = float(request.form['prezzo'])

        # Trovare gli artisti che hanno un budget al di sotto di un determinato prezzo
        artisti = []
        for artista in mongo.db.artisti.find():
            prezzo_artista = float(artista.get('prezzo_artista', ''))
            if prezzo_artista <= budget:
                artisti.append(artista)
        return render_template('query6.html', artisti=artisti, budget=budget)
    return render_template('query6_form.html')


@app.route('/query9', methods=['GET', 'POST'])
def query9():
    if request.method == 'POST':
        locale = request.form['locale']

        # Trovare gli artisti che hanno un budget al di sotto di un determinato prezzo
        eventi = []
        for evento in mongo.db.eventi.find():
            nome_locale = evento.get('nome_locale', '')
            if locale == nome_locale:
                eventi.append(evento)
        return render_template('query9.html', eventi=eventi, locale=locale)
    return render_template('query9_form.html')

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
