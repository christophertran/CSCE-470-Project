from setup import setup, query
from flask import Flask, render_template, request, url_for, redirect

# Setup the BM25 scorer so that we can call the query function
# This is called before setting up the server because we want to be
# able to quickly query the data. The initial setup takes the longest.
setup()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/find", methods=["GET", "POST"])
def find():
    if request.method == "POST":
        user_query = request.form[
            "query"
        ].lower()  # You will see name="query" at our form's input on find.html

        # Returns pandas dataframe with COLS and n rows
        print(query(user_query, 5))
    return render_template("find.html")
