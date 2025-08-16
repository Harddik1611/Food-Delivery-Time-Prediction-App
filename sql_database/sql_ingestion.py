import pandas as pd
import sqlite3
import os
import logging

# -------------------------------
# Configure Logging
# -------------------------------
def setup_logging(log_file='sql_ingestion.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s — %(levelname)s — %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Logging is set up.")


# -------------------------------
# Load CSV into DataFrame
# -------------------------------
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully read CSV file: {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise


# -------------------------------
# Ingest DataFrame into SQLite
# -------------------------------
def ingest_to_sqlite(df, db_path, table_name):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logging.info(f"Data successfully ingested into SQLite table: {table_name}")
    except Exception as e:
        logging.error(f"Error ingesting data into SQLite: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logging.info("SQLite connection closed.")


# -------------------------------
# Main Executionsql
# -------------------------------
def main():
    setup_logging()

    # File paths
    csv_file_path = os.path.join('data', 'train.csv')
    db_file_path = 'food_delivery.db'
    table_name = 'food_delivery_data'

    # Load and ingest
    df = load_csv(csv_file_path)
    ingest_to_sqlite(df, db_file_path, table_name)


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == '__main__':
    main()
