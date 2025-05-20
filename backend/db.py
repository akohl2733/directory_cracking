import mysql.connector
from mysql.connector import Error
import os

# Azure MySQL Connection Details
host = os.getenv('universityscraper-server.mysql.database.azure.com', 'universityscraper-server.mysql.database.azure.com')
database = os.getenv('universityscraper-database', 'staffdb')
user = os.getenv('IpB3BDgu$VhQGBme', 'akohlscrapedb@universityscraper-server')
password = os.getenv('xdizdhgxyp', 'Blue1234?')
driver = '{ODBC Driver 18 for SQL Server}'


connection_string = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_connection():
    return pyodbc.connect(connection_string)

#def get_connection():
    # try:
    #     connection = mysql.connector.connect(
    #         host=host,
    #         user=user,
    #         password=password,
    #         database=database,
    #         ssl_ca=None,  # Optional: specify path to SSL cert if needed
    #         ssl_disabled=True  # Set to False if you require SSL
    #     )
    #     return connection
    # except Error as e:
    #     print(f"Error connecting to Azure MySQL: {e}")
    #     raise

def insert_rec(entry):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        IF OBJECT_ID('Staff', 'U') IS NULL
        BEGIN
            CREATE TABLE Staff (
                id INT PRIMARY KEY IDENTITY(1,1),
                name NVARCHAR(255),
                title NVARCHAR(255),
                email NVARCHAR(255),
                phone NVARCHAR(255)
            )
        END
    ''')

    cursor.execute('''
        INSERT INTO Staff (name, title, email, phone)
        VALUES (?, ?, ?, ?)
    ''', (entry.get('name'), entry.get('title'), entry.get('email'), entry.get('phone')))

    conn.commit()
    cursor.close()
    conn.close()

# def test_connection():
#     try:
#         conn = get_connection()
#         if conn.is_connected():
#             print("Azure MySQL connection successful!")
#         conn.close()
#     except Exception as e:
#         print(f"Error: {e}")

# Optional: run to test immediately
# test_connection()

# def insert_rec(entry):
#     conn = None
#     cursor = None
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         # Create table if it doesn't exist
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS Staff (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 name VARCHAR(255),
#                 title VARCHAR(255),
#                 email VARCHAR(255),
#                 phone VARCHAR(255)
#             )
#         ''')

#         # Insert the record
#         cursor.execute('''
#             INSERT INTO Staff (name, title, email, phone)
#             VALUES (%s, %s, %s, %s)
#         ''', (entry.get('name'), entry.get('title'), entry.get('email'), entry.get('phone')))

#         conn.commit()

#     except Error as e:
#         print(f"Error inserting record: {e}")
#         if conn:
#             conn.rollback()
#         raise
#     finally:
#         if cursor:
#             cursor.close()
#         if conn and conn.is_connected():
#             conn.close()
