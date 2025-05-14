import mysql.connector
from mysql.connector import Error

# Connection details
host = 'localhost'
database = 'staffdb'
user = 'root'
password = 'root'

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='staffdb',
            auth_plugin='mysql_native_password'  # Add this line
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise

def test_connection():
    try:
        conn = get_connection()
        if conn.is_connected():
            print("MySQL connection successful!")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

test_connection()

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
        if conn and conn.is_connected():
            conn.close()
