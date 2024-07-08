# Event-Planner
Sistema ideato per un gruppo di organizzatori di eventi pubbilici ed è stato realizzato come progetto universitario per il corso di Basi di Dati II del dipartimento di Informatica persso l'Università degli Studi di Salerno.
## Descrizione
Tale progetto è un'applicazione web per gestire eventi, inclusa la creazione, la visualizzazione e la ricerca di eventi. Gli organizzatori possono inserire nuovi eventi, vedere i dettagli degli eventi esistenti, e eseguire diverse query sui dati esistenti.

## Requisiti
- [MongoDB-Compass](https://www.mongodb.com/docs/compass/current/install/).
- [Python(versione 3.12.4](https://www.python.org/downloads/) con libreria [PyMongo](https://pypi.org/project/pymongo/).
- [Flask](https://pypi.org/project/Flask/).

## Descrizione delle Cartelle
- La cartella **json** contiene i dati fittizi generati con il tool [Mockaroo](https://www.mockaroo.com/), in particolare attraverso file con estensione .json;
- Il file **db_load.py** rappresenta lo script Python che legge i file json e importa automaticamente tutti i dati in MongoDB Compass;
- La cartella **templates** contiene i vari file HTML realizzati per la visualizzazione e l'inserimento di dati al fine di effettuare il rendering delle query response;
- Il file **web_server.py** rappresente il Web Server con la definizione delle API per interagire con MongoDB e con il Front-End;

## Configurazione dell'infrastruttura MongoDB
Per automatizzare la procedura di importazione dei dati in MongoDB, bisogna eseguire il file **db_load.py** tramite il seguente comando:
```bash

python db_load.py

```
Tuttavia, si assume che già sia stato creato il database "evento" su MongoDB Compass.
Per visualizzare a schermo il sistema web, bisogna eseguire il file **web_server.py** tramite il seguente comando:
```bash

python web_server.py

```
