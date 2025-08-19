# 📘 Documentazione API REST – AIRFARM

Tutte le API restituiscono e accettano dati in formato JSON.\
Prefisso base: `http://localhost:8000/`

______________________________________________________________________

## 👤 AUTENTICAZIONE

### `POST /users/`

Registra un nuovo utente. Il campo `role` è opzionale e di default è `"Esperto"`.

**Request Body**

```json
{
  "username": "alice",
  "password": "segreta",
  "role": "Esperto"
}
```

**Response 201 Created**

```json
{
  "id": 1,
  "username": "alice",
  "role": "Esperto"
}
```

### `POST /token`

Esegue il login e restituisce un token JWT da usare nelle richieste protette.

**Request Body** `application/x-www-form-urlencoded`

```
username=<username>&password=<password>
```

**Response 200 OK**

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Per le rotte che richiedono autenticazione inviare l'header:

`Authorization: Bearer <token>`

## 📁 IMMAGINI

### `GET /images`

Restituisce l’elenco delle immagini disponibili nella directory configurata e sincronizza il DB.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "filename": "immagine1.jpg",
    "url": "/static/immagine1.jpg",
    "exif_camera_model": "DJI Mavic Air 2",
    "exif_datetime": "2025-07-31 14:30:00",
    "image_type_id": 1
  }
]
```

### `POST /images/upload`

Carica una nuova immagine salvandola sul server ed estrae i metadati EXIF. È possibile specificare una Tipologia Immagine già esistente.

**Request** `multipart/form-data`

```
file=<binary>
image_type_id=1
```

**Response 201 Created**

```json
{
  "id": 2,
  "filename": "nuova.jpg",
  "path": "./image_data/nuova.jpg",
  "image_type_id": 1,
  "exif_camera_model": "DJI Mavic Air 2",
  "exif_datetime": "2025-07-31 14:30:00"
}
```

### `GET /images/{image_id}`

Restituisce i dettagli di una singola immagine.

**Response 200 OK**

```json
{
  "id": 1,
  "filename": "immagine1.jpg",
  "path": "./image_data/immagine1.jpg",
  "exif_camera_model": "DJI Mavic Air 2",
  "image_type": {
    "id": 1,
    "name": "Aerea"
  }
}
```

### `PUT /images/{image_id}`

Aggiorna i metadati di un’immagine esistente.

**Request Body**

```json
{
  "filename": "nuovo_nome.jpg",
  "image_type_id": 2
}
```

**Response 200 OK**

```json
{
  "id": 1,
  "filename": "nuovo_nome.jpg",
  "path": "./image_data/nuovo_nome.jpg",
  "image_type_id": 2
}
```

### `DELETE /images/{image_id}`

Rimuove un’immagine dal database e dal filesystem.

**Response 204 No Content**

______________________________________________________________________

## 🏷️ TIPOLOGIE IMMAGINE

### `GET /image-types/`

Elenca tutte le tipologie immagine disponibili.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "name": "Aerea"
  }
]
```

### `POST /image-types/`

Crea una nuova tipologia immagine.

**Request Body**

```json
{
  "name": "Termica"
}
```

**Response 201 Created**

```json
{
  "id": 2,
  "name": "Termica"
}
```

### `PUT /image-types/{type_id}`

Aggiorna il nome di una tipologia esistente.

**Request Body**

```json
{
  "name": "Multispettrale"
}
```

**Response 200 OK**

```json
{
  "id": 2,
  "name": "Multispettrale"
}
```

### `DELETE /image-types/{type_id}`

Elimina una tipologia immagine.

**Response 204 No Content**

______________________________________________________________________

## ❓ DOMANDE E OPZIONI

### `GET /questions/`

Elenca tutte le domande presenti nel sistema.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "question_text": "Qual è lo stato della pianta?"
  }
]
```

### `POST /questions/`

Crea una nuova domanda.

**Request Body**

```json
{
  "question_text": "La pianta è infestata?"
}
```

**Response 201 Created**

```json
{
  "id": 5,
  "question_text": "La pianta è infestata?"
}
```

### `GET /questions/{question_id}/options`

Restituisce tutte le opzioni associate a una domanda.

**Response 200 OK**

```json
[
  {
    "id": 10,
    "option_text": "Sì"
  },
  {
    "id": 11,
    "option_text": "No"
  }
]
```

### `POST /questions/{question_id}/options`

Aggiunge una nuova opzione a una domanda esistente.

**Request Body**

```json
{
  "option_text": "Non determinabile"
}
```

**Response 201 Created**

```json
{
  "id": 12,
  "question_id": 5,
  "option_text": "Non determinabile"
}
```

______________________________________________________________________

## 📝 RISPOSTE

Richiede autenticazione; l'utente associato viene determinato dal token presente nell'header `Authorization: Bearer <token>`.

### `POST /answers/`

Registra la risposta fornita per una determinata immagine e domanda. L'associazione all'utente è automatica e non va specificato `user_id` nel body.

**Request Body**

```json
{
  "image_id": 1,
  "question_id": 5,
  "selected_option_id": 12
}
```

**Response 201 Created**

```json
{
  "id": 33,
  "image_id": 1,
  "question_id": 5,
  "selected_option_id": 12,
  "answered_at": "2025-08-01T15:12:00"
}
```

______________________________________________________________________

## 🎯 ANNOTAZIONI

Richiede autenticazione; le annotazioni vengono collegate all'utente identificato dal token nell'header `Authorization`.

### `POST /annotations/`

Salva un’annotazione su un'immagine selezionata (poligono + label predefinita). `user_id` è gestito automaticamente.

**Request Body**

```json
{
  "image_id": 1,
  "label_id": 2,
  "points": [
    {"x": 120.5, "y": 80.2},
    {"x": 170.5, "y": 82.0},
    {"x": 160.0, "y": 120.0}
  ]
}
```

**Response 201 Created**

```json
{
  "id": 14,
  "image_id": 1,
  "label_id": 2,
  "label": {"id": 2, "name": "foglia danneggiata"},
  "points": [
    {"x": 120.5, "y": 80.2},
    {"x": 170.5, "y": 82.0},
    {"x": 160.0, "y": 120.0}
  ],
  "annotated_at": "2025-08-01T15:14:00"
}
```

### `GET /annotations/{image_id}`

Restituisce tutte le annotazioni dell'utente autenticato per una determinata immagine.

**Response 200 OK**

```json
[
  {
    "id": 14,
    "image_id": 1,
    "label_id": 2,
    "label": {"id": 2, "name": "foglia danneggiata"},
    "points": [
      {"x": 120.5, "y": 80.2},
      {"x": 170.5, "y": 82.0},
      {"x": 160.0, "y": 120.0}
    ],
    "annotated_at": "2025-08-01T15:14:00"
  }
]
```

### `PUT /annotations/{annotation_id}`

Aggiorna un'annotazione esistente. Solo i campi forniti nel body vengono modificati.

**Request Body**

```json
{
  "label_id": 3,
  "points": [
    {"x": 130.0, "y": 80.2},
    {"x": 170.5, "y": 82.0},
    {"x": 160.0, "y": 120.0}
  ]
}
```

**Response 200 OK**

```json
{
  "id": 14,
  "image_id": 1,
  "label_id": 3,
  "label": {"id": 3, "name": "foglia sana"},
  "points": [
    {"x": 130.0, "y": 80.2},
    {"x": 170.5, "y": 82.0},
    {"x": 160.0, "y": 120.0}
  ],
  "annotated_at": "2025-08-01T15:14:00"
}
```

### `DELETE /annotations/{annotation_id}`

Elimina un'annotazione esistente.

**Response 204 No Content**

______________________________________________________________________
