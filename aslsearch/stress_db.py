# ----------------------------------------------------------------------
# stress_db.py
# Author: Anagha Rajagopalan
# ----------------------------------------------------------------------
from aslsearch import db
from aslsearch.models import Admins, Words, Defs, Signs
from random_word import RandomWords
# ----------------------------------------------------------------------

db.drop_all()
db.create_all()
print("Step 1: Dropped and recreated tables.")

# admins
a1 = Admins(netid = 'anaghar', superadmin = True)
a2 = Admins(netid = 'nadb', superadmin = True)
a3 = Admins(netid = 'rdondero', superadmin = False)
db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.commit()

# words
r = RandomWords()
word_list = r.get_random_words(limit=100)

for word in word_list:
    w = Words(title = word)
    db.session.add(w)
    print("Added Word!")
    for x in range (10):
        d = Defs(definition = "definition")
        db.session.add(d)
        print("Added Def!")
        w.definitions.append(d)
        for x in range (5):
            s = Signs(gloss = "gloss", pos = "noun", context = "sample", url = "https://www.youtube.com/embed/nUzoCPYbqqM")
            db.session.add(s)
            print("Added Sign!")
            d.signs.append(s)
    db.session.commit()