# 🧪 Esempi di Chiamate API – Annotaria

Questa guida fornisce esempi pratici di richieste alle API REST del progetto Annotaria.

______________________________________________________________________

## 📷 Recupero immagini

### `GET /images`

```bash
curl http://localhost:8000/images
```

### `POST /images/upload`

```bash
curl -X POST http://localhost:8000/images/upload \
  -F "file=@/percorso/della/immagine.jpg"
```

### `GET /images/1`

```bash
curl http://localhost:8000/images/1
```

### `PUT /images/1`

```bash
curl -X PUT http://localhost:8000/images/1 \
  -H "Content-Type: application/json" \
  -d '{"filename": "nuovo.jpg"}'
```

### `DELETE /images/1`

```bash
curl -X DELETE http://localhost:8000/images/1
```

______________________________________________________________________

## ➕ Creazione di una domanda

### `POST /questions/`

```bash
curl -X POST http://localhost:8000/questions/ \
  -H "Content-Type: application/json" \
  -d '{"question_text": "Qual è la condizione del raccolto?"}'
```

______________________________________________________________________

## ➕ Aggiunta di opzioni a una domanda

### `POST /questions/1/options`

```bash
curl -X POST http://localhost:8000/questions/1/options \
  -H "Content-Type: application/json" \
  -d '{"option_text": "Secco"}'
```

______________________________________________________________________

## 📝 Invio di una risposta

### `POST /answers/`

```bash
curl -X POST http://localhost:8000/answers/ \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": 1,
    "question_id": 1,
    "selected_option_id": 2
}'
```

______________________________________________________________________

## 🖍️ Annotazione di una regione dell’immagine

### `POST /annotations/`

```bash
curl -X POST http://localhost:8000/annotations/ \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": 1,
    "label": "malattia fungina",
    "x": 120.5,
    "y": 88.0,
    "width": 40.0,
    "height": 60.0
}'
```

______________________________________________________________________

## ✅ Visualizzazione domande e opzioni

### `GET /questions/`

```bash
curl http://localhost:8000/questions/
```

### `GET /questions/1/options`

```bash
curl http://localhost:8000/questions/1/options
```

______________________________________________________________________

> 🔧 Tutte le richieste usano `Content-Type: application/json`.
> Assicurati che l'API sia in esecuzione su `localhost:8000`.
