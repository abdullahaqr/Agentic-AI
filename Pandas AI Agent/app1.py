import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()


DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
BASE_URL_OF_SQL_AGENT_MODEL = os.environ.get('BASE_URL_OF_SQL_AGENT_MODEL')

# Create engine
# engine = create_engine("mysql+pymysql://your_username:your_password@your_host/your_database")
uri = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'
db_engine = create_engine(uri)
print("Database connected...")

# Load a table data directly into Pandas
# df = pd.read_sql("SELECT * FROM your_table", db_engine)
df = pd.read_sql("SELECT * FROM carc", db_engine)
# print(df.head())
# df.to_csv('carc.csv', index=False)

# # Alternative for Multiple Tables
# tables = pd.read_sql("SHOW TABLES", db_engine)
# table_names = tables.iloc[:, 0].tolist()
# tables_dict = {table: pd.read_sql(f"SELECT * FROM {table}", db_engine) for table in table_names}
# print("Fetching all tables into dataframe completed....")
# # print("dfs->>>>>>", dfs)
# # Convert dictionary to DataFrame
# df = pd.DataFrame(tables_dict)
# print(df.head())