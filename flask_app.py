from flask import Flask, render_template, request
from whoosh_index import search_whoosh_index


app = Flask(__name__)

index_dir = "indexdir"

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = None

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            # Search the Whoosh index
            results = search_whoosh_index(index_dir, query)

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)