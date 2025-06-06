FROM python:3.12

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 80
EXPOSE 6379