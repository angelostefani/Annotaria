# 📂 Documentazione API REST – Annotaria

Questa sezione descrive gli endpoint REST esposti dall'applicazione Annotaria.

---

## ✅ Elenco degli endpoint

| Metodo | Endpoint                            | Descrizione                                      |
|--------|-------------------------------------|--------------------------------------------------|
| GET    | `/images`                           | Restituisce immagini e sincronizza la cartella  |
| POST   | `/questions/`                       | Crea una nuova domanda                          |
| GET    | `/questions/`                       | Elenca tutte le domande                         |
| POST   | `/questions/{id}/options/`          | Aggiunge opzioni a una domanda                  |
| GET    | `/questions/{id}/options/`          | Elenca opzioni di una domanda                   |
| POST   | `/answers/`                         | Registra una risposta                           |
| POST   | `/annotations/`                     | Salva un'annotazione grafica                    |

---

## 📘 Esempi

### POST `/questions/`

```json
{
  "question_text": "Qual è lo stato della pianta?"
}
```

### POST `/questions/{id}/options/`

```json
{
  "option_text": "Foglie ingiallite"
}
```

### POST `/answers/`

```json
{
  "image_id": 1,
  "question_id": 2,
  "selected_option_id": 5
}
```

### POST `/annotations/`

```json
{
  "image_id": 1,
  "label": "foglia malata",
  "x": 100.5,
  "y": 200.0,
  "width": 50.0,
  "height": 75.0
}
```