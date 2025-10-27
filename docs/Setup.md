# Setup del Progetto Annotaria

______________________________________________________________________

## Prerequisiti

- Python >= 3.12
- pip
- PostgreSQL (o SQLite)
- Docker e Docker Compose (opzionali, consigliati per il deploy)

______________________________________________________________________

## Installazione e Avvio con Docker

```bash
docker compose build --no-cache
docker compose up -d
```

______________________________________________________________________

## Installazione e Avvio con Ambiente Virtuale (venv)

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
   - Avvio in background (Linux/macOS):<br>`nohup uvicorn main:app --host 0.0.0.0 --port 9100 > annotaria.log 2>&1 &`

______________________________________________________________________

## Credenziali Predefinite

- Utente amministratore preconfigurato: `admin` / `changeme` (cambiare la password al primo accesso).
- Gli utenti creati tramite interfaccia avranno ruolo **Esperto**.

______________________________________________________________________

## Risorse Utili

- Documentazione API: [http://localhost:9100/docs](http://localhost:9100/docs)
- Interfaccia Web: [http://localhost:9100/ui](http://localhost:9100/ui)
