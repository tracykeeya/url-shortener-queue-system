# URL Shortener Queue System
A Django application that shortens URLs and processes them asynchronously using a Redis-backed task queue.

## Features
- REST API endpoint to create shortened URLs
- Background job worker using Celery + Redis
- Error handling and retry mechanism
- Unit tests for core components

## Architecture
1. User submits a URL → stored in database.
2. Worker picks it up → processes and generates a shortened URL.
3. Worker handles failures gracefully with retry logic.

## How to Run
1. `git clone ...`
2. Setup Redis and install requirements `pip install -r requirements.txt`
3. Run worker: `celery -A project worker --loglevel=info`
4. Run the web server: `python manage.py runserver`
