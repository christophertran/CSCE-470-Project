from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/find', methods=['GET', 'POST'])
def find():
    return render_template('find.html')