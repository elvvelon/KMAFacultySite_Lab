# Faculty Site

A Django-based web portal for the Faculty of Humanities at NaUKMA.

---

## Quick Start & Running the Project

### 1. Prerequisites
- Python 3.10+
- `pip` and `virtualenv`

### 2. Environment Setup

Clone or extract the repository, open a terminal in the project root, and set up a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (cmd):
venv\Scripts\activate.bat
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install Django and required dependencies:
```bash
pip install django
```

### 4. Database Setup & Migrations
Run database migrations and populate the initial faculty dataset:
```bash
python manage.py migrate
python manage.py loaddata initial_data
```

*(Optional) Create an administrative account to access the admin panel:*
```bash
python manage.py createsuperuser
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Homepage:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Verifying Migrations (Rollback & Re-apply)

To test the two-way migration pipeline:

```bash
# Roll back all migrations in the faculty app to zero
python manage.py migrate faculty zero

# Re-apply all migrations up to the latest state
python manage.py migrate
```