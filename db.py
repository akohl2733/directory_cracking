import pyodbc

# Update with your actual Azure SQL Database connection details
server = 'arkstaffserver.database.windows.net'
database = 'staffdb'
username = 'akohl51404'
password = 'Blue1234?'
driver = '{ODBC Driver 18 for SQL Server}'

connection_string = (
    f"DRIVER={driver};"
    f"SERVER=tcp:{server},1433;"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_connection():
    return pyodbc.connect(connection_string)

def test_connection():
    try:
        conn = get_connection()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
test_connection()

def insert_rec(entry):
    conn = get_connection()
    cursor = conn.cursor()

    # Create the table if it doesn't exist (optional, for convenience)
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

    # Insert the record
    cursor.execute('''
            INSERT INTO Staff (name, title, email, phone)
            VALUES (?, ?, ?, ?)
        ''', entry.get('name'), entry.get('title'), entry.get('email'), entry.get('phone'))


    conn.commit()
    cursor.close()
    conn.close()