For local development:

1) Clone the repository
2) Install necessary requirements using
    -pip install -r requirements.txt
3) Set up the Database:
    a) Install postgres, create a database, and update the Database URI in the config file 
        OR Change the Database URI to sqlite:///site.db
    b) Run the database script using
        -flask shell
        -from aslsearch import sample_db OR from aslsearch import stress_db
        -quit()
4) Run the app using 
    -flask run