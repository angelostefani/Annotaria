# Struttura del Database – AIRFARM

Questo documento descrive la struttura del database relazionale utilizzato dall’applicazione AIRFARM.

---

## 🗃️ Tabelle principali

### 1. `images`

Contiene le immagini caricate dal sistema e i metadati EXIF associati.

```sql
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL UNIQUE,
    path TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT NOW(),

    exif_datetime TEXT,
    exif_gps_lat FLOAT,
    exif_gps_lon FLOAT,
    exif_gps_alt FLOAT,
    exif_camera_make TEXT,
    exif_camera_model TEXT,
    exif_lens_model TEXT,
    exif_focal_length FLOAT,
    exif_aperture FLOAT,
    exif_iso INTEGER,
    exif_shutter_speed TEXT,
    exif_orientation TEXT,
    exif_image_width INTEGER,
    exif_image_height INTEGER,

    exif_drone_model TEXT,
    exif_flight_id TEXT,
    exif_pitch FLOAT,
    exif_roll FLOAT,
    exif_yaw FLOAT
);
```

---

### 2. `questions`

Contiene le domande comuni da porre per ciascuna immagine.

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL
);
```

---

### 3. `options`

Opzioni a scelta multipla associate a ciascuna domanda.

```sql
CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL
);
```

---

### 4. `answers`

Risposte fornite dagli utenti per ogni immagine e domanda.

```sql
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    image_id INTEGER NOT NULL REFERENCES images(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    selected_option_id INTEGER NOT NULL REFERENCES options(id),
    answered_at TIMESTAMP DEFAULT NOW()
);
```

---

### 5. `annotations`

Contiene le annotazioni grafiche fatte sulle immagini.

```sql
CREATE TABLE annotations (
    id SERIAL PRIMARY KEY,
    image_id INTEGER NOT NULL REFERENCES images(id),
    label TEXT NOT NULL,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    width FLOAT NOT NULL,
    height FLOAT NOT NULL,
    annotated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Note aggiuntive

- Le immagini sono associate a metadati EXIF che includono anche parametri specifici per immagini acquisite da droni.
- Le domande sono comuni a tutte le immagini.
- Il database è progettato per supportare il versioning futuro delle annotazioni.