#!/bin/bash
# Startup script that runs migrations and starts gunicorn

# This matches the working command that successfully deployed
# Go to repo root (one level up from WorkTrack directory)
cd ..

# Run migrations automatically
python manage.py migrate --noinput || true

# Create admin user if it doesn't exist (only if not already created)
python manage.py create_admin --username zeen --email zeenalzein4@gmail.com --password "${ADMIN_PASSWORD:-@zenZEEN20&25}" || true

# Go back into WorkTrack directory and start gunicorn
cd WorkTrack

# Set PYTHONPATH to include parent directory so Python can find WorkTrack module
export PYTHONPATH=..:$PYTHONPATH

# Start gunicorn (WorkTrack module is at ./WorkTrack/wsgi.py)
exec gunicorn WorkTrack.wsgi:application --bind 0.0.0.0:$PORT

