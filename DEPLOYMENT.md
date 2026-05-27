# PostgreSQL, Docker, GitHub Actions, and Render

## What PostgreSQL Is

PostgreSQL is a production database server. Unlike SQLite, which stores data in one local `db.sqlite3` file, PostgreSQL runs as a separate service with users, passwords, networking, backups, and better support for real deployments.

This project now reads the database connection from `DATABASE_URL`.

Local Docker database URL:

```text
postgresql://support_user:support_password@db:5432/support_db
```

GitHub Actions database URL:

```text
postgresql://support_user:support_password@localhost:5432/support_db
```

## Local Docker Setup

This project has three Docker services:

```text
web      Django app
db       PostgreSQL database
pgadmin  Browser UI for PostgreSQL
```

Start everything:

```bash
docker compose up --build
```

Open the app:

```text
http://127.0.0.1:8000/
```

Open pgAdmin:

```text
http://127.0.0.1:5050/
```

pgAdmin login:

```text
Email: admin@example.com
Password: admin123
```

Add a pgAdmin server connection:

```text
Host: db
Port: 5432
Database: support_db
Username: support_user
Password: support_password
```

Create Django superuser inside Docker:

```bash
docker compose exec web python manage.py createsuperuser
```

Stop containers:

```bash
docker compose down
```

Stop containers and delete database volume:

```bash
docker compose down -v
```

## GitHub Actions

Workflow file:

```text
.github/workflows/ci.yml
```

It runs on push and pull request. It starts a PostgreSQL service, installs dependencies, runs:

```bash
python manage.py check
python manage.py migrate --no-input
python manage.py test
```

## Render Deployment

Render config file:

```text
render.yaml
```

It creates:

```text
support-ticket-web  Django web service
support-ticket-db   Managed PostgreSQL database
```

Deployment steps:

1. Push this project to GitHub.
2. Go to Render Dashboard.
3. Open Blueprints.
4. Click New Blueprint Instance.
5. Connect your GitHub repository.
6. Select this repo.
7. Apply the blueprint.

Render will:

```text
install requirements
collect static files
run migrations before deploy
start gunicorn
connect DATABASE_URL automatically
```

After deploy, open your Render URL.

If your Render workspace does not offer a free PostgreSQL plan, choose the available paid/hobby database plan in the dashboard.
