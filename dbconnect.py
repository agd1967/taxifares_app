#Open database connection and create cursor
import mysql.connector

def connection():

    conn = mysql.connector.connect(user='root',
                                    password='taxi',
                                    host='localhost',
                                    database='taxi')
    c = conn.cursor()

    return c, conn


