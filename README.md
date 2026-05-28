Project README — Mail setup & deployment

Mailtrap (recommended for development)

1. Create a free account at https://mailtrap.io and create an inbox.
2. From the Mailtrap inbox settings copy SMTP credentials (host, port, user, pass).
3. In the project root copy `.env.example` to `.env` and paste Mailtrap values:

   cp .env.example .env
   # then edit .env and replace MAILTRAP values

4. Start the stack (rebuild if you changed code):

   docker compose up --build -d

5. Request a password reset in the app (http://localhost:8080/forgot-password/).
   Mailtrap will show the captured email with the OTP.

Gmail (real emails)

- Enable 2FA and create an App Password. Copy those credentials into `.env` replacing Mailtrap values. Use `EMAIL_HOST=smtp.gmail.com` and `EMAIL_PORT=587`.

Render deployment notes

- Do NOT commit `.env`.
- On Render set these environment variables for the backend service:
  - `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
  - `DATABASE_URL` can be provided by Render-managed Postgres and referenced in `render.yaml`.
  - Set `RENDER_API_KEY`, `RENDER_SERVICE_ID_BACKEND`, `RENDER_SERVICE_ID_FRONTEND` in GitHub Actions secrets for auto-deploy.

Testing locally without real SMTP

- The app defaults to the console email backend when `DEBUG=True` so OTPs are printed in backend logs.
- To see OTPs in logs:

   docker compose logs --tail 200 backend

Security recommendations

- Keep OTP lifetime short (15 minutes currently).
- Add rate-limiting and request logging for the password-reset endpoints in production.
