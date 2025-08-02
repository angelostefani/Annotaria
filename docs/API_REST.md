# 📘 Documentazione API REST – AIRFARM

Tutte le API restituiscono e accettano dati in formato JSON.  
Prefisso base: `http://localhost:8000/`

---

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
    "exif_datetime": "2025-07-31 14:30:00"
  }
]
```

---

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

### `GET /questions/{question_id}/options/`
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

### `POST /questions/{question_id}/options/`
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

---

## 📝 RISPOSTE

### `POST /answers/`
Registra la risposta fornita da un utente per una determinata immagine e domanda.

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

---

## 🎯 ANNOTAZIONI

### `POST /annotations/`
Salva un’annotazione su un'immagine selezionata (area rettangolare + label).

**Request Body**
```json
{
  "image_id": 1,
  "label": "foglia danneggiata",
  "x": 120.5,
  "y": 80.2,
  "width": 50,
  "height": 30
}
```

**Response 201 Created**
```json
{
  "id": 14,
  "image_id": 1,
  "label": "foglia danneggiata",
  "x": 120.5,
  "y": 80.2,
  "width": 50,
  "height": 30,
  "annotated_at": "2025-08-01T15:14:00"
}
```

---

## 🛠️ Endpoints in sviluppo

- `PUT /questions/{id}` – Modifica una domanda
- `DELETE /questions/{id}` – Elimina una domanda
- `PUT /options/{id}` – Modifica un’opzione
- `DELETE /options/{id}` – Elimina un’opzione
- `GET /answers/{image_id}` – Tutte le risposte per un'immagine
- `GET /annotations/{image_id}` – Tutte le annotazioni per immagine