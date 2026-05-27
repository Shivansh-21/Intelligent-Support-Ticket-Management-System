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

Since Render discontinued its free PostgreSQL database tier, you have three options to deploy this application:

### Option A: Free PostgreSQL with Neon.tech / Supabase (Recommended)

1. Sign up for a free PostgreSQL database on [Neon](https://neon.tech/) or [Supabase](https://supabase.com/).
2. Copy your database connection string (looks like `postgresql://user:password@host/db`).
3. In `render.yaml`, you can remove the `databases` block and define a Web Service.
4. When creating the Web Service on Render, add an environment variable `DATABASE_URL` and paste your Neon/Supabase connection string.

### Option B: Ephemeral SQLite (Testing Only)

If you don't provide a `DATABASE_URL`, the application will automatically fall back to SQLite. 
*Note: Any data created will be lost whenever the Render web service restarts or redeploys.*

---

### Step-by-Step Deployment Steps:

1. **Push this project to GitHub**:
   Because the local machine is authenticated to GitHub as `harshitchauhann95`, pushing directly via HTTPS/SSH to `Shivansh-21`'s repository will return a `403 Forbidden` error.
   
   To push successfully as `Shivansh-21`:
   - Generate a Personal Access Token (PAT) on the `Shivansh-21` GitHub account under Settings -> Developer Settings -> Personal Access Tokens (Classic) with `repo` scopes.
   - Run the push command using your token:
     ```bash
     git push https://<YOUR_PERSONAL_ACCESS_TOKEN>@github.com/Shivansh-21/Intelligent-Support-Ticket-Management-System.git main
     ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com).
   - Click **New** -> **Web Service**.
   - Connect your GitHub account and select the `Intelligent-Support-Ticket-Management-System` repository.
   - Set the runtime to **Python**.
   - Build Command: `./build.sh`
   - Start Command: `gunicorn support_system.wsgi:application`
   - Under **Environment Variables**, add:
     - `SECRET_KEY`: (generate a random string)
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
     - `CSRF_TRUSTED_ORIGINS`: `https://your-app-name.onrender.com`
     - `DATABASE_URL`: (your Neon or Supabase connection string, if using Option A)

Render will automatically install requirements, collect static files, run migrations, and start the Gunicorn server.
