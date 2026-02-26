# Configuration Service

## Overview

This project is a minimal Configuration Service implemented with Flask. It is designed to act as a standalone
microservice within a broader ecosystem. The service provides versioned configuration storage per
`(service, environment)` pair and exposes a simple REST API to create, retrieve, and list configuration versions.

The repository supports two storage backends:

- File-based repository (for local development and simple setups)
- SQLAlchemy-based repository (for relational database persistence) `[UNDER CONSTRUCTION]`

The project is intentionally minimal and intended as a walking skeleton. It will be extended with authentication, schema
validation, caching, feature flags, and integration hooks.

---

## Core Features

- Health endpoint
- Versioned configuration storage
- Retrieve the latest or specific version
- Pluggable repository implementation
- JSON-based configuration payloads

---

## Project Structure

```
config-service/
├── app.py
├── models.py
├── models_db.py
├── storage.py
├── repository_sqlalchemy.py
├── requirements.txt
└── data/                # used by file-based repository
```

---

## Requirements

- Python 3.10+
- pip
- Virtual environment tool (venv recommended)

Optional:

- PostgreSQL or other relational DB (for SQLAlchemy repository)

---

## Setup Instructions

### 1. Clone the repository

```shell
git clone https://github.com/olegood/lab-conf.git
cd lab-conf
```

### 2. Create virtual environment

Linux/macOS:

```shell
python3 -m venv venv
source venv/bin/activate
```

Windows:

```shell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```shell
pip install -r requirements.txt
```

---

## Running the Service

By default, the app runs with the file-based repository.

```shell
python app.py
```

The service will start at:

```shell
http://localhost:5000
```

Health check:

```shell
GET /health
```

---

## Using SQLAlchemy Repository

To switch to database-backed storage:

1. Modify app.py to use SQLAlchemyConfigRepository.
2. Provide a database URL.

Example (SQLite for development):

```python
repo = SQLAlchemyConfigRepository(
    db_url="sqlite:///config.db"
)
```

Example (PostgreSQL):

```
postgresql+psycopg://user:password@localhost:5432/configdb
```

When using SQLAlchemy for the first time, tables are auto-created via `metadata.create_all()`. In a production setting,
replace this with proper migrations (e.g., Alembic).

---

## Example API Usage

Create configuration:

```
POST /configs/lab-orgs/dev
Content-Type: application/json

{
  "data": {
    "timeout": 30,
    "retries": 3
  },
  "created_by": "admin"
}
```

Get latest configuration:

```
GET /configs/lab-orgs/dev
```

Get a specific version:

```
GET /configs/lab-orgs/dev?version=<uuid>
```

List versions:

```
GET /configs/lab-orgs/dev/versions
```
