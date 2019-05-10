from typing import List, Dict
import sys
import requests
import json
import time
from random import randint

url_history = 'http://medicalservice:5000/history'
patient_url = 'http://medicalservice:5000/patients'
# For testing outside a container:
#url = 'http://localhost:5000/history'


def add_patient(name, age, email, telephone, reason, doctor):
    r = requests.post(patient_url, data={'name': name,
                                'age': age,
                                'email': email,
                                'telephone': telephone,
                                'reason': reason,
                                'doctor' : doctor})

def delete_patient(id):
    r = requests.delete(patient_url, data={'id' : id})

def get_history():
    r = requests.get(url_history)
    d = json.loads(r.text)
    header = "action".ljust(15) + "name".ljust(15) + "doctor".ljust(20) + "section".ljust(15) + "money".ljust(10) + "date".ljust(10)
    print(header)
    print('=' * len(header))
    for h in d:
        line = ''
        line += str(h['action']).ljust(15)
        line += str(h['name']).ljust(15)
        line += str(h['doctor']).ljust(20)
        line += str(h['section']).ljust(15)
        line += str(h['money']).ljust(10)
        line += str(h['date']).ljust(10)

        print(line)

def get_patients():
    r = requests.get(patient_url)
    d = json.loads(r.text)
    header = "id".ljust(5) + "name".ljust(15) + "age".ljust(15) + "email".ljust(25) + "telephone".ljust(15) + "reason".ljust(30) + "date_arrival".ljust(25) + "doctor".ljust(10)
    print(header)
    print('=' * len(header))

    for h in d:
        line = ''
        line += str(h).ljust(5)
        line += str(d[h][0]).ljust(15)
        line += str(d[h][1]).ljust(15)
        line += str(d[h][2]).ljust(25)
        line += str(d[h][3]).ljust(15)
        line += str(d[h][4]).ljust(30)
        line += str(d[h][5]).ljust(25)
        line += str(d[h][6]).ljust(10)

        print(line)

main_msg = "What do you want to do?\n\
1 - show history, 2 - show patients, 3 - add patient, 4 - delete patient, 5 - show this message, 6 - quit"

def main():
    while(True):
        print("Enter a command. Press 5 for help")
        line = sys.stdin.readline()
        if line == "1\n":
            get_history()
        elif line == "2\n":
            get_patients()

        elif line == "3\n":
            name = input("Name of the patient: ")
            age = input("Age of the patient: ")
            email = input("Email of the patient: ")
            telephone = input("Telephone of the patient: ")
            reason = input("Reasor of the patient: ")
            doctor = input("Doctor of the patient: ")
            add_patient(name, age, email, telephone, reason, doctor)
            print("Patient added!")
        elif line == "4\n":
            id = input("Which patient id do you wish to delete: ")
            delete_patient(id)
        elif line == "5\n":
            print(main_msg)
        elif line == "6\n":
            break

if __name__ == '__main__':
    main()
