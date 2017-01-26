import os
from flask.ext.script import Manager

from text import app
from text.database import session, Book, User
from getpass import getpass
from werkzeug.security import generate_password_hash

from flask.ext.migrate import Migrate, MigrateCommand
from text.database import Base


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    


@manager.command
def seed():
    subject = 'Physics'
    author = 'Hong Lin'
    for i in range(25):
        book = Book(
            title="Test Book #{}".format(i),
            author = author,
            subject=subject
            
        )
        session.add(book)
    session.commit()    
    
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
    
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)    

if __name__ == "__main__":
    manager.run()