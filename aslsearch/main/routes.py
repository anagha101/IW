from flask import request, make_response, render_template, redirect, url_for
from flask.blueprints import Blueprint
from aslsearch.models import Words
from aslsearch import db
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import URL

class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    submit = SubmitField()

class DefinitionForm(FlaskForm):
    definition = StringField('Definition', validators=[DataRequired()])

class SignForm(FlaskForm):
    gloss = StringField('ASL Gloss', validators=[DataRequired()])
    pos = StringField('Part of Speech', validators=[DataRequired()])
    url = StringField('YouTube URL', validators=[URL(), DataRequired()])
    context = StringField('Context')

main = Blueprint('main', __name__)

@main.route("/", methods=['GET'])
def homepage():
    html = render_template('index.html')
    response = make_response(html)
    return response


@main.route("/about", methods=['GET'])
def about():
    html = render_template('about.html')
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
    word = Words.query.filter(Words.title.like(title)).all()
    html = render_template("wordpage.html", 
        defs = word[0].definitions)
        
    return make_response(html)

@main.route("/uploadword", methods = ['GET', 'POST'])
def uploadword():
    print("here3")
    form = WordForm()
    if form.validate_on_submit():
        db.session.add(Words(title = form.word.data))
        # make lowercase here
        db.session.commit()
        # return redirect(url_for('uploaddef'))

    return render_template('uploadword.html', form=form)

    # html = render_template("words.html", words = words)

    # return make_response(html)