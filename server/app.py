from flask import Flask, render_template, request, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import mysql.connector
from datetime import datetime

app = Flask(__name__)
#app.secret_key = 'super secret key'


def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database='bd'
    )
    return mydb

connect_to_db()


@app.route('/history')
def get_history():
    hist = []
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.callproc('get_history')
    for res in cursor.stored_results():
        res = res.fetchall()
        for r in res:
            # print(r)
            h = {}
            h['action'] = r[0]
            h['name'] = r[1]
            h['doctor'] = r[2]
            h['section'] = r[3]
            h['money'] = r[4]
            h['date'] = r[5]
            hist.append(h)

    return str(hist)
    return render_template('history.html', hist=hist)


@app.route('/doctor')
def get_doctor_patients():
    id = request.args.get('id')
    print(id)
    if not id:
        id = 1


    conn = connect_to_db()
    cursor = conn.cursor()

    args = [id]
    cursor.callproc('get_doct_pats', args)
    title = list(cursor.stored_results())[0].fetchall()[0][0]

    pat = []
    for r in list(cursor.stored_results())[1].fetchall():
        p = {}
        p['id'] = r[0]
        p['name'] = r[1]
        p['age'] = r[2]
        p['email'] = r[3]
        p['tel'] = r[4]
        p['reason'] = r[5]
        p['date'] = r[6]
        p['money'] = r[7]
        pat.append(p)

    return render_template('doctor.html', title=title, pat=pat)



class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])



@app.route("/pacient", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        telephone = request.form['telephone']
        reason = request.form['reason']
        doctor = request.form['doctor']

        # print(name)
        # print(age)
        # print(email)
        # print(telephone)
        # print(reason)
        # print(doctor)

        conn = connect_to_db()
        cursor = conn.cursor()

        args = [name, age, email, telephone, reason, datetime.now(), doctor]
        result_args = cursor.callproc('insert_pat', args)
        conn.commit()

        # if form.validate():
            # Save the comment here.
            # flash('Thanks for registration ' + name)
        # else:
        #     flash('Error: All the form fields are required. ')
        return get_history()

    return render_template('insert-pat.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
