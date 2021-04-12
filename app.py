from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"

@app.route("/index")
def harry():
    return render_template('view.html')
#app.run(debug=True)

@app.route("/about")
def about():
    name='Rahul'
    return render_template('about.html',name2=name)

@app.route("/bootstrap")
def bootstrap():
    return render_template('bootstrap.html')

app.run(debug=True)
