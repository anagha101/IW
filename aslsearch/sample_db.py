from aslsearch import db
from aslsearch.models import Words, Defs, Signs

db.drop_all()
db.create_all()
print("Step 1: Dropped and recreated tables.")

# dummy words
word1 = Words(title = "squash")
word2 = Words(title = "dog")

db.session.add(word1)
db.session.add(word2)
db.session.commit()
print("Step 2: Added words.")

# dummy definitions
def11 = Defs(definition = "to squeeze or crush")
def12 = Defs(definition = "a game with rackets in a closed court")
def13 = Defs(definition = "a gourd vegetable")
def21 = Defs(definition = "a domesticated mammal that barks")

db.session.add(def11)
db.session.add(def12)
db.session.add(def13)
db.session.add(def21)
db.session.commit()
print("Step 3: Added definitions.")

# dummy signs
sign111 = Signs(gloss = "TO-SQUASH", pos = "verb", context = "use in reference to the squeezing of anything. See CRUSH or SQUEEZE.", url = "https://www.youtube.com/embed/gz-E13UuuwE")
sign112 = Signs(gloss = "TO-SQUASH++", pos = "progressive verb", context = "use for the active action of squeezing. See CRUSH++ or SQUEEZE++.", url = "https://www.youtube.com/embed/cLyAFNe2g1U")
sign121 = Signs(gloss = "SQUASH (sport)", pos = "noun", context = "can also sign PLAY, then fingerspell S-Q-U-A-S-H.", url = "https://www.youtube.com/embed/B57C8B22U98")
sign131 = Signs(gloss = "SQUASH (vegetable)", pos = "noun", context = "can also sign EAT, then fingerspell S-Q-U-A-S-H.", url = "https://www.youtube.com/embed/ZuifhBiMSPo")
sign211 = Signs(gloss = "DOG (formal)", pos = "noun", context = "use in reference to the animal dog in general.", url = "https://www.youtube.com/embed/xql81QmylRM")
sign212 = Signs(gloss = "DOG (informal)", pos = "noun", context = "use in reference to one's own pet dog.", url = "https://www.youtube.com/embed/jw_JtL35ZP4")


db.session.add(sign111)
db.session.add(sign112)
db.session.add(sign121)
db.session.add(sign131)
db.session.add(sign211)
db.session.add(sign212)
db.session.commit()
print("Step 4: Added signs.")

word1.definitions.extend((def11, def12, def13))
word2.definitions.append(def21)
def11.signs.extend((sign111, sign112))
def12.signs.append(sign121)
def13.signs.append(sign131)
def21.signs.extend((sign211, sign212))
db.session.commit()
print("#----------------------------------------------------------------------")

print("Sample Queries:")
#sample queries
print("Words:")
print(*Words.query.all())
print(*Words.query.filter_by(title = "dog").all())

print("Defs:")
print(*Defs.query.all())
print(*Defs.query.filter_by(definition = "to squeeze or crush").all())

print("Signs:")
print(*Signs.query.all())
print(*Signs.query.filter_by(gloss="TO-SQUASH").all())

print("Word-Def relationship test:")
print(word1.definitions)
print(word2.definitions)

print("Def-Sign relationship test:")
print(def11.signs)
print(def12.signs)
print(def13.signs)
print(def21.signs)