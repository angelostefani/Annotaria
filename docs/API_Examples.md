# Esempi di Chiamate API – Annotaria

Questa guida fornisce esempi pratici di richieste alle API REST del progetto Annotaria.

> Tutti gli esempi usano `http://localhost:9100` come base URL.
> Le richieste che richiedono autenticazione usano la variabile `TOKEN` — sostituirla con il token JWT ottenuto dal login.

______________________________________________________________________

## Autenticazione

### Registrazione utente

```bash
curl -X POST http://localhost:9100/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "segreta123"}'
```

### Login e recupero token

```bash
curl -X POST http://localhost:9100/token \
  -d "username=alice&password=segreta123"
```

Salvare l'`access_token` dalla risposta come variabile d'ambiente:

```bash
TOKEN="<access_token_qui>"
```

### Profilo utente corrente

```bash
curl http://localhost:9100/users/me \
  -H "Authorization: Bearer $TOKEN"
```

### Cambio password

```bash
curl -X POST http://localhost:9100/users/me/password \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_password": "segreta123", "new_password": "nuova1234", "new_password_confirm": "nuova1234"}'
```

______________________________________________________________________

## Immagini

### Elenco immagini

```bash
curl http://localhost:9100/images \
  -H "Authorization: Bearer $TOKEN"
```

### Upload singolo

```bash
curl -X POST http://localhost:9100/images/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/percorso/della/immagine.jpg" \
  -F "image_type_id=1"
```

### Import massivo da directory

```bash
curl -X POST http://localhost:9100/images/import-directory \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"directory": "campagna_luglio", "image_type_id": 1, "recursive": true}'
```

### Dettaglio immagine

```bash
curl http://localhost:9100/images/1
```

### Modifica immagine

```bash
curl -X PUT http://localhost:9100/images/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filename": "nuovo.jpg", "image_type_id": 2}'
```

### Eliminazione immagine

```bash
curl -X DELETE http://localhost:9100/images/1 \
  -H "Authorization: Bearer $TOKEN"
```

______________________________________________________________________

## Tipologie immagine

### Elenco tipologie

```bash
curl http://localhost:9100/image-types/
```

### Creazione tipologia

```bash
curl -X POST http://localhost:9100/image-types/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Termica"}'
```

______________________________________________________________________

## Tipologie esperto

### Elenco tipologie esperto

```bash
curl http://localhost:9100/expert-types/
```

### Creazione tipologia esperto

```bash
curl -X POST http://localhost:9100/expert-types/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Agronomo", "image_type_ids": [1]}'
```

______________________________________________________________________

## Etichette

### Elenco etichette

```bash
curl http://localhost:9100/labels/
```

### Creazione etichetta

```bash
curl -X POST http://localhost:9100/labels/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Anomalia", "image_type_ids": [1]}'
```

### Modifica etichetta

```bash
curl -X PUT http://localhost:9100/labels/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Anomalia grave", "image_type_ids": [1, 2]}'
```

### Eliminazione etichetta

```bash
curl -X DELETE http://localhost:9100/labels/1 \
  -H "Authorization: Bearer $TOKEN"
```

______________________________________________________________________

## Domande e opzioni

### Elenco domande

```bash
curl http://localhost:9100/questions/
```

### Creazione domanda

```bash
curl -X POST http://localhost:9100/questions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question_text": "Qual è la condizione del raccolto?", "image_type_ids": [1]}'
```

### Modifica domanda

```bash
curl -X PUT http://localhost:9100/questions/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question_text": "Valuta la condizione del raccolto", "image_type_ids": [1]}'
```

### Eliminazione domanda

```bash
curl -X DELETE http://localhost:9100/questions/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Elenco opzioni di una domanda

```bash
curl http://localhost:9100/questions/1/options
```

### Aggiunta opzione (con logica follow-up)

```bash
curl -X POST http://localhost:9100/questions/1/options \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"option_text": "Secco", "follow_up_question_ids": [2]}'
```

### Modifica opzione

```bash
curl -X PUT http://localhost:9100/options/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"option_text": "Molto secco", "follow_up_question_ids": [2, 3]}'
```

### Eliminazione opzione

```bash
curl -X DELETE http://localhost:9100/options/1 \
  -H "Authorization: Bearer $TOKEN"
```

______________________________________________________________________

## Risposte

### Invio risposta (con upsert)

Se l'utente ha già risposto alla stessa domanda per la stessa immagine, la risposta viene aggiornata.

```bash
curl -X POST http://localhost:9100/answers/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": 1,
    "question_id": 1,
    "selected_option_id": 2
  }'
```

### Elenco risposte per immagine

```bash
curl http://localhost:9100/answers/1 \
  -H "Authorization: Bearer $TOKEN"
```

______________________________________________________________________

## Annotazioni

### Creazione annotazione (poligono)

```bash
curl -X POST http://localhost:9100/annotations/ \
  -H "Authorization: Bearer $TOKEN" \
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

### Elenco annotazioni per immagine

```bash
curl http://localhost:9100/annotations/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Modifica annotazione

```bash
curl -X PUT http://localhost:9100/annotations/14 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"label_id": 3}'
```

### Eliminazione annotazione

```bash
curl -X DELETE http://localhost:9100/annotations/14
```

______________________________________________________________________

> Assicurarsi che l'API sia in esecuzione su `localhost:9100` prima di eseguire gli esempi.
> La documentazione interattiva (Swagger UI) è disponibile su `http://localhost:9100/docs`.
