import flask
from flask import Flask
from flask import jsonify, request
from flask_httpauth import HTTPTokenAuth
from mysql.connector import Error
from db import create_connection, execute_query, execute_read_query

conn = create_connection('coogs.cypiz5agmq0c.us-east-1.rds.amazonaws.com', 'admin', 'phoebe123', 'coogs_db')
cursor = conn.cursor()

# setting up an application name
app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # show errors in browser

app.secret_key = 'd80c53e65a11d69aca7897d78478280d3c701045ada7a8ae5220aa01a020e756'

# you are assigning the type of auth (be sure to specify in postman)
auth = HTTPTokenAuth(scheme='Bearer')

master_token = '880088'

# this function is used to veryify that the token is the same as the master token being passed
@auth.verify_token
def verify_token(token):
    return token == master_token

# def get_active_col():
#     curser = conn.cursor()
#     result = curser.execute("SELECT * FROM powerplant")
#     for s in range(len(result)):
#         if result[s]["active"] == 'TRUE':
#             return 'coolio'


# this function is used to select all data and order it from highest to lowest capacity
@app.route('/api/powerplant', methods=['GET'])
def show_powerplant():
    query = "SELECT * FROM coogs_db.powerplant ORDER BY capacity DESC;"
    try:
        plants = execute_read_query(conn, query)
        return jsonify(plants)
    except Error as e:
        return f" The error '{e}' has occurred!"

# this function is used to add a row to the powerplant tablew
@app.route('/api/powerplant', methods=['POST'])
# auth with token if token is used then grant access
@auth.login_required
def add_powerplant():
    request_data = request.get_json()
    new_name = request_data['name']
    new_type = request_data['type']
    new_capacity = request_data['capacity']
    new_inauguration = request_data['inauguration']
    new_active = request_data['active']

    insert_powerplant = f"INSERT INTO powerplant (name, type, capacity, inauguration, active) VALUES ('{new_name}', '{new_type}', '{new_capacity}', {new_inauguration},'{new_active}')"
    try:
        execute_query(conn, insert_powerplant)

        return f"Congratulations, you have successfully added a {new_name} to the powerplant table!"
    except Error as e:
        return f"the error {e} occurred"


@app.route('/api/powerplant', methods=['DELETE'])
# auth with token if token is used then grant access
@auth.login_required
def remove_powerplant():
    request_data = request.get_json()
    new_id = request_data['id']
    curser = conn.cursor()
    result = curser.execute("SELECT * FROM powerplant")
    jsonify(result)
    for s in range(len(result)):
        if result[s]["active"] == 'TRUE':
            delete = f'UPDATE coogs_db.powerplant SET active = "FALSE" WHERE id={new_id}'
            execute_query(conn, delete)
            return f"Congratulations, you have successfully updated {new_id} "
        else:
            deleting = f'UPDATE coogs_db.powerplant SET active = "TRUE" WHERE id={new_id}'
            execute_query(conn, deleting)
            return f"Congratulations, you have successfully updated {new_id} "



# this function updates only capacity
@app.route('/api/powerplant', methods=['PUT'])
# auth with token if token is used then grant access
@auth.login_required
def update_powerplant_capacity():
    request_data = request.get_json()
    id = request_data['id']
    new_capacity = request_data['capacity']

    update_criteria = f"UPDATE powerplant SET capacity='{new_capacity}' WHERE id={id}"
    try:
        execute_query(conn, update_criteria)

        return f"Congratulations, you have successfully updated row {id} !!!!!!!!"
    except Error as e:
        return f"the error {e} occurred"


app.run()
