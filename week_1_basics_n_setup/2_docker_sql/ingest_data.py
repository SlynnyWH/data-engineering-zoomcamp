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
    

    
    os.system(f"wget {url} -O {csv_name}.gz")
    os.system(f"gzip -d {csv_name}.gz")
    os.system(f"rm -rf {csv_name}.gz")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    dfX = next(df_iter)

    dfX.tpep_pickup_datetime = pd.to_datetime(dfX.tpep_pickup_datetime)
    dfX.tpep_dropoff_datetime = pd.to_datetime(dfX.tpep_dropoff_datetime)
    dfX.to_sql(name=tb,con=engine, if_exists='replace')
    #dfX.head(n=0).to_sql(name=tb,con=engine, if_exists='replace')

    from time import time
    u_t_start = time()

    n=1
    for x in df_iter:
        t_start = time()
        x.tpep_pickup_datetime = pd.to_datetime(x.tpep_pickup_datetime)
        x.tpep_dropoff_datetime = pd.to_datetime(x.tpep_dropoff_datetime)
        x.to_sql(name=tb,con=engine, if_exists='append')
        
        t_end = time()
        print(f'inserted chunk number {n}, it took %.3f seconds' % (t_end - t_start))
        n = n+1
        
    u_t_end = time()
    print(f'Chunks inserted: {n-1}. Total time: %.3f seconds' % (u_t_end - u_t_start))

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
