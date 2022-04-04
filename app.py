from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == "POST":
        user_query = request.form["query"].lower()  # You will see name="query" at our form's input on find.html
    return render_template('find.html')