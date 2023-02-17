FROM python:3.9
WORKDIR C:\Users\rituladh\ab working\ab_working\app
COPY . .
EXPOSE 5000
RUN pip install --upgrade pip Flask psycopg2
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"] 