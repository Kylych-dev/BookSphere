FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

#WORKDIR /app/backend


RUN python backend/manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.core.wsgi:application"]