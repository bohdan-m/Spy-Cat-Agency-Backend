# Spy Cat Agency Backend

## Overview

This is the backend for the **Spy Cat Agency** test task.
It provides **CRUD operations for Spy Cats** and **Missions / Targets**.

**Tech stack:**

* Python
* Django
* Django REST Framework
* PostgreSQL
* CORS Headers

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/bohdan-m/Spy-Cat-Agency-Backend/tree/main
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Create a `.env` file in the root directory. Example:

```
POSTGRES_DB=spycat
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

## 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Run development server

```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000`

---

## 7. Postman collection

You can find all endpoints in the `[postman/SpyCatAgency.postman_collection.json](https://www.postman.com/bohdanmatvieiev1-9415816/spy-cat-agency/collection/51164177-7a22163f-f7e0-40bb-bfa6-6c90fa1c75d4/?action=share&creator=51164177)`.
Import it into Postman to test all API calls.

---

## Notes

* Frontend is built separately (Next.js). Focus here is on **backend CRUD and API**.
* Breed validation is done using [TheCatAPI](https://api.thecatapi.com/v1/breeds).
* CORS is configured for `http://localhost:3000` (Next.js frontend).
* SQLite is preconfigured for easy local setup. PostgreSQL recommended for production or real testing.

---
