from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.sqlite3'
db = SQLAlchemy(app)

import json
with open('config.json','r') as c:
    parameters = json.load(c)['params']



class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

@app.route("/")
def home():
    return render_template('index.html',params=parameters)


@app.route("/about")
def about():
    return render_template('about.html',params=parameters)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        print(Contacts.query.all())

    return render_template('contact.html',params=parameters)

@app.route("/view")
def view():
    #keys={'a':{'name':'Rahul','email':'r'},'b':{'name':'Shivam','email':'ss'}}
    val=Contacts.query.all()

    return render_template("view.html",values=val,params=parameters)
    #return render_template("view.html",values=keys)

db.create_all()
app.run(debug=True)



