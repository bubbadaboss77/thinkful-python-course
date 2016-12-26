import os
from flask_script import Manager
import logging
import psycopg2

from blog import app

from blog.database import session, Post

# Set the log output file, and the log level
logging.basicConfig(filename="debug.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")




manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()  

from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.database import User

@manager.command
def adduser():
    """Create new user"""
    
    # User input name and email address
    name = input("Name: ")
    email = input("Email: ")
    # Test whether user already exists
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return
    
    # User input password (entered twice for verification)
    password = ""
    password_2 = ""
    # Loop while either password is empty or passwords do not match
    while not (password and password_2) or password != password_2:
        # Use builtin getpass function to input password without echoing string
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    # Create new user instance
    # Password is converted to hash - string of characters based on SHA1 hashing algorithm
    # Hashes only work one-way (password to hash string) to prevent malicious use of stored passwords
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
    
from flask.ext.migrate import Migrate, MigrateCommand
from blog.database import Base

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)    
    
  

if __name__ == "__main__":
    manager.run()