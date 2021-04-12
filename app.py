from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"

@app.route("/index")
def harry():
    return render_template('index.html')
#app.run(debug=True)

@app.route("/about")
def about():
    name='Rahul'
    return render_template('about.html',name2=name)

app.run(debug=True)
