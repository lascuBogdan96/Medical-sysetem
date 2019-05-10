from typing import List, Dict
from flask import *
import mysql.connector
import json

app = Flask(__name__)

def connect_to_db():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'hw'
    }
    mydb = mysql.connector.connect(**config)
    return mydb

@app.route('/history')
def get_history():
    hist = []
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.callproc('get_history')
    for res in cursor.stored_results():
        res = res.fetchall()
        for r in res:
            h = {}
            h['action'] = r[0]
            h['name'] = r[1]
            h['doctor'] = r[2]
            h['section'] = r[3]
            h['money'] = r[4]
            h['date'] = str(r[5]);
            hist.append(h)

    return json.dumps(hist)

def get_doctors():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM doct')
    results = {}
    for (id, name, email, telephone, section) in cursor:
        results[id] = [name, email, telephone, section]

    cursor.close()
    conn.close()
    return json.dumps(results)

def get_patients():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pat')
    results = {}
    for (id, name, age, email, telephone, reason, date_arrival, doctor) in cursor:
        results[id] = [name, age, email, telephone, reason, str(date_arrival), doctor]

    cursor.close()
    conn.close()
    return json.dumps(results)

def add_doctor():
    conn = connect_to_db()
    cursor = conn.cursor()

    name = request.values.get('name')
    email = request.values.get('email')
    telephone = request.values.get('telephone')
    section = request.values.get('section')

    insert_stmt = ('INSERT INTO doct(name, email, telephone, section) '
            'VALUES (%s, %s, %s, %s)')
    data = (name, email, telephone, section)
    cursor.execute(insert_stmt, data)
    conn.commit()

    cursor.close()
    conn.close()
    return ""

def add_patient():
    conn = connect_to_db()
    cursor = conn.cursor()

    name = request.values.get('name')
    age = request.values.get('age')
    email = request.values.get('email')
    telephone = request.values.get('telephone')
    reason = request.values.get('reason')
    doctor = request.values.get('doctor')

    insert_stmt = ('INSERT INTO pat(name, age, email, telephone, reason, doctor) '
            'VALUES (%s, %s, %s, %s, %s, %s)')
    data = (name, age, email, telephone, reason, doctor)
    cursor.execute(insert_stmt, data)
    conn.commit()

    cursor.close()
    conn.close()
    return ""

def delete_flight():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'hw'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    id = request.values.get('id')
    cursor.execute('DELETE FROM flights WHERE id = \'' + str(id) + '\'')
    connection.commit()

    cursor.close()
    connection.close()
    return ""

def delete_doctor():
    conn = connect_to_db()
    cursor = conn.cursor()

    id = request.values.get('id')
    cursor.execute('DELETE FROM doct WHERE id = \'' + str(id) + '\'')
    conn.commit()

    cursor.close()
    conn.close()

    return ""


def delete_patient():
    conn = connect_to_db()
    cursor = conn.cursor()

    id = request.values.get('id')
    cursor.execute('DELETE FROM pat WHERE id = \'' + str(id) + '\'')
    conn.commit()

    cursor.close()
    conn.close()

    return ""


@app.route('/doctors', methods = ['GET', 'POST', 'DELETE'])
def doctors():
    if request.method == 'GET':
        return get_doctors()
    if request.method == 'POST':
        return add_doctor()
    if request.method == 'DELETE':
        return delete_doctor()

@app.route('/patients', methods = ['GET', 'POST', 'DELETE'])
def patients():
    if request.method == 'GET':
        return get_patients()
    if request.method == 'POST':
        return add_patient()
    if request.method == 'DELETE':
        return delete_patient()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
