import pymongo
import json
from bson import ObjectId

# Configura la connessione al database MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['eventi']

# Collezioni
eventi_collection = db['eventi']
artisti_collection = db['artisti']
condotto_collection = db['condotto']
partecipanti_collection = db['partecipanti']
partecipa_collection = db['partecipa']

# Funzione per caricare i dati da un file JSON
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Carica i dati dai file JSON
artisti_data = load_json_data('json/artista.json')
eventi_data = load_json_data('json/evento.json')
condotto_data = load_json_data('json/condotto.json')
partecipanti_data = load_json_data('json/partecipante.json')
partecipa_data = load_json_data('json/partecipa.json')

# Elimina eventuali dati esistenti nelle collezioni
artisti_collection.delete_many({})
eventi_collection.delete_many({})
condotto_collection.delete_many({})
partecipa_collection.delete_many({})
partecipanti_collection.delete_many({})

# Dizionario per mappare id_artista e id_user originale con ObjectId MongoDB
artisti_id_map = {}
partecipanti_id_map = {}

# Rimuovi gli attributi 'id_artista' e inserisci i dati degli artisti
for artista in artisti_data:
    original_id = artista['id_artista']
    del artista['id_artista']
    artisti_inserted_id = artisti_collection.insert_one(artista).inserted_id
    artisti_id_map[original_id] = artisti_inserted_id

# Rimuovi gli attributi 'id_user' e inserisci i dati dei partecipanti
for partecipante in partecipanti_data:
    original_id = partecipante['id_user']
    del partecipante['id_user']
    partecipante_inserted_id = partecipanti_collection.insert_one(partecipante).inserted_id
    partecipanti_id_map[original_id] = partecipante_inserted_id

# Inserisci gli eventi e aggiungi l'attributo 'artisti' a ciascun evento ed anche gli Object_id dei partecipanti
for evento in eventi_data:
    evento_id = evento['codice']
    del evento['codice']
    evento['artisti'] = []
    evento['partecipanti'] = []


    # Cerca i collegamenti condotto per questo evento
    for condotto in condotto_data:
        if condotto['evento_id'] == evento_id:
            artista_id = condotto['artista_id']
            # Aggiungi l'artista all'evento
            if artista_id in artisti_id_map:
                artista_mongo_id = artisti_id_map[artista_id]
                artista = artisti_collection.find_one({'_id': artista_mongo_id})
                if artista:
                    artista['_id'] = artista_mongo_id
                    evento['artisti'].append(artista)
                    
    # Cerca i collegamenti partecipa per questo evento
    for partecipa in partecipa_data:
        if partecipa['evento_id'] == evento_id:
            partecipante_id = partecipa['partecipante_id']
            # Aggiungi l'ObjectId del partecipante all'evento
            if partecipante_id in partecipanti_id_map:
                partecipante_mongo_id = partecipanti_id_map[partecipante_id]
                evento['partecipanti'].append(partecipante_mongo_id)
                
    # Inserisci l'evento nella collezione degli eventi
    eventi_collection.insert_one(evento)

print("Importazione completata con successo!")
