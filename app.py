import os
import boto3 
import re
import json
import psycopg2
from flask import Flask, render_template
from flask import Flask, render_template, request, url_for, redirect
from botocore.exceptions import ClientError


app = Flask(__name__)


def get_db_connection():

    # Gets the preset environment variable and appends to create secret name that matches to secrets manager.
    secret_name = "{}/demo-app/postgresql".format(os.environ.get('COPILOT_ENVIRONMENT_NAME')) 
    
    # Create a Secrets Manager Client
    client = boto3.client('secretsmanager')
    
    # Get the secret value
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    conn = psycopg2.connect(host=secret['host'],
                            database=secret['dbname'],
                            user=secret['username'],
                            password=secret['password']) 
    
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