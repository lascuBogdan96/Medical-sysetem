from typing import List, Dict
import sys
import requests
import json
import time

url = 'http://medicalservice:5000/history'
doctor_url =  'http://medicalservice:5000/doctors'
# For testing outside a container, uncomment
#url = 'http://localhost:5000/history'


def add_doctor(name, email, telephone, section):
    r = requests.post(doctor_url, data={'name': name,
                                'email': email,
                                'telephone': telephone,
                                'section' : section})

def delete_doctor(id):
    r = requests.delete(doctor_url, data={'id' : id})

def get_history():
    r = requests.get(url)
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

def get_doctors():
    r = requests.get(doctor_url)
    d = json.loads(r.text)
    header = "id".ljust(5) + "name".ljust(15) + "email".ljust(25) + "telephone".ljust(15) + "section".ljust(10)
    print(header)
    print('=' * len(header))

    for h in d:
        line = ''
        line += str(h).ljust(5)
        line += str(d[h][0]).ljust(15)
        line += str(d[h][1]).ljust(25)
        line += str(d[h][2]).ljust(15)
        line += str(d[h][3]).ljust(10)

        print(line)

main_msg = "What do you want to do?\n\
1 - show history, 2 - show doctors, 3 - add a doctor, 4 - delete a doctor, 5 - show this mesage, 6 - quit"


def main():


    while(True):
        print("Enter a command. Press 5 for help")
        line = sys.stdin.readline()
        if line == "1\n":
            get_history()
        if line == "2\n":
            get_doctors()
        elif line == "3\n":
            name = input("Name of the doctor: ")
            email = input("Email of the doctor: ")
            telephone = input("telephone of the doctor: ")
            section = int(input("section of the doctor: "))

            add_doctor(name, email, telephone, section)
            print("Doctor added!")

        elif line == "4\n":
            id = input("Which doctor id do you wish to delete: ")
            delete_doctor(id)
        elif line == "5\n":
            print(main_msg)
        elif line == "6\n":
            break

if __name__ == '__main__':
    main()
