#video to add multiple databases
from flask import Flask, render_template, request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
from datetime import datetime
import os
from werkzeug.utils import secure_filename



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



@app.route("/edit/<string:sno>" , methods=['GET', 'POST'])
#always pass the argument like slug sno in the function
def edit(sno):
    if "user" in session and session['user']==parameters['admin_user']:
        if(request.method=='POST'):
            box_title = request.form.get('title')
            tline = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if sno=='0':
                post = Posts(title=box_title, slug=slug, content=content, tagline=tline, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
                return redirect('/dashboard')
                
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.tline = tline
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)
                #return redirect(/dashboard)

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=parameters, post=post,sno=sno)

@app.route("/uploader",methods = ['GET', 'POST'])
def uploader():
    if "user" in session and session['user']== parameters['admin_user']:
        if(request.method=='POST'):
            f=request.files('myfile')
            f.save(os.path.join(parameters["upload_loaction"],secure_filename(f.filename)))
            return "uploaded succesfully"


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/delete/<string:sno>" , methods=['GET', 'POST'])
#always pass the argument like slug sno in the function
def delete(sno):
    if "user" in session and session['user']== parameters['admin_user']:
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect("/dashboard")


#creates both database tables
db.create_all()

firstpost=Posts(title="This is first post",slug="firstpost",content="chalja bhai",img_file='about-bg.jpg',tagline='tag1',date = datetime.now())
secondpost=Posts(title="This is second post",slug="second-post",content="cool bro",img_file='about-bg.jpg',tagline='tag2',date = datetime.now())
thirdpost=Posts(title="This is third post",slug="third-post",content="yeah bro",img_file='about-bg.jpg',tagline='tag3',date = datetime.now())

# db.session.add(firstpost)
# db.session.add(secondpost)
# db.session.add(thirdpost)
# db.session.commit()

app.run(debug=True)



