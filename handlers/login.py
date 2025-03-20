import flask
import random
from flask import request
import ipinfo
from handlers import copy
from db import posts, users, helpers

blueprint = flask.Blueprint("login", __name__)

country_codes = ["US", "BO", "NL", "TM", "AU", "ZW", "KR", "CN", "RU", "CR", "MA", "GQ", "BR"]

@blueprint.route('/loginscreen')
def loginscreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()

    # First check if already logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title, subtitle=copy.subtitle)

@blueprint.route('/login', methods=['POST'])
def login():
    """Log in the user.

    Using the username and password fields on the form, create, delete, or
    log in a user, based on what button they click.
    """
    db = helpers.load_db()

    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    if username == login and password == login:
        resp = flask.make_response(flask.redirect(flask.url_for('login.logout')))
    resp.set_cookie('username', username)
    resp.set_cookie('password', password)

    submit = flask.request.form.get('type')
    if submit == 'Create':
        # Check if the user exists in the secondary_users table, since only secondary users can create an account
        if users.new_user(db, username, password, users.get_user_by_cc(db, country_codes[random.randrange(0, len(country_codes))])) is None:
            flask.flash('Username {} already taken!'.format(username), 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
        flask.flash('User {} created successfully!'.format(username), 'success')

    elif submit == 'Login':
        user = users.get_user(db, username, password)

        if user:
            flask.flash(f'Welcome back, {username}!', 'success')
            return flask.redirect(flask.url_for('login.index'))
        else:
            flask.flash('Invalid username or password. Please try again.', 'danger')

    return resp

@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/')
def index():
    """Serves the main feed page for the user."""
    db = helpers.load_db()

    # Make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    flask.flash("Username is: {}".format(username), 'danger')
    flask.flash("Password is: {}".format(password), 'danger')

    if username is None or password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))


    user = users.get_user(db, username, password)
    flask.flash("User {} found!".format(user), 'success')
    if not user:
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    # Get the info for the user's feed
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    
    # Sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('feed.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts)