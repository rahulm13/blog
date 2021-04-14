#xThis is a reference code to add multiple databases from flask sqlalchemy https://www.youtube.com/watch?v=SB5BfYYpXjE

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/multiple_databases/one.db'
app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:////mnt/c/Users/antho/Documents/multiple_databases/two.db',
                                  'three' : 'sqlite:////mnt/c/Users/antho/Documents/multiple_databases/three.db'}

db = SQLAlchemy(app)

class One(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Two(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)

class Three(db.Model):
    __bind_key__ = 'three'
    id = db.Column(db.Integer, primary_key=True)

@app.route('/')
def index():
    second = Two(id=634)
    db.session.add(second)
    db.session.commit()

    return 'Added a value to the second table!' 

if __name__ == '__main__':
    app.run(debug=True)