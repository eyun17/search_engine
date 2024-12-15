from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)

@app.route("/")
def home():
    return """ <form action="/search" method="get">
            <input type="text" name="q" placeholder="Search">
            <button type="submit">Search</button>
        </form>
    """


