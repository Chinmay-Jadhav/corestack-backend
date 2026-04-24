# Corestack Backend

A production-style backend built with FastAPI, focused on implementing core backend engineering concepts such as authentication, database management, and modular architecture.

## 🚀 Features
- User authentication system
- PostgreSQL integration
- Alembic database migrations
- Modular architecture (services, routes, models)

## 🛠 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Chinmay-Jadhav/corestack-backend.git
cd corestack-backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environemnt variables
Create a .env file :
```.env
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET = <hexadecimal value>
JWT_ALGO = <algorithm of choice>
```

### 5. Run Migrations
```bash
alembic upgrade head
```

### 6. Start the server
```bash
uvicorn src.main:app --reload
```

### 📁 Project Structure

src/
  auth/        # authentication logic
  db/          # database setup
  models/      # ORM models
  routes/      # API routes
  services/    # business logic

migrations/    # alembic migrations

