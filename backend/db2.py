# import mysql.connector
# import os
# from mysql.connector import Error
# import sys

# # Azure MySQL Connection Details
# # host = os.getenv('AZURE_MYSQL_HOST')
# # user = os.getenv('AZURE_MYSQL_USER')
# # password = os.getenv('AZURE_MYSQL_PASSWORD')
# # database = os.getenv('AZURE_MYSQL_NAME')

# def get_connection():
#     try:
#         connection = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=database,
#             ssl_disabled=False  # Azure MySQL requires SSL by default
#         )
#         return connection
#     except Error as e:
#         print(f"Error connecting to MySQL: {e}")
#         raise

# def insert_rec(entry):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS Staff (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 name VARCHAR(255),
#                 title VARCHAR(255),
#                 email VARCHAR(255),
#                 phone VARCHAR(255)
#             )
#         ''')

#         cursor.execute('''
#             INSERT INTO Staff (name, title, email, phone)
#             VALUES (%s, %s, %s, %s)
#         ''', (
#             entry.get("name"),
#             entry.get("title"),
#             entry.get("email"),
#             entry.get("phone")
#         ))

#         conn.commit()
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         raise