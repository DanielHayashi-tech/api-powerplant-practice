import mysql.connector
from mysql.connector import Error


# create a connection to mysql db
def create_connection(hostname, username, userpw, dbname):
    connection = None
    connection = mysql.connector.connect(host=hostname, user=username, password=userpw, database=dbname)
    print("connection was successful")
    return connection


# function that will execute my sql queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        # this cursor is how we execute sql statements
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# fucntion that will read my sql queries
def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    cursor.execute(query)
    # here we are appending the result
    result = cursor.fetchall()
    return result
