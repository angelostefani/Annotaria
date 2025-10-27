# Annotaria

Annotaria è un'applicazione web per la raccolta e l'annotazione di dati da immagini, pensata per generare dataset strutturati utili all'addestramento di modelli di machine learning.

______________________________________________________________________

## Panoramica

- Supporto a immagini **JPG, TIFF, RAW**, anche provenienti da droni.
- Estrazione e salvataggio automatico dei metadati **EXIF**.
- Visualizzazione immagini da una cartella configurabile.
- Questionari a scelta multipla condivisi tra tutte le immagini.
- Annotazioni grafiche con bounding box e label associata.
- Persistenza di risposte e annotazioni su database relazionale.
- Gestione tipologie di immagine e ruoli degli esperti tramite endpoint dedicati.
- Accesso autenticato tramite token **JWT**.

______________________________________________________________________

## Documentazione

- [API REST](./docs/API_REST.md)
- [Struttura del Database](./docs/Database_Structure.md)
- [Esempi JSON e Test](./docs/API_Examples.md) *(opzionale)*
- [Setup e Configurazione](./docs/Setup.md)

______________________________________________________________________

## Tecnologie

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL** o **SQLite**
- **HTML + JavaScript (Canvas/Fabric.js)**
- **Docker** (opzionale, consigliato in produzione)

______________________________________________________________________

## Installazione e Avvio

### Docker

```bash installazione
docker compose build --no-cache
```
```bash avvio
docker compose up -d
```

### Ambiente Virtuale (venv)

1. Posizionati nella cartella del progetto.
2. Crea l'ambiente virtuale:
   - Linux/macOS: `python3.12 -m venv venv`
   - Windows: `python -m venv venv`
3. Attiva l'ambiente virtuale:
   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Installa le dipendenze: `pip install -r requirements.txt`
5. Avvia il server FastAPI scegliendo una porta libera:
   - Avvio semplice: `uvicorn main:app --host 0.0.0.0 --port 9100`
   - Avvio in background (Linux/macOS): `nohup uvicorn main:app --host 0.0.0.0 --port 9100 > annotaria.log 2>&1 &`

______________________________________________________________________

## Credenziali Predefinite

- Utente amministratore disponibile al primo avvio: `admin` / `admin`. Cambiare la password dopo l'accesso.
- Gli utenti creati tramite interfaccia vengono assegnati al ruolo **Esperto**.

______________________________________________________________________

## Struttura del Progetto

```
annotaria/
├── main.py                  # Entrypoint FastAPI
├── database.py              # Configurazione SQLAlchemy
├── models.py                # Definizione modelli database
├── routers/                 # Router FastAPI
├── schemas/                 # Modelli Pydantic
├── static/                  # Asset JS/CSS
├── templates/               # Template HTML
├── image_data/              # Archivio immagini configurabile
├── docs/                    # Documentazione aggiuntiva
└── .env                     # Configurazione ambiente
```

______________________________________________________________________

## Licenza

Progetto open source distribuito sotto licenza MIT.

______________________________________________________________________
