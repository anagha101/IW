For local development:
Clone the repository
Install necessary requirements with the command pip install -r requirements.txt

Database setup:
Step 1:
Install postgres, create a databse, and update the Database URI in the config file
OR
Change the Database URI to sqlite:///site.db
Step 2:
Run the database script using:
flask shell
from aslsearch import sample_db
OR
from aslsearch import stress_db
quit()
Run the app using:
flask run
