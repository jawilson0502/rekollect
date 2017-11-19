import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey

import yaml

CONFIG_FILE_NAME = "config.yaml"

with open(CONFIG_FILE_NAME, 'r') as f:
    CONFIG = yaml.load(f)['postgres']

def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of PostgreSQL URL 
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine is our connection
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta

# Connect to DB to initialize
con, meta = connect(CONFIG['user'], CONFIG['password'], CONFIG['db'])

# Below are all the tables that need to be created
results = Table('results', meta,
                Column('date', sqlalchemy.types.DateTime),
                Column('file_id', String),
                Column('plugin', String),
                Column('result', sqlalchemy.types.JSON))

files = Table('files', meta,
              Column('id', Integer, primary_key=True),
              Column('filename', String),
              Column('case_name', String)
             )

# Create the above table(s)
meta.create_all(con)
