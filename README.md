# Annotaria
Annotaria is a lightweight and modular platform for data collection and annotation, designed to streamline the creation of datasets for training artificial intelligence models. It supports image inputs, interactive region selection, and multiple-choice questions, with database storage and a fully customizable interface.

# AIRFARM

**AIRFARM** è un'applicazione web per la raccolta e annotazione di dati da immagini, finalizzata alla creazione di dataset per l'addestramento di reti neurali.

---

## 📖 Panoramica del progetto

- Supporta immagini **JPG, TIFF, RAW**, anche provenienti da **droni**.
- Estrazione e salvataggio completo dei **metadati EXIF**.
- Caricamento e visualizzazione delle immagini da una **directory configurabile**.
- **Domande a scelta multipla**, comuni a tutte le immagini.
- **Annotazione interattiva**: l’utente seleziona un’area dell’immagine e assegna una **label**.
- **Salvataggio** delle risposte e annotazioni in un **database relazionale**.
- Obiettivo finale: dataset per **addestramento supervisionato** di modelli ML.

---

## 🛠️ Tecnologie utilizzate

- **Python 3.10+**
- **FastAPI** (API REST)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (o SQLite)
- **JavaScript + HTML5 Canvas (Fabric.js)** per annotazioni
- **Docker** (opzionale)

---

## 📂 Struttura del progetto

```
airfarm/
│
├── main.py                  # FastAPI app principale
├── database.py              # Connessione al database
├── models.py                # Modelli SQLAlchemy
├── schemas/                 # Modelli Pydantic
├── static/                  # JS/CSS
├── templates/               # HTML
├── image_data/              # Immagini da annotare
└── data/questions.json      # Dataset di domande iniziali (opzionale)
```

---

## 🗃️ Schema del database

Vedi il file [airfarm_database_structure.md](./airfarm_database_structure.md) per i dettagli completi delle tabelle.

---

## 🚀 API REST principali

| Metodo | Endpoint                            | Descrizione                                      |
|--------|-------------------------------------|--------------------------------------------------|
| GET    | `/images`                           | Restituisce le immagini e sincronizza la cartella |
| POST   | `/questions/`                       | Crea una nuova domanda                          |
| GET    | `/questions/`                       | Elenca tutte le domande                         |
| POST   | `/questions/{id}/options/`          | Aggiunge un’opzione a una domanda               |
| GET    | `/questions/{id}/options/`          | Elenca le opzioni di una domanda                |
| POST   | `/answers/`                         | Salva la risposta dell’utente                   |
| POST   | `/annotations/`                     | Salva un’annotazione grafica                    |

---

## ▶️ Avvio rapido

1. Crea `.env` con:

```dotenv
DATABASE_URL=postgresql://user:password@localhost:5432/airfarm
IMAGE_DIR=./image_data
```

2. Avvia il server:

```bash
uvicorn main:app --reload
```

3. Visita [http://localhost:8000/docs](http://localhost:8000/docs) per testare le API.

---

## 🧪 Esempio di risposta

```json
{
  "image_id": 1,
  "question_id": 2,
  "selected_option_id": 8,
  "answered_at": "2025-08-01T12:34:56"
}
```

---

## 📈 Sviluppi futuri

- CRUD amministrativo (immagini, domande, risposte, annotazioni)
- Interfaccia Streamlit o React frontend
- Versioning immagini e annotazioni
- Esportazione CSV/JSON per modelli ML
- Docker + docker-compose

---

## 📝 Licenza

Progetto open source sotto licenza MIT.

---