from flask import request, make_response, render_template, redirect, url_for
from flask.blueprints import Blueprint
from aslsearch.models import Words, Defs, Signs
from aslsearch import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import URL
import sqlalchemy
import re
from urllib.parse import urlparse

def validate_url(form, field):
        url_regex = r'''((http|https)\:\/\/)?www\.youtube\.com\/watch\?v=[\w]{11}'''
        regex = re.compile(url_regex)
        match = regex.match(field.data)
        if not match:
            print("inside error")
            # HELP NOT RAISING
            raise ValidationError('Field must be a Youtube URL')

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

class EditDefinitionForm(FlaskForm):
    definition = StringField('Definition', validators=[DataRequired()])
    submit = SubmitField('Edit Definition')

class SignForm(FlaskForm):
    gloss = StringField('ASL Gloss', validators=[DataRequired()])
    pos = StringField('Part of Speech', validators=[DataRequired()])
    url = StringField('YouTube URL', validators=[DataRequired(), validate_url])
    context = StringField('Context', validators=[DataRequired()])
    submit = SubmitField('Add Sign')

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

@main.route("/<string:word>/<int:defid>/edit", methods = ['GET', 'POST'])
def editdef(word, defid):
    print("here3")
    form = EditDefinitionForm()
    defobj = Defs.query.get(defid)
    if request.method == 'GET':
        form.definition.data = defobj.definition
    if form.validate_on_submit():
        print("in submit")
        try:
            print("in try")
            print("OG: ", defobj.definition)
            print("new: ", form.definition.data)
            defobj.definition = form.definition.data
            print("replaced? :", defobj.definition)
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except sqlalchemy.exc.IntegrityError as e:
            # some popup with error message with Bootstrap
            print(type(e))
            raise
    return render_template('editdef.html', form=form)

@main.route("/<string:word>/<int:defid>/uploadsign", methods = ['GET', 'POST'])
def uploadsign(word, defid):
    print("here3")
    form = SignForm()
    defobj = Defs.query.get(defid)
    print("here4")
    if form.validate_on_submit():
        print("inside submit")
        try:
            print("inside try")
            print(form.url.data)
            embed_url = convert_url(form.url.data)
            print(embed_url)
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