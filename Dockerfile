FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip3 install -r requirements.txt
COPY ./news /app/
CMD python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && ["gunicorn", "news/news.wsgi:application", "--bind", "0.0.0.0:8000"]