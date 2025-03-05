import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="db4free.net",
        user="rcrdpimentel",
        password="a123456@",
        database="caa_db"
    )
    return connection
