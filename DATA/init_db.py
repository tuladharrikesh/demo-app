import os
import psycopg2
import boto3
import json


secret_name = "demodatabaseAuroraSecret-wne9Ak8tMKhD"

# Create a Secrets Manager Client
client = boto3.client('secretsmanager')

# Get the secret value

response = client.get_secret_value(SecretId=secret_name)
secret = json.loads(response['SecretString'])

conn = psycopg2.connect(host=secret['host'],
                            database=secret['dbname'],
                            user=secret['username'],
                            password=secret['password'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS services;')
cur.execute('CREATE TABLE services (id serial PRIMARY KEY,'
                                 'service_name VARCHAR (20) NOT NULL,'
                                 'product_category VARCHAR (20) NOT NULL,'
                                 'description text,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO services (service_name, product_category, description)'
            'VALUES (%s, %s, %s)',
            ('Amazon EC2',
             'Compute',
             'Resizable compute capacity in the Cloud.')
            )


cur.execute('INSERT INTO services (service_name, product_category, description)'
            'VALUES (%s, %s, %s)',
            ('Amazon S3',
             'Storage',
             'Secure, durable, and scalable object storage infrastructure.')
            )

conn.commit()

cur.close()
conn.close()