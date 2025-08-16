from sqlalchemy import create_engine
engine= create_engine('sqlite:///D:/Grow Data Skill/food_delivery.db')
conn=engine.connect()

import sqlite3
import pandas as pd
import logging
logging.basicConfig(
    filename="sql_ingestion.log", 
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    filemode="a"  
)

def ingest_db(df, table_name, engine):
    '''this function will ingest the dataframe into database table'''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)
    
def create_train_summary(conn):
    
