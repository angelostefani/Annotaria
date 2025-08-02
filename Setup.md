# ⚙️ Setup del Progetto Annotaria

---

## Prerequisiti

- Python >= 3.10
- PostgreSQL (o SQLite)
- pip
- (Opzionale) Docker e docker-compose

---

## 📁 Struttura directory suggerita

```
annotaria/
├── .env
├── image_data/
├── main.py
├── database.py
├── models.py
├── static/
├── templates/
├── schemas/
└── docs/
```

---

## 🔧 Configurazione

Crea un file `.env` con:

```dotenv
DATABASE_URL=postgresql://utente:password@localhost:5432/annotaria
IMAGE_DIR=./image_data
```

---

## 🚀 Avvio

1. Crea le tabelle (automaticamente alla partenza)
2. Avvia il server:

```bash
uvicorn main:app --reload
```

3. Documentazione API:

[http://localhost:8000/docs](http://localhost:8000/docs)