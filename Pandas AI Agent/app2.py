import mysql.connector
import pandas as pd
import os


DATABASE_USER = "root"
DATABASE_PASSWORD = ""
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "healthq_test_db"

# Database connection
# conn = mysql.connector.connect(
#     host="your_host",
#     user="your_username",
#     password="your_password",
#     database="your_database"
# )
conn = mysql.connector.connect(
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    database=DATABASE_NAME
)

# Query to fetch data
# query = "SELECT * FROM your_table"
query = "SELECT * FROM carc"

# Load data into Pandas DataFrame
df = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Print DataFrame
print(df.head())
