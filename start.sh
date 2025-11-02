#!/bin/bash
# Startup script that runs migrations and starts gunicorn

# Navigate to the repository root (where manage.py is)
cd /opt/render/project/src/..

# Run migrations automatically
python manage.py migrate --noinput || true

# Create admin user if it doesn't exist
# Password comes from ADMIN_PASSWORD env var, or use the default specified below
python manage.py create_admin --username zeen --email zeenalzein4@gmail.com --password "${ADMIN_PASSWORD:-@zenZEEN20&25}" || true

# Set PYTHONPATH to include current directory (repo root) so Python can find WorkTrack module
export PYTHONPATH=/opt/render/project/src/../:$PYTHONPATH

# Start gunicorn from repo root (WorkTrack module is at WorkTrack/WorkTrack/)
exec gunicorn WorkTrack.WorkTrack.wsgi:application --bind 0.0.0.0:$PORT

