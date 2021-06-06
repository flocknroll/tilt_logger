import psycopg2
import os

pwd = os.environ['TILT_DB_PWD']

with psycopg2.connect(host='localhost', dbname='tilt_db', user='tilt', password=pwd):
    pass