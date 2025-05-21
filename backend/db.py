import mysql.connector
import os
from mysql.connector import Error

# Azure MySQL Connection Details
host = os.getenv('AZURE_MYSQL_HOST', 'universityscraper-server.privatelink.mysql.database.azure.com')
database = os.getenv('AZURE_MYSQL_NAME', 'universityscraper-database')
user = os.getenv('AZURE_MYSQL_USER', 'akohlscrapedb@universityscraper-server')
password = os.getenv('AZURE_MYSQL_PASSWORD', 'Blue1234?')

print("🌐 DEBUG: MySQL host being used =", host)


def get_connection():
    try:
        print(f"Connecting to: {host}")  # TEMP debug
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def insert_rec(entry):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Staff (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                title VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(255)
            )
        ''')

        # Insert the record
        cursor.execute('''
            INSERT INTO Staff (name, title, email, phone)
            VALUES (%s, %s, %s, %s)
        ''', (entry.get('name'), entry.get('title'), entry.get('email'), entry.get('phone')))

        conn.commit()

    except Error as e:
        print(f"Error inserting record: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



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
