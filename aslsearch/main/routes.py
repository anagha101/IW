from flask import request, session, make_response, render_template, redirect, url_for
from flask.blueprints import Blueprint
from aslsearch.models import Admins, Words, Defs, Signs
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
    url_regex = r'''.*(youtube|youtu.be).*'''
    regex = re.compile(url_regex)
    match = regex.match(url)
    if match:
        return True
    else:
        return False

def convert_url(url):
    video_id = url[-11:]
    embed_url = "https://www.youtube.com/embed/" + video_id
    return embed_url

class AdminForm(FlaskForm):
    admin = StringField('Add Administrator', validators=[DataRequired()])
    submit = SubmitField('Add')

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
    context = StringField('Additional Information')
    submit = SubmitField('Add Sign')

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

@main.route("/admins", methods = ['GET', 'POST'])
def admins():
    form = AdminForm()
    admins = Admins.query.order_by(Admins.netid).all()
    if form.validate_on_submit():
        try:
            db.session.add(Admins(netid = form.admin.data.lower()))
            db.session.commit()
            return redirect(url_for('main.admins', admins=admins))
            # Only sqlalchemy error encountered, will handle more as they come
        except sqlalchemy.exc.IntegrityError:
            return 'Admin priveleges already granted. <a href="/admins">Try another netid.</a>'
        except:
            return 'Unexpected Error!'
    return render_template('admins.html', form=form, admins=admins, admin=is_admin())

@main.route("/<int:adminid>/delete", methods = ['GET', 'POST'])
def removeadmin(adminid):
    adminobj = Admins.query.get(adminid)
    try:
        db.session.delete(adminobj)
        db.session.commit()
        return redirect(url_for('main.admins'))
    except Exception as e:
        print(type(e))
        return 'Unexpected Error!'

@main.route("/words", methods = ['GET'])
def words():
    keyword = request.args.get('word')
    words = None
    if not keyword:
        words = Words.query.order_by(Words.title).all()
    else:
        keyword = "%{}%".format(keyword.lower())
        words = Words.query.filter(Words.title.like(keyword)).order_by(Words.title).all()
    html = render_template("words.html", words = words, admin=is_admin())
    return make_response(html)

@main.route("/wordpage/<string:title>", methods = ['GET'])
def wordpage(title):
    word = Words.query.filter(Words.title.ilike(title)).first()
    html = render_template("wordpage.html", 
        defs = word.definitions,
        title = title.capitalize(),
        admin=is_admin())   
    return make_response(html)

@main.route("/uploadword", methods = ['GET', 'POST'])
def uploadword():
    form = WordForm()
    if form.validate_on_submit():
        try:
            db.session.add(Words(title = form.word.data.lower()))
            db.session.commit()
            return redirect(url_for('main.wordpage', title=form.word.data))
            # Only sqlalchemy error encountered, will handle more as they come
        except sqlalchemy.exc.IntegrityError:
            return 'Word already exists. <a href="/uploadword">Try another word.</a>'
        except:
            return 'Unexpected Error!'
    return render_template('uploadword.html', form=form, admin=is_admin())

@main.route("/<string:word>/delete", methods = ['GET', 'POST'])
def deleteword(word):
    wordobj = Words.query.filter(Words.title.ilike(word)).first()
    print("word: ", wordobj.title)
    try:
        print("in try")
        for defobj in wordobj.definitions:
            for signobj in defobj.signs:
                db.session.delete(signobj)
                print("deleted signs")
            db.session.delete(defobj)
            print("deleted defs")
        db.session.delete(wordobj)
        print("deleted word")
        db.session.commit()
        return redirect(url_for('main.words'))
    except Exception as e:
        print(type(e))
        return 'Unexpected Error!'

@main.route("/<string:word>/uploaddef", methods = ['GET', 'POST'])
def uploaddef(word):
    form = DefinitionForm()
    if form.validate_on_submit():
        try:
            definition = Defs(definition = form.definition.data)
            wordobj = Words.query.filter(Words.title.ilike(word)).first()
            db.session.add(definition)
            wordobj.definitions.append(definition)
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except Exception as e:
            print(type(e))
            return 'Unexpected Error!'
    return render_template('uploaddef.html', word=word, form=form, admin=is_admin())

@main.route("/<string:word>/<int:defid>/edit", methods = ['GET', 'POST'])
def editdef(word, defid):
    form = DefinitionForm()
    defobj = Defs.query.get(defid)
    if request.method == 'GET':
        form.definition.data = defobj.definition
    if form.validate_on_submit():
        try:
            defobj.definition = form.definition.data
            db.session.commit()
            return redirect(url_for('main.wordpage', title=word))
        except Exception as e:
            print(type(e))
            return 'Unexpected Error!'
    return render_template('uploaddef.html', word=word, form=form, admin=is_admin())

@main.route("/<string:word>/<int:defid>/delete", methods = ['GET', 'POST'])
def deletedef(word, defid):
    defobj = Defs.query.get(defid)
    try:
        for signobj in defobj.signs:
            db.session.delete(signobj)
        db.session.delete(defobj)
        db.session.commit()
        return redirect(url_for('main.wordpage', title=word))
    except Exception as e:
        print(type(e))
        return 'Unexpected Error!'

@main.route("/<string:word>/<int:defid>/uploadsign", methods = ['GET', 'POST'])
def uploadsign(word, defid):
    form = SignForm()
    defobj = Defs.query.get(defid)
    if form.validate_on_submit():
        if not validate_url(form.url.data):
            form.url.errors.append("Must be a Youtube URL")
        else:
            try:
                embed_url = convert_url(form.url.data)
                sign = Signs(gloss = form.gloss.data, 
                    pos = form.pos.data, 
                    context = form.context.data, 
                    url = embed_url)
                db.session.add(sign)
                defobj.signs.append(sign)
                db.session.commit()
                return redirect(url_for('main.wordpage', title=word))
            except Exception as e:
                print(type(e))
                return 'Unexpected Error!'
    return render_template('uploadsign.html', 
        word=word, 
        definition=defobj.definition, 
        form=form,
        admin=is_admin())

@main.route("/<string:word>/<int:defid>/<int:signid>/edit", methods = ['GET', 'POST'])
def editsign(word, defid, signid):
    form = SignForm()
    defobj = Defs.query.get(defid)
    signobj = Signs.query.get(signid)
    if request.method == 'GET':
        form.gloss.data = signobj.gloss
        form.pos.data = signobj.pos
        form.url.data = signobj.url
        form.context.data = signobj.context
    if form.validate_on_submit():
        if not validate_url(form.url.data):
            form.url.errors.append("Must be a Youtube URL")
        else:
            try:
                signobj.gloss = form.gloss.data
                signobj.pos = form.pos.data
                signobj.url = form.url.data
                signobj.context = form.context.data
                db.session.commit()
                return redirect(url_for('main.wordpage', title=word))
            except Exception as e:
                print(type(e))
                return 'Unexpected Error!'
    return render_template('uploadsign.html', 
        word=word, 
        definition=defobj.definition, 
        form=form,
        admin=is_admin())

@main.route("/<string:word>/<int:defid>/<int:signid>/delete", methods = ['GET', 'POST'])
def deletesign(word, defid, signid):
    signobj = Signs.query.get(signid)
    try:
        db.session.delete(signobj)
        db.session.commit()
        return redirect(url_for('main.wordpage', title=word))
    except Exception as e:
        print(type(e))
        return 'Unexpected Error!'

@main.route('/login')
def login():
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
        adminobj = Admins.query.filter(Admins.netid.ilike(user)).first()
        print(user, " ", adminobj)
        if (adminobj != None) :
            session['admin'] = user
            return redirect(next)
        else:
            return 'User is not an admin. <a href="/logout">Return to homepage.</a>'

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