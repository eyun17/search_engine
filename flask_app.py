from flask import Flask, render_template, request
from whoosh_index import search_whoosh_index, create_whoosh_index, populate_whoosh_index, find_all_pages


app = Flask(__name__)

index_dir = "indexdir"
base_url = "https://vm009.rz.uos.de/crawl/"


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = None

    if request.method == "POST":
        query = request.form.get("query")

        if query:
            windex = create_whoosh_index(index_dir)
            pages = find_all_pages(base_url)
            populate_whoosh_index(base_url, pages, windex)
            #########if the query doesn't exist, error message poped up
            # Search the Whoosh index
            results = search_whoosh_index(index_dir, query)

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)