#video to add multiple databases
from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
from datetime import datetime



app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///posts.sqlite3'}
db = SQLAlchemy(app)
app.secret_key = 'super-secret-key'

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


class Posts(db.Model):
    __bind_key__ = 'two'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)
    tagline = db.Column(db.String(120), nullable=False)



# @app.route("/")
# def home():
#     return render_template('index.html',params=parameters)
#adding functionality to get top 3 posts
@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:parameters['no_of_posts']]
    return render_template('index.html', params=parameters, posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',params=parameters)

@app.route("/dashboard",methods = ['GET', 'POST'])
def dashboard():
#user already logged in 
    if "user" in session and session['user']==parameters['admin_user']:
        posts=Posts.query.all()
        return render_template("dashboard.html",params=parameters,posts=posts)
       # return render_template("contact.html",params=parameters)
    #print(request.method)
    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username==parameters['admin_user'] and userpass==parameters['admin_password']:
            # set the session variable
            session['user']=username
            posts=Posts.query.all()
            return render_template("dashboard.html",params=parameters,posts=posts)
            #return render_template("contact.html",params=parameters)
            
    else:
        return render_template("login.html", params=parameters)



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

#rule is to whatever is the variable you need to pass it to function
@app.route("/post/<string:post_slug>",methods=["Get"])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html',params=parameters,post=post)
#creates both database tables
db.create_all()
firstpost=Posts(title="This is first post",slug="firstpost",content="chalja bhai",img_file='about-bg.jpg',tagline='tag1')
firstpost.date=date = datetime.now()
db.session.add(firstpost)
secondpost=Posts(title="This is second post",slug="second-post",content="cool bro",img_file='about-bg.jpg',tagline='tag2')
thirdpost=Posts(title="This is third post",slug="third-post",content="yeah bro",img_file='about-bg.jpg',tagline='tag3')
db.session.add(secondpost)
db.session.add(thirdpost)
db.session.commit()
app.run(debug=True)



