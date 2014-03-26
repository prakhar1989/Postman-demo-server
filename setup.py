from sqlite3 import dbapi2 as sqlite3
import os

DATABASE = os.path.join('postman_demo.db')

def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def setup_db():
    db = connect_db()
    with open('utils/blogschema.sql', "r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    print "---- DATABASE CLEARED ----"

if __name__ == "__main__":
    setup_db()
