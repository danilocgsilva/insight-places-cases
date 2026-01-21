# Insight Places - SQLAlchemy + Alembic Project

This project replaces the MySQL script with a Python-based approach using SQLAlchemy for ORM and Alembic for database migrations.

## Project Structure

```
insight_places/
├── alembic/
│   ├── versions/
│   │   └── 001_initial_schema.py
│   └── env.py
├── models.py
├── database.py
├── alembic.ini
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

Update the database URL in both files:

**alembic.ini** (line 63):
```ini
sqlalchemy.url = mysql+pymysql://your_user:your_password@localhost/insight_places
```

**database.py** (line 6):
```python
DATABASE_URL = "mysql+pymysql://your_user:your_password@localhost/insight_places"
```

### 3. Create Database

First, create the database in MySQL:

```sql
CREATE DATABASE insight_places;
```

### 4. Initialize Alembic (Already Done)

The project already has Alembic initialized with:
- `alembic.ini` configuration file
- `alembic/env.py` environment file
- Initial migration in `alembic/versions/001_initial_schema.py`

### 5. Run Migrations

Apply the migrations to create all tables:

```bash
alembic upgrade head
```

### 6. Verify Tables

Check that all tables were created:

```sql
USE insight_places;
SHOW TABLES;
```

## Using the Models

### Example: Creating Records

```python
from database import SessionLocal
from models import Proprietario, Cliente, Endereco, Hospedagem, Aluguel, Avaliacao
from datetime import date
from decimal import Decimal

# Create a session
db = SessionLocal()

# Create a proprietario
proprietario = Proprietario(
    proprietario_id="prop_001",
    nome="João Silva",
    cpf_cnpj="12345678901",
    contato="joao@example.com"
)
db.add(proprietario)

# Create an endereco
endereco = Endereco(
    endereco_id="end_001",
    rua="Rua das Flores",
    numero=123,
    bairro="Centro",
    cidade="São Paulo",
    estado="SP",
    cep="01234-567"
)
db.add(endereco)

# Create a hospedagem
hospedagem = Hospedagem(
    hospedagem_id="hosp_001",
    tipo="Apartamento",
    endereco_id="end_001",
    proprietario_id="prop_001",
    ativo=True
)
db.add(hospedagem)

# Commit changes
db.commit()

# Close session
db.close()
```

### Example: Querying Records

```python
from database import SessionLocal
from models import Hospedagem

db = SessionLocal()

# Query all active hospedagens
active_hospedagens = db.query(Hospedagem).filter(Hospedagem.ativo == True).all()

for hosp in active_hospedagens:
    print(f"ID: {hosp.hospedagem_id}, Tipo: {hosp.tipo}")
    print(f"Proprietário: {hosp.proprietario.nome}")
    print(f"Endereço: {hosp.endereco.rua}, {hosp.endereco.numero}")

db.close()
```

## Common Alembic Commands

### Create a New Migration (Auto-generate)
```bash
alembic revision --autogenerate -m "description of changes"
```

### Create a New Migration (Manual)
```bash
alembic revision -m "description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback One Migration
```bash
alembic downgrade -1
```

### View Migration History
```bash
alembic history
```

### View Current Version
```bash
alembic current
```

## Models Overview

- **Proprietario**: Property owners
- **Cliente**: Customers/guests
- **Endereco**: Addresses
- **Hospedagem**: Accommodations (linked to endereco and proprietario)
- **Aluguel**: Rentals (linked to cliente and hospedagem)
- **Avaliacao**: Reviews (linked to cliente and hospedagem)

## Key Features

- ✅ All relationships properly configured with SQLAlchemy ORM
- ✅ Foreign keys maintained
- ✅ Migration system for version control of database schema
- ✅ Type-safe models with proper data types
- ✅ Rollback capability with `downgrade()` functions