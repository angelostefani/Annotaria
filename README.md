# Annotaria

**Annotaria** è un'applicazione web in Python per la raccolta e annotazione di dati da immagini, finalizzata alla creazione di dataset strutturati per l'addestramento di reti neurali.

______________________________________________________________________

## 📖 Panoramica

- Supporta immagini **JPG, TIFF, RAW**, anche da **droni**.
- Estrae e salva automaticamente i **metadati EXIF**.
- Visualizza immagini da una **directory configurabile**.
- Presenta domande a **scelta multipla**, comuni a tutte le immagini.
- Permette annotazioni grafiche (bounding box) con **label associata**.
- Salva risposte e annotazioni in un **database relazionale**.
- Gestisce **tipologie di immagine** e ruoli degli esperti tramite endpoint dedicati.
- Accesso autenticato tramite token **JWT**.

______________________________________________________________________

## 🧱 Struttura dei file di documentazione

- [📂 API REST](./docs/API_REST.md)
- [🗃️ Struttura del Database](./docs/Database_Structure.md)
- [🧪 Esempi JSON e Test](./docs/API_Examples.md) *(opzionale)*
- [🧰 Configurazione e Ambiente](./docs/Setup.md) *(opzionale)*

______________________________________________________________________

## 🛠️ Tecnologie utilizzate

- **Python 3.10+**
- **FastAPI** per le API REST
- **SQLAlchemy** (ORM)
- **PostgreSQL** o **SQLite**
- **HTML + JavaScript (Canvas/Fabric.js)** per annotazioni grafiche
- **Docker** (opzionale, per ambienti isolati)

______________________________________________________________________

## ▶️ Avvio rapido

1. Crea un file `.env`:

```dotenv
DATABASE_URL=postgresql://user:password@localhost:5432/annotaria
IMAGE_DIR=./image_data
```

2. Avvia l'applicazione:

```bash
uvicorn main:app --reload
```

nohup python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8001 > uvicorn.log 2>&1 &

3. Visita: [http://localhost:8000/docs](http://localhost:8000/docs)

______________________________________________________________________

## 🐳 Docker

- Build immagine: `docker build -t annotaria .`
- Esecuzione (SQLite): `docker run --rm -p 8000:8000 --env-file .env -v "$PWD/image_data:/app/image_data" annotaria`
- docker compose (PostgreSQL): `docker compose up --build`

Nota: dettagli e file inclusi (`Dockerfile`, `docker-compose.yml`) in AGENTS.md, sezione “Docker & Containers”.

______________________________________________________________________

## 📁 Struttura del progetto

```
annotaria/
│
├── main.py                  # Entrypoint FastAPI
├── database.py              # Configurazione SQLAlchemy
├── models.py                # Definizione modelli database
├── schemas/                 # Modelli Pydantic per le API
├── static/                  # JS e CSS
├── templates/               # Template HTML (opzionale)
├── image_data/              # Cartella immagini configurabile
├── data/questions.json      # Dataset domande iniziali
└── docs/                    # Documentazione Markdown
    ├── API_REST.md
    ├── Database_Structure.md
    └── Setup.md
```

______________________________________________________________________

Per creare un’annotazione poligonale:

Aggiunta dei vertici – ogni singolo click sul canvas aggiunge un punto alla forma in costruzione

Chiusura del poligono – un doppio click chiude il poligono:

se sono stati inseriti meno di tre punti, i vertici vengono scartati;

altrimenti compare una finestra di dialogo che elenca le label disponibili e consente di scegliere l’etichetta da associare

In pratica, continua a cliccare per aggiungere vertici e, quando hai terminato, fai un doppio click: si aprirà il prompt in cui inserire (o selezionare) la label, completando così l’annotazione.
______________________________________________________________________

## 📈 Sviluppi futuri

- Interfaccia amministrativa CRUD per immagini, domande, annotazioni
- Versionamento immagini/annotazioni
- Interfaccia Streamlit o frontend React
- Esportazione dati per ML (CSV/JSON)
- Container Docker (Dockerfile + docker-compose)

______________________________________________________________________

## 📝 Licenza

Progetto open source sotto licenza MIT.

______________________________________________________________________
