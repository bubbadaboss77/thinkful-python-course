from flask import render_template

from . import app
from .database import session, Post
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user, login_required, current_user, logout_user, AnonymousUserMixin
from werkzeug.security import check_password_hash


PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def view_post(page=1):
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts.all()
    return render_template("posts.html",
        posts=posts,
        has_next = has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

from flask.ext.login import current_user

@app.route("/entry/add", methods=["POST"])
#login_required
def add_entry_post():
    post = Post(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("view_post"))    

@app.route("/post/<int:id>")
def single_post(id=1):
    posts = session.query(Post)
    posts = posts.filter(Post.id == id).all()
    return render_template("posts.html",
        posts=posts)

# GET request for deleting existing post
@app.route("/post/<int:id>/delete", methods=["GET"])
#login_required
def delete_post_get(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    return render_template("delete_post.html", post_title=post.title)

# POST request for deleting existing post
@app.route("/post/<int:id>/delete", methods=["POST"])
#login_required
def delete_post_delete(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    session.delete(post)
    session.commit()
    return redirect(url_for("view_post"))    

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from blog.database import User

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
    return redirect(request.args.get('next') or url_for("view_post"))   
    
# Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login_get"))    