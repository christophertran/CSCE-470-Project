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


@app.route("/find", methods=["GET"])
def find():
    output = []
    if request.args:
        # Gets query_text parameter value and stores it.
        user_query = request.args.get(
            "query_text"
        )  # You will see name="query_text" at our form's textbox on find.html

        # Returns pandas dataframe with COLS and n rows
        retrieved_songs = query(user_query, 6)

        for row in retrieved_songs.itertuples():
            output.append([row.SONG_NAME, row.ARTIST_NAME, row.SONG_URL])

    return render_template("find.html", outputtext=output)

if __name__ == "__main__":
    app.run()