FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

ENV SECRET_KEY=dummy-secret-key-only-for-build-stage
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "gunicorn cookbook_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2"]
