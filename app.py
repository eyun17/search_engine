from flask import Flask, request, render_template
from flask_fontawesome import FontAwesome
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


app = Flask(__name__)
fa = FontAwesome(app)
@app.route("/")
def home():
    return render_template('home_page.html')

@app.route('/crawl')
def search():
    return render_template('test.html')


app.run(host="0.0.0.0", port=80)