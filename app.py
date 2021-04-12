from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"

@app.route("/index")
def harry():
    return render_template('/templates/index.html')
app.run(debug=True)
