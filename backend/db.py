import os
import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="u",
        password = "pw",
        database = "staffdb"
    )

def insert_rec(entry):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            title VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(255)
        )
    ''')

    cursor.execute('''
        INSERT INTO staff (name, title, email, phone)
        VALUES (%s, %s, %s, %s)
    ''', (
        entry.get("name"),
        entry.get("title"),
        entry.get("email"),
        entry.get("phone")
    ))

    conn.commit()
    cursor.close()
    conn.close()