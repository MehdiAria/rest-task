FROM python:3.12-slim
WORKDIR /app
COPY ./project /app
RUN pip install --no-cache-dir django==5.* djangorestframework psycopg2-binary celery redis structlog pyautogui opencv-python-headless psutil gunicorn djangorestframework-simplejwt
ENV DJANGO_SETTINGS_MODULE=config.settings PYTHONUNBUFFERED=1
