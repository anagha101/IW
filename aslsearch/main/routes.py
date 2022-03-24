from flask import request, make_response, render_template
from flask.blueprints import Blueprint
from aslsearch.models import Words
from aslsearch import db

main = Blueprint('main', __name__)

@main.route("/", methods=['GET'])
def homepage():
    html = render_template('index.html')
    response = make_response(html)
    return response

@main.route("/words", methods = ['GET'])
def words():
    print("here1")
    keyword = request.args.get('word')
    print(keyword)
    words = None
    if not keyword:
        words = Words.query.all()
        print(words)
    else:
        keyword = "%{}%".format(keyword)
        words = Words.query.filter(Words.title.like(keyword)).all()
        print(words)

    html = render_template("words.html", words = words)

    return make_response(html)

@main.route("/wordpage/<string:title>", methods = ['GET'])
def wordpage(title):
    print("here2")
    print(title)
    word = Words.query.filter(Words.title.like(title)).all()
    print(word)
    print(word[0])
    print(word[0].definitions)
    print(word[0].definitions[0].signs[0].url)
    html = render_template("wordpage.html", 
        defs = word[0].definitions)
        
    return make_response(html)