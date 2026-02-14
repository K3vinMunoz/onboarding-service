# Onboarding Service (FastAPI)

Servicio para administrar **Client Apps** y sus **API Keys**: crear, listar, rotar y activar/desactivar.  
El servicio **no almacena la API key en texto plano**: guarda un **hash (HMAC-SHA256 + pepper)** y un **prefix** para identificación.

---

## Comenzando

Estas instrucciones te permiten levantar el proyecto en tu máquina local para desarrollo y pruebas.

---

## Pre-requisitos

Qué necesitas antes de iniciar:

- Docker + Docker Compose
- Python 3.11+
- Git (opcional)

---

## Instalación

### 1) Levantar PostgreSQL (Docker)

Levanta la base de datos:

```bash
docker compose up -d
```

Verifica que esté corriendo:

```bash
docker ps
```

Postgres quedará accesible en:
- Host: `localhost`
- Puerto: `5433`
- DB: `onboarding`

---

### 2) Configuración de entorno

Crea tu `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

---

### 3) Instalación (Python)

Crea y activa el entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

---

### 4) Migraciones (Alembic)

Aplicar migraciones:

```bash
alembic upgrade head
```

Crear una migración nueva:

```bash
alembic revision --autogenerate -m "describe_change"
```

---

## Correr el servicio

Levanta el servidor:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación y endpoints útiles:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL (Docker)
- Alembic (migrations)

---

## Estructura del proyecto (resumen)

- `app/` Código del servicio (FastAPI, modelos, seguridad, auth)
- `app/schemas/` Schemas Pydantic por dominio
- `alembic/` Migraciones
- `alembic.ini` Configuración Alembic
- `docker-compose.yml` PostgreSQL local para desarrollo
- `.env`
- `.env.example`
- `requirements.txt` Dependencias