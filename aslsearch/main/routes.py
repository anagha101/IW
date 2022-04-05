from flask import request, make_response, render_template, redirect, url_for
from flask.blueprints import Blueprint
from aslsearch.models import Words, Defs, Signs
from aslsearch import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import URL
import sqlalchemy
import re

def convert_url(url):
    video_id = url[-11:]
    embed_url = "https://www.youtube.com/embed/" + video_id
    return embed_url

class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    submit = SubmitField('Add Word')

class DefinitionForm(FlaskForm):
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Add Definition')

# class EditDefinitionForm(FlaskForm):
#     definition = StringField('Definition', validators=[DataRequired()])
#     submit = SubmitField('Add Definition')

class SignForm(FlaskForm):
    gloss = StringField('ASL Gloss', validators=[DataRequired()])
    pos = StringField('Part of Speech', validators=[DataRequired()])
    url = StringField('YouTube URL', validators=[DataRequired()])
    context = TextAreaField('Context')
    submit = SubmitField('Add Sign')

    def validate_url(form, url):
        pattern = re.compile("https://www\.youtube\.com/watch\?v=[\w]{11}")
        match = pattern.match(url.data)
        pattern = re.compile("www\.youtube\.com/watch\?v=[\w]{11}")
        match = pattern.match(url.data)
        print("correct?: ", match)
        if not match:
            print("inside error")
            raise ValidationError('Field must be a Youtube URL')

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
        words = Words.query.order_by(Words.title).all()
        print(words)
    else:
        keyword = "%{}%".format(keyword)
        words = Words.query.filter(Words.title.like(keyword)).order_by(Words.title).all()
        print(words)

    html = render_template("words.html", words = words)

    return make_response(html)

@main.route("/wordpage/<string:title>", methods = ['GET'])
def wordpage(title):
    print("here2: ", title)
    word = Words.query.filter(Words.title.ilike(title)).first()
    html = render_template("wordpage.html", 
        defs = word.definitions,
        title = title.capitalize())
        
    return make_response(html)

@main.route("/uploadword", methods = ['GET', 'POST'])
def uploadword():
    print("here3")
    form = WordForm()
    if form.validate_on_submit():
        try:
            db.session.add(Words(title = form.word.data))
            # make lowercase here
            db.session.commit()
            return redirect(url_for('main.wordpage', title=form.word.data))
        except sqlalchemy.exc.IntegrityError as e:
            # some popup with error message with Bootstrap
            print(type(e))
            raise
    return render_template('uploadword.html', form=form)
    # html = render_template("words.html", words = words)
    # return make_response(html)

@main.route("/<string:word>/uploaddef", methods = ['GET', 'POST'])
def uploaddef(word):
    print("here3")
    form = DefinitionForm()
    if form.validate_on_submit():
        try:
            definition = Defs(definition = form.definition.data)
            wordobj = Words.query.filter(Words.title.ilike(word)).first()
            db.session.add(definition)
            wordobj.definitions.append(definition)
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except sqlalchemy.exc.IntegrityError as e:
            # some popup with error message with Bootstrap
            # definition already exists
            print(type(e))
            raise
    return render_template('uploaddef.html', word=word, form=form)

# @main.route("/<string:word>/<int:defid>/edit", methods = ['GET', 'POST'])
# def editdef(word, defid):
#     print("here3")
#     form = EditDefinitionForm()
#     defobj = Defs.query.filter(Defs.id.like(defid)).first()
#     form.definition.data = defobj.definition
#     if form.validate_on_submit():
#         try:
#             definition = Defs(definition = form.definition.data)
#             db.session.update(Defs.definition, definition)
#             db.session.commit()
#             return redirect(url_for('main.wordpage', title=word))
#         except sqlalchemy.exc.IntegrityError as e:
#             # some popup with error message with Bootstrap
#             print(type(e))
#             raise
#     return render_template('uploaddef.html', form=form)

@main.route("/<string:word>/<int:defid>/uploadsign", methods = ['GET', 'POST'])
def uploadsign(word, defid):
    print("here3")
    form = SignForm()
    defobj = Defs.query.get(defid)
    if form.validate_on_submit():
        try:
            embed_url = convert_url(form.url.data)
            sign = Signs(gloss = form.gloss.data, pos = form.pos.data, context = form.context.data, url = embed_url)
            db.session.add(sign)
            defobj.signs.append(sign)
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except sqlalchemy.exc.IntegrityError as e:
            # some popup with error message with Bootstrap
            # sign already exists!
            print(type(e))
            raise

    return render_template('uploadsign.html', word=word, definition=defobj.definition, form=form)