# ----------------------------------------------------------------------
# sample_db.py
# Author: Anagha Rajagopalan
# ----------------------------------------------------------------------
from aslsearch import db
from aslsearch.models import Admins, Words, Defs, Signs
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

# dog
w1 = Words(title = "dog")
db.session.add(w1)
d1 = Defs(definition = "a domesticated mammal that barks")
db.session.add(d1)
w1.definitions.append(d1)
s11 = Signs(gloss = "DOG", pos = "noun", context = "Primary usage.", url = "https://www.youtube.com/embed/xql81QmylRM")
s12 = Signs(gloss = "DOG", pos = "noun", context = "Common usage. Equally acceptable.", url = "https://www.youtube.com/embed/jw_JtL35ZP4")
s13 = Signs(gloss = "DOG", pos = "noun", context = "Common usage. Equally acceptable.", url = "https://www.youtube.com/embed/jw_JtL35ZP4")
s14 = Signs(gloss = "DOG", pos = "noun", context = "Comes from the Philadelphia region. Less common usage.", url = "https://www.youtube.com/embed/jw_JtL35ZP4")
s15 = Signs(gloss = "DOG", pos = "noun", context = "Comes from the South. Less common usage.", url = "https://www.youtube.com/embed/jw_JtL35ZP4")
db.session.add(s11)
db.session.add(s12)
db.session.add(s13)
db.session.add(s14)
db.session.add(s15)
d1.signs.extend((s11, s12, s13, s14, s15))
db.session.commit()

# open
w2 = Words(title = "open")
db.session.add(w2)
d21 = Defs(definition = "move or adjust to make space for access and view")
d22 = Defs(definition = "(of a person) frank and communicative nature")
d23 = Defs(definition = "(of a business) available and admitting customers")
db.session.add(d21)
db.session.add(d22)
db.session.add(d23)
w2.definitions.extend((d21, d22, d23))
s21 = Signs(gloss = "OPEN", pos = "verb", context = "Primary usage.", url = "https://www.youtube.com/embed/nUzoCPYbqqM")
s22 = Signs(gloss = "OPEN-DOOR", pos = "noun-verb pairing", context = "Same as OPEN, but understood as OPEN-DOOR in context. See DOOR for more.", url = "https://www.youtube.com/embed/SDTlfgtJKlI")
s23 = Signs(gloss = "OPEN-WINDOW", pos = "noun-verb pairing", context = "Different from OPEN. See WINDOW for more.", url = "https://www.youtube.com/embed/eNfDK2UHMvE")
s24 = Signs(gloss = "MIND-OPEN", pos = "adjective", context = "He/she/they is/are MIND-OPEN.", url = "https://www.youtube.com/embed/csw0gDBht9U")
s25 = Signs(gloss = "OPEN", pos = "adjective", context = "General sign for OPEN as a state or concept.", url = "https://www.youtube.com/embed/65jEbaQHw98")
db.session.add(s21)
db.session.add(s22)
db.session.add(s23)
db.session.add(s24)
db.session.add(s25)
d21.signs.extend((s21, s22, s23))
d22.signs.append(s24)
d23.signs.append(s25)
db.session.commit()

# door
w3 = Words(title = "door")
db.session.add(w3)
d3 = Defs(definition = "a hinged barrier at the entrance of something")
db.session.add(d3)
w3.definitions.append(d3)
s3 = Signs(gloss = "DOOR", pos = "noun", context = "Primary usage. For signs OPEN-DOOR or CLOSE-DOOR see OPEN or CLOSE respectively.", url = "https://www.youtube.com/embed/vuquufAIg7o")
db.session.add(s3)
d3.signs.append(s3)
db.session.commit()

# learn
w4 = Words(title = "learn")
db.session.add(w4)
d4 = Defs(definition = "to gain knowledge")
db.session.add(d4)
w4.definitions.append(d4)
s4 = Signs(gloss = "TO-LEARN(++)", pos = "progressive verb or gerund", context = "Sign once for learn in the past or future tense, sign twice for learn in the present tense with a finite duration or as a gerund (verb operating as a noun).", url = "https://www.youtube.com/embed/78mzpzvN9tc")
db.session.add(s4)
d4.signs.append(s4)
db.session.commit()