FROM python:3.9

WORKDIR /app/data

COPY . .

RUN pip install --upgrade pip psycopg2

CMD ["python", "./init_db.py"]