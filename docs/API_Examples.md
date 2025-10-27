# 🧪 Esempi di Chiamate API – Annotaria

Questa guida fornisce esempi pratici di richieste alle API REST del progetto Annotaria.

______________________________________________________________________

## 📷 Recupero immagini

### `GET /images`

```bash
curl http://localhost:9100/images
```

### `POST /images/upload`

```bash
curl -X POST http://localhost:9100/images/upload \
  -F "file=@/percorso/della/immagine.jpg" \
  -F "image_type_id=1"
```

### `GET /images/1`

```bash
curl http://localhost:9100/images/1
```

### `PUT /images/1`

```bash
curl -X PUT http://localhost:9100/images/1 \
  -H "Content-Type: application/json" \
  -d '{"filename": "nuovo.jpg"}'
```

### `DELETE /images/1`

```bash
curl -X DELETE http://localhost:9100/images/1
```

______________________________________________________________________

## ➕ Creazione di una domanda

### `POST /questions/`

```bash
curl -X POST http://localhost:9100/questions/ \
  -H "Content-Type: application/json" \
  -d '{"question_text": "Qual è la condizione del raccolto?"}'
```

______________________________________________________________________

## ➕ Aggiunta di opzioni a una domanda

### `POST /questions/1/options`

```bash
curl -X POST http://localhost:9100/questions/1/options \
  -H "Content-Type: application/json" \
  -d '{"option_text": "Secco"}'
```

______________________________________________________________________

## 📝 Invio di una risposta

### `POST /answers/`

```bash
curl -X POST http://localhost:9100/answers/ \
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
curl -X POST http://localhost:9100/annotations/ \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": 1,
    "label_id": 2,
    "points": [
      {"x": 120.5, "y": 88.0},
      {"x": 160.5, "y": 90.0},
      {"x": 150.0, "y": 120.0}
    ]
  }'
```

______________________________________________________________________

## ✅ Visualizzazione domande e opzioni

### `GET /questions/`

```bash
curl http://localhost:9100/questions/
```

### `GET /questions/1/options`

```bash
curl http://localhost:9100/questions/1/options
```

______________________________________________________________________

## 🏷️ Tipologie di immagine

### `GET /image-types`

```bash
curl http://localhost:9100/image-types/
```

### `POST /image-types`

```bash
curl -X POST http://localhost:9100/image-types/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Termica"}'
```

______________________________________________________________________

> 🔧 Tutte le richieste usano `Content-Type: application/json`.
> Assicurati che l'API sia in esecuzione su `localhost:9100`.
