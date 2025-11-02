# Deployment Guide

## Production Checklist

### Backend (Django) Deployment

1. **Environment Variables**
   - Copy `.env.example` to `.env`
   - Set `SECRET_KEY` to a secure random value
   - Set `DEBUG=False`
   - Add your domain to `ALLOWED_HOSTS`
   - Update `CORS_ALLOWED_ORIGINS` with your frontend domain

2. **Database**
   - Current: SQLite (development)
   - Production: Use PostgreSQL or MySQL
   - Update `DATABASES` in `settings.py`

3. **Static Files**
   - Run `python manage.py collectstatic`
   - Configure web server (nginx/apache) to serve static files

4. **Security Settings**
   - Ensure `SESSION_COOKIE_SECURE=True` (HTTPS required)
   - Ensure `CSRF_COOKIE_SECURE=True` (HTTPS required)
   - Set `SESSION_COOKIE_HTTPONLY=True`
   - Update `CORS_ALLOWED_ORIGINS` with production frontend URL

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Frontend (React/Vite) Deployment

1. **Environment Variables**
   - Copy `.env.example` to `.env`
   - Set `VITE_API_BASE_URL` to your production backend URL

2. **Build**
   ```bash
   npm run build
   ```

3. **Deploy**
   - Deploy `dist/` folder to your hosting service (Netlify, Vercel, etc.)
   - Ensure environment variables are set in your hosting platform

### Important Notes

- Always use HTTPS in production
- Keep `SECRET_KEY` secret
- Don't commit `.env` files to version control
- Update CORS settings for your production domains
- Test PDF generation after deployment
- Ensure static files (logo) are accessible

