FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "tinder_site.wsgi:application", "--bind", "0:8000"]