# 🗃️ Struttura del Database – Annotaria

---

## 1. `users`

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
);
```

## 2. `images`

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

## 3. `questions`

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL
);
```

## 4. `options`

```sql
CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL
);
```

## 5. `answers`

```sql
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    image_id INTEGER NOT NULL REFERENCES images(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    selected_option_id INTEGER NOT NULL REFERENCES options(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    answered_at TIMESTAMP DEFAULT NOW()
);
```

## 6. `annotations`

```sql
CREATE TABLE annotations (
    id SERIAL PRIMARY KEY,
    image_id INTEGER NOT NULL REFERENCES images(id),
    label TEXT NOT NULL,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    width FLOAT NOT NULL,
    height FLOAT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    annotated_at TIMESTAMP DEFAULT NOW()
);
```
