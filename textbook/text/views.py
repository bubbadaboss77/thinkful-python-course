from flask import render_template
from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt

import gc


from . import app
from .database import session, Book
from flask import request, redirect, url_for

from flask import flash, Blueprint
from flask.ext.login import login_user, login_required, current_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from flask_security.decorators import roles_accepted

@app.route("/")
@app.route("/home")
def home_screen():
    return render_template("home.html")

PAGINATE_BY = 10

@app.route("/page/<int:page>")
def view_book(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Book).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    books = session.query(Book)
    books = books.order_by(Book.datetime.desc())
    books = books[start:end]

    return render_template("books.html",
        books=books,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
    
from flask.ext.login import current_user

@app.route("/book/add", methods=["GET"])
def add_entry_get():
    return render_template("add_book.html")

@app.route("/book/add", methods=["POST"])
@login_required
def add_book_post():
    book = Book(
        title=request.form["title"],
        subject=request.form["subject"],
        author=request.form['author'],
        owner = current_user
    )
    session.add(book)
    session.commit()
    return redirect(url_for("view_book", page=1))    

@app.route("/book/<int:id>")
def single_book(id=1):
    books = session.query(Book)
    books = books.filter(Book.id == id).all()
    return render_template("books.html",
        books=books)
 
# GET request for deleting existing post
@app.route("/book/<int:id>/delete", methods=["GET"])
@login_required
def delete_book_get(id=1):
#if owner == current_user:
    book = session.query(Book)
    book = book.filter(Book.id == id).first()
    return render_template("delete_book.html", book_title=book.title)

# POST request for deleting existing post
@app.route("/book/<int:id>/delete", methods=["POST"])
@login_required
@roles_accepted('author')
def delete_book_post(id=1):
    book = session.query(Book)
    book = book.filter(Book.id == id).first()
    session.delete(book)
    session.commit()
    return redirect(url_for("view_book"))    

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from text.database import User

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    # Test whether user already exists
    user = session.query(User).filter_by(email=email).first()
    # If user does not exist or password does not match hashed password, then redirect with error message
    if not user or not check_password_hash(user.password, password):
        # Flask 'flash' function stores message to display in page
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    
    # If username and password are correct, 
    # Use Flask-Login login_user function to use cookie to identify user in browser
    login_user(user)
    # Either access resource selected at login or go to main /posts page
    return redirect(request.args.get('next') or url_for("view_book", page=1))   

class RegistrationForm(Form):
    #username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        
        #validators.EqualTo('confirm', message='Passwords must match')
    ])
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

@app.route('/register/', methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        user = User(email=form.email.data, password=generate_password_hash(password))
        
        session.add(user)
        session.commit()
        flash('Thanks for registering')
        return redirect(url_for("login_get"))
    return render_template('register.html', form=form)
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for("home_screen"))    