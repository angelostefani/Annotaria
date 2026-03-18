# Documentazione API REST – Annotaria

Tutte le API restituiscono e accettano dati in formato JSON.
Prefisso base: `http://localhost:9100/`

Gli endpoint contrassegnati con **(auth)** richiedono il token JWT nell'header:
`Authorization: Bearer <token>`

Gli endpoint contrassegnati con **(admin)** richiedono ruolo `Amministratore`.

______________________________________________________________________

## AUTENTICAZIONE

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
  "role": "Esperto",
  "expert_types": []
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

### `GET /users/me` (auth)

Restituisce i dati dell'utente autenticato.

**Response 200 OK**

```json
{
  "id": 1,
  "username": "alice",
  "role": "Esperto",
  "expert_types": [{"id": 1, "name": "Agronomo"}]
}
```

### `POST /users/me/password` (auth)

Cambia la password dell'utente autenticato. La nuova password deve avere almeno 8 caratteri e deve essere diversa da quella attuale.

**Request Body**

```json
{
  "current_password": "vecchia",
  "new_password": "nuova1234",
  "new_password_confirm": "nuova1234"
}
```

**Response 200 OK**

```json
{
  "detail": "Password updated"
}
```

______________________________________________________________________

## IMMAGINI

### `GET /images` (auth)

Restituisce l'elenco delle immagini visibili all'utente autenticato e sincronizza il DB con la directory `IMAGE_DIR`. Gli Esperti vedono solo le immagini delle tipologie associate alle proprie competenze; gli Amministratori vedono tutto.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "filename": "immagine1.jpg",
    "path": "/app/image_data/immagine1.jpg",
    "image_type_id": 1,
    "exif_camera_model": "DJI Mavic Air 2",
    "exif_datetime": "2025-07-31 14:30:00"
  }
]
```

### `POST /images/upload` (auth, admin)

Carica una nuova immagine salvandola sul server ed estrae i metadati EXIF. È possibile specificare una tipologia immagine già esistente.

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
  "path": "/app/image_data/nuova.jpg",
  "image_type_id": 1,
  "exif_camera_model": "DJI Mavic Air 2",
  "exif_datetime": "2025-07-31 14:30:00"
}
```

### `POST /images/import-directory` (auth, admin)

Importa in blocco tutte le immagini presenti in una directory (o ricorsivamente nelle sue sotto-directory). La directory deve essere una sotto-directory di `IMAGE_DIR`.

**Request Body**

```json
{
  "directory": "campagna_luglio",
  "image_type_id": 1,
  "recursive": true
}
```

**Response 200 OK**

```json
{
  "created": 42,
  "updated": 3,
  "skipped": 1,
  "errors": []
}
```

| Campo | Descrizione |
|-------|-------------|
| `created` | Nuove immagini aggiunte al database |
| `updated` | Immagini già presenti con metadati aggiornati |
| `skipped` | File ignorati (estensione non supportata) |
| `errors` | Array di `{"path": "...", "error": "..."}` per i file falliti |

**Estensioni supportate**: `.jpg`, `.jpeg`, `.tif`, `.tiff`, `.png`, `.raw`, `.nef`, `.cr2`, `.arw`

### `GET /images/{image_id}`

Restituisce i dettagli di una singola immagine.

**Response 200 OK**

```json
{
  "id": 1,
  "filename": "immagine1.jpg",
  "path": "/app/image_data/immagine1.jpg",
  "exif_camera_model": "DJI Mavic Air 2",
  "image_type": {
    "id": 1,
    "name": "Aerea"
  }
}
```

### `PUT /images/{image_id}` (auth, admin)

Aggiorna i metadati di un'immagine esistente.

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
  "path": "/app/image_data/nuovo_nome.jpg",
  "image_type_id": 2
}
```

### `DELETE /images/{image_id}` (auth, admin)

Rimuove un'immagine dal database e dal filesystem.

**Response 204 No Content**

______________________________________________________________________

## TIPOLOGIE IMMAGINE

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

### `POST /image-types/` (auth, admin)

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

### `PUT /image-types/{type_id}` (auth, admin)

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

### `DELETE /image-types/{type_id}` (auth, admin)

Elimina una tipologia immagine.

**Response 204 No Content**

______________________________________________________________________

## TIPOLOGIE ESPERTO

### `GET /expert-types/`

Elenca tutte le tipologie esperto disponibili.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "name": "Agronomo",
    "image_types": [{"id": 1, "name": "Aerea"}]
  }
]
```

### `POST /expert-types/` (auth, admin)

Crea una nuova tipologia esperto, con le tipologie immagine associate.

**Request Body**

```json
{
  "name": "Geologo",
  "image_type_ids": [1, 2]
}
```

**Response 200 OK**

```json
{
  "id": 2,
  "name": "Geologo",
  "image_types": [{"id": 1, "name": "Aerea"}, {"id": 2, "name": "Termica"}]
}
```

### `PUT /expert-types/{type_id}` (auth, admin)

Aggiorna nome e tipologie immagine associate a una tipologia esperto.

**Request Body**

```json
{
  "name": "Geologo senior",
  "image_type_ids": [2]
}
```

**Response 200 OK**

```json
{
  "id": 2,
  "name": "Geologo senior",
  "image_types": [{"id": 2, "name": "Termica"}]
}
```

### `DELETE /expert-types/{type_id}` (auth, admin)

Elimina una tipologia esperto e rimuove i collegamenti con utenti e tipologie immagine.

**Response 204 No Content**

______________________________________________________________________

## ETICHETTE

### `GET /labels/`

Elenca tutte le etichette disponibili.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "name": "Anomalia",
    "image_types": [{"id": 1, "name": "Aerea"}]
  }
]
```

### `POST /labels/` (auth, admin)

Crea una nuova etichetta. Il campo `image_type_ids` è opzionale.

**Request Body**

```json
{
  "name": "Danno struttura",
  "image_type_ids": [1]
}
```

**Response 200 OK**

```json
{
  "id": 2,
  "name": "Danno struttura",
  "image_types": [{"id": 1, "name": "Aerea"}]
}
```

### `PUT /labels/{label_id}` (auth, admin)

Aggiorna nome e tipologie immagine associate all'etichetta.

**Request Body**

```json
{
  "name": "Danno strutturale",
  "image_type_ids": [1, 2]
}
```

**Response 200 OK**

```json
{
  "id": 2,
  "name": "Danno strutturale",
  "image_types": [{"id": 1, "name": "Aerea"}, {"id": 2, "name": "Termica"}]
}
```

### `DELETE /labels/{label_id}` (auth, admin)

Elimina un'etichetta.

**Response 204 No Content**

______________________________________________________________________

## DOMANDE E OPZIONI

### `GET /questions/`

Elenca tutte le domande presenti nel sistema.

**Response 200 OK**

```json
[
  {
    "id": 1,
    "question_text": "Qual è lo stato della pianta?",
    "image_types": [{"id": 1, "name": "Aerea"}],
    "depends_on_question_id": null,
    "depends_on_option_id": null
  }
]
```

### `POST /questions/` (auth, admin)

Crea una nuova domanda. Il campo `image_type_ids` associa la domanda a una o più tipologie di immagine.

**Request Body**

```json
{
  "question_text": "La pianta è infestata?",
  "image_type_ids": [1]
}
```

**Response 200 OK**

```json
{
  "id": 5,
  "question_text": "La pianta è infestata?",
  "image_types": [{"id": 1, "name": "Aerea"}],
  "depends_on_question_id": null,
  "depends_on_option_id": null
}
```

### `PUT /questions/{question_id}` (auth, admin)

Aggiorna il testo e le tipologie immagine associate a una domanda.

**Request Body**

```json
{
  "question_text": "La pianta mostra segni di infestazione?",
  "image_type_ids": [1, 2]
}
```

**Response 200 OK**

```json
{
  "id": 5,
  "question_text": "La pianta mostra segni di infestazione?",
  "image_types": [{"id": 1, "name": "Aerea"}, {"id": 2, "name": "Termica"}]
}
```

### `DELETE /questions/{question_id}` (auth, admin)

Elimina una domanda e le sue opzioni.

**Response 204 No Content**

### `GET /questions/{question_id}/options`

Restituisce tutte le opzioni associate a una domanda.

**Response 200 OK**

```json
[
  {
    "id": 10,
    "question_id": 5,
    "option_text": "Sì",
    "follow_up_question_ids": [6]
  },
  {
    "id": 11,
    "question_id": 5,
    "option_text": "No",
    "follow_up_question_ids": []
  }
]
```

### `POST /questions/{question_id}/options` (auth, admin)

Aggiunge una nuova opzione a una domanda esistente. Il campo `follow_up_question_ids` specifica quali domande mostrare quando questa opzione viene selezionata (logica condizionale).

**Request Body**

```json
{
  "option_text": "Non determinabile",
  "follow_up_question_ids": []
}
```

**Response 200 OK**

```json
{
  "id": 12,
  "question_id": 5,
  "option_text": "Non determinabile",
  "follow_up_question_ids": []
}
```

### `PUT /options/{option_id}` (auth, admin)

Aggiorna il testo e le domande follow-up di un'opzione.

**Request Body**

```json
{
  "option_text": "Incerto",
  "follow_up_question_ids": [7]
}
```

**Response 200 OK**

```json
{
  "id": 12,
  "question_id": 5,
  "option_text": "Incerto",
  "follow_up_question_ids": [7]
}
```

### `DELETE /options/{option_id}` (auth, admin)

Elimina un'opzione.

**Response 204 No Content**

### `GET /questions/{question_id}/image-types`

Restituisce le tipologie immagine associate a una domanda.

**Response 200 OK**

```json
[
  {"id": 1, "name": "Aerea"}
]
```

### `POST /questions/{question_id}/image-types/{image_type_id}` (auth, admin)

Aggiunge una tipologia immagine alla domanda.

**Response 200 OK** — restituisce la domanda aggiornata.

### `DELETE /questions/{question_id}/image-types/{image_type_id}` (auth, admin)

Rimuove una tipologia immagine dalla domanda.

**Response 204 No Content**

______________________________________________________________________

## RISPOSTE

Richiedono autenticazione; l'utente associato viene determinato dal token nell'header `Authorization: Bearer <token>`.

### `POST /answers/` (auth)

Registra la risposta per una determinata immagine e domanda. L'associazione all'utente è automatica. Se l'utente ha già risposto alla stessa domanda sulla stessa immagine, la risposta viene aggiornata (upsert).

**Request Body**

```json
{
  "image_id": 1,
  "question_id": 5,
  "selected_option_id": 12
}
```

**Response 200 OK**

```json
{
  "id": 33,
  "image_id": 1,
  "question_id": 5,
  "selected_option_id": 12,
  "user_id": 1,
  "answered_at": "2025-08-01T15:12:00"
}
```

### `GET /answers/{image_id}` (auth)

Restituisce tutte le risposte dell'utente autenticato per una determinata immagine.

**Response 200 OK**

```json
[
  {
    "id": 33,
    "image_id": 1,
    "question_id": 5,
    "selected_option_id": 12,
    "user_id": 1,
    "answered_at": "2025-08-01T15:12:00"
  }
]
```

______________________________________________________________________

## ANNOTAZIONI

Richiedono autenticazione; le annotazioni vengono collegate all'utente identificato dal token nell'header `Authorization`.

### `POST /annotations/` (auth)

Salva un'annotazione su un'immagine selezionata (poligono + etichetta). `user_id` è gestito automaticamente.

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

**Response 200 OK**

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
  "user_id": 1,
  "annotated_at": "2025-08-01T15:14:00"
}
```

### `GET /annotations/{image_id}` (auth)

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
    "user_id": 1,
    "annotated_at": "2025-08-01T15:14:00"
  }
]
```

### `PUT /annotations/{annotation_id}` (auth)

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
  "user_id": 1,
  "annotated_at": "2025-08-01T15:14:00"
}
```

### `DELETE /annotations/{annotation_id}`

Elimina un'annotazione esistente.

**Response 204 No Content**

______________________________________________________________________
