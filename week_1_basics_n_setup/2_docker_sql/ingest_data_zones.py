#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from time import time
import argparse

def main(params):
    
    user = params.user
    password = params.pswd
    host = params.host
    port = params.port
    db = params.database
    tb = params.table
    url = params.url
    csv_name = params.filename
    

    
    os.system(f"wget {url} -O {csv_name}")
    os.system(f"gzip -d {csv_name}.gz")
    os.system(f"rm -rf {csv_name}.gz")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df = pd.read_csv(csv_name)
    df.to_sql(name=tb,con=engine, if_exists='append')    
    print('Data inserted.')

    os.system(f"rm -rf {csv_name}")

'''
Vars to be used:
- user
- password
- port
- db name
- tablename
- url of the csv
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Ingestion pipeline',
                        description='Ingest CSV data to Postgres'
                        )

    parser.add_argument("-u", "--user",     help="postgres user name")
    parser.add_argument("-pw", "--pswd",    help="postgres user password")
    parser.add_argument("-hs", "--host",     help="host for postgres")
    parser.add_argument("-pt", "--port",    help="host for postgres")
    parser.add_argument("-db", "--database",help="db name for postgres")
    parser.add_argument("-tb", "--table",   help="tb name for postgres")
    parser.add_argument("-url", "--url",   help="url for the gzip file")
    parser.add_argument("-fn", "--filename",   help="name of the csv file")


    args = parser.parse_args() 
    
    main(args)
