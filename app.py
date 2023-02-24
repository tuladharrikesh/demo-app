import os
import boto3 
import json
import psycopg2
from flask import Flask, render_template
from flask import Flask, render_template, request, url_for, redirect
from botocore.exceptions import ClientError

#pip install Flask psycopg2



app = Flask(__name__)


def get_db_connection():

    """secret_name = "rds!db-96874cdd-abcf-471d-bb2b-71f0ead3c827"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString'] """



    secret_name = os.environ.get("SECRET_NAME")
    #secret_name = "demo-app/postgreSql" # test secret name
   # secret_name = "demo-app/prod/postgreSql" # prod secret name


    #secret_name = "rds!db-96874cdd-abcf-471d-bb2b-71f0ead3c827"
    
    # Create a Secrets Manager Client
    client = boto3.client('secretsmanager')
    

    # Get the secret value

    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    conn = psycopg2.connect(host=secret['host'],
                            database=secret['dbname'],
                            user=secret['username'],
                            password=secret['password']) 
    
    """conn = psycopg2.connect(host='demo-database.cyy3xzejpvft.us-east-1.rds.amazonaws.com',
                            database='demo_database',
                            user='postgres',
                            password='G8-pzvc%pe0mXAaZN!aP}5(s~dUZ')"""

    """conn = psycopg2.connect(host='demo-database.cyy3xzejpvft.us-east-1.rds.amazonaws.com',
                            database='demo_database',
                            user=secret['username'],
                            password=secret['password'])"""
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        service_name = request.form['service_name']
        product_category = request.form['product_category']
        description = request.form['description']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO services (service_name, product_category, description)'
                    'VALUES (%s, %s, %s)',
                    (service_name, product_category, description))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/main')
def base():
    return render_template('base.html')

@app.route('/list')
def list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services;')
    services = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('list2.html', services = services)

if __name__ == "__main__":
    app.run(debug=True)