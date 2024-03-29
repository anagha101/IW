# ----------------------------------------------------------------------
# models.py
# Author: Anagha Rajagopalan
# ----------------------------------------------------------------------
from aslsearch import db
# ----------------------------------------------------------------------

words_to_defs = db.Table("words_to_defs", 
                    db.Column('word_id', db.Integer,
                    db.ForeignKey('words.id'), primary_key=True), 
                    db.Column('def_id', db.Integer,
                    db.ForeignKey('defs.id'), primary_key=True))

defs_to_signs = db.Table("defs_to_signs",
        db.Column('def_id', db.Integer,
        db.ForeignKey('defs.id'), primary_key=True), 
        db.Column('sign_id', db.Integer, 
        db.ForeignKey('signs.id'), primary_key=True))

# ----------------------------------------------------------------------

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)

    definitions = db.relationship("Defs", secondary=words_to_defs, back_populates="word")

    def __repr__(self):
        return f"Word: '{self.title}'"

# ----------------------------------------------------------------------


class Defs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    definition = db.Column(db.Text, nullable=False)

    word = db.relationship("Words", secondary=words_to_defs, back_populates="definitions")

    signs = db.relationship("Signs", secondary=defs_to_signs, back_populates="definition")

    def __repr__(self):
        return f"Definition: '{self.definition}'"

# ----------------------------------------------------------------------

class Signs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gloss = db.Column(db.String(120), nullable=False)
    pos = db.Column(db.String(120), nullable=False)
    context = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(120), nullable=False)

    definition = db.relationship("Defs", secondary=defs_to_signs, back_populates="signs")

    def __repr__(self):
        return f"ASL gloss: '{self.gloss}'"

# ----------------------------------------------------------------------

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(120), unique=True, nullable=False)
    superadmin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Net ID: '{self.netid}'"