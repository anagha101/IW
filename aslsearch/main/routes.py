from flask import request, session, make_response, render_template, redirect, url_for
from flask.blueprints import Blueprint
from aslsearch.models import Words, Defs, Signs
from aslsearch import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import URL
import sqlalchemy
import re
from cas import CASClient

cas_client = CASClient(
    version=3,
    service_url='http://localhost:5000/login?next=%2F',
    server_url='https://fed.princeton.edu/cas/login'
)

def is_admin():
    if 'admin' in session:
        isAdmin = True
    else:
        isAdmin = False
    return isAdmin

def validate_url(url):
    url_regex = r'''((http|https)\:\/\/)?www\.youtube\.com\/watch\?v=[\w]{11}'''
    regex = re.compile(url_regex)
    match = regex.match(url)

    if match:
        print("match!")
        return True
    else:
        print("not match!")
        return False


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

class SignForm(FlaskForm):
    gloss = StringField('ASL Gloss', validators=[DataRequired()])
    pos = StringField('Part of Speech', validators=[DataRequired()])
    url = StringField('YouTube URL', validators=[DataRequired()])
    context = StringField('Context', validators=[DataRequired()])
    submit = SubmitField('Add Sign')

class DeleteForm(FlaskForm):
    idk = StringField('idk')

main = Blueprint('main', __name__)

@main.route("/", methods=['GET'])
def homepage():
    html = render_template('index.html', admin=is_admin())
    response = make_response(html)
    return response


@main.route("/about", methods=['GET'])
def about():
    html = render_template('about.html', admin=is_admin())
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

    html = render_template("words.html", words = words, admin=is_admin())

    return make_response(html)

@main.route("/wordpage/<string:title>", methods = ['GET'])
def wordpage(title):
    print("here2: ", title)
    word = Words.query.filter(Words.title.ilike(title)).first()
    html = render_template("wordpage.html", 
        defs = word.definitions,
        title = title.capitalize(),
        admin=is_admin())
        
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
    return render_template('uploadword.html', form=form, admin=is_admin())
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
    return render_template('uploaddef.html', word=word, form=form, admin=is_admin())

@main.route("/<string:word>/<int:defid>/edit", methods = ['GET', 'POST'])
def editdef(word, defid):
    print("here3")
    form = DefinitionForm()
    defobj = Defs.query.get(defid)
    if request.method == 'GET':
        form.definition.data = defobj.definition
    if form.validate_on_submit():
        try:
            defobj.definition = form.definition.data
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except sqlalchemy.exc.IntegrityError as e:
            # some popup with error message with Bootstrap
            print(type(e))
            raise
    return render_template('uploaddef.html', form=form, admin=is_admin())

@main.route("/<string:word>/<int:defid>/delete", methods = ['GET', 'POST'])
def deletedef(word, defid):
    print("inside delete fn")
    defobj = Defs.query.get(defid)
    try:
        print("inside try")
        for sign in defobj.signs:
            db.session.delete(sign)
        db.session.delete(defobj)
        db.session.commit()
        return redirect(url_for('main.wordpage', title=word))
    except sqlalchemy.exc.IntegrityError as e:
        # some popup with error message with Bootstrap
        print(type(e))
        raise

@main.route("/<string:word>/<int:defid>/uploadsign", methods = ['GET', 'POST'])
def uploadsign(word, defid):
    print("here3")
    form = SignForm()
    defobj = Defs.query.get(defid)
    if form.validate_on_submit():
        if not validate_url(form.url.data):
            form.url.errors.append("Must be a Youtube URL")
        else:
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
    return render_template('uploadsign.html', 
        word=word, 
        definition=defobj.definition, 
        form=form,
        admin=is_admin())

@main.route("/<string:word>/<int:defid>/<int:signid>/edit", methods = ['GET', 'POST'])
def editsign(word, defid, signid):
    print("here3")
    form = SignForm()
    signobj = Signs.query.get(signid)
    if request.method == 'GET':
        form.gloss.data = signobj.gloss
        form.pos.data = signobj.pos
        form.url.data = signobj.url
        form.context.data = signobj.context
    if form.validate_on_submit():
        print("in submit")
        try:
            signobj.gloss = form.gloss.data
            signobj.pos = form.pos.data
            signobj.url = form.url.data
            signobj.context = form.context.data
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except sqlalchemy.exc.IntegrityError as e:
            # some popup with error message with Bootstrap
            print(type(e))
            raise
    return render_template('uploadsign.html', form=form, admin=is_admin())

@main.route("/<string:word>/<int:defid>/<int:signid>/delete", methods = ['GET', 'POST'])
def deletesign(word, defid, signid):
    signobj = Signs.query.get(signid)
    try:
        db.session.delete(signobj)
        db.session.commit()
        return redirect(url_for('main.wordpage', title=word))
    except sqlalchemy.exc.IntegrityError as e:
        # some popup with error message with Bootstrap
        print(type(e))
        raise

@main.route('/login')
def login():
    print("inside login")
    if 'admin' in session:
        print("Username exists:", session['admin'])
        # Already logged in
        return redirect(url_for('main.homepage'))

    next = request.args.get('next')
    ticket = request.args.get('ticket')
    if not ticket:
        # Send to CAS login
        cas_login_url = cas_client.get_login_url()
        return redirect(cas_login_url)

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    if not user:
        return 'Failed to verify ticket. <a href="/login">Login</a>'
    else:  # Login success, redirect
        if (user=='anaghar' or user=='nadb') :
            session['admin'] = True
        else:
            session['admin'] = False
        return redirect(next)


@main.route('/logout')
def logout():
    redirect_url = url_for('main.logout_callback', _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)

    return redirect(cas_logout_url)


@main.route('/logout_callback')
def logout_callback():
    # Logout success, redirect
    session.pop('admin', None)
    return redirect(url_for('main.homepage'))