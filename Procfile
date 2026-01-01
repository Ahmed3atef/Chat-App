web: daphne -b 0.0.0.0 -p 8000 mainProject.asgi:application
worker: celery -A mainProject worker --loglevel=info
beat: celery -A mainProject beat --loglevel=info
