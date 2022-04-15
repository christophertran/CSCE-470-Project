from queryTool import QueryTool
from flask import Flask, render_template, request, url_for, redirect

# Create the QueryTool object that will setup the BM25 scorer
# call queryTool.query() to find relevant documents to the query.
queryTool = QueryTool()

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

        # Returns list of dictionaries whose keys are column names
        retrieved_songs = queryTool.query(user_query, 6)

        for doc in retrieved_songs:
            output.append([doc["SONG_NAME"], doc["ARTIST_NAME"], doc["SONG_URL"]])

    return render_template("find.html", outputtext=output)


if __name__ == "__main__":
    app.run()
