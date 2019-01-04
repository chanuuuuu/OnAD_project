from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("test.html")

app.run(debug=True)