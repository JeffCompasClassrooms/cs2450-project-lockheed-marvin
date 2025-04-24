import flask
import os

from db import posts, users, helpers

blueprint = flask.Blueprint("posts", __name__)

# Set the allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#Function to make sure file is valid a valid type.
def allowed_file(filename, is_video):
    if is_video:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp4'
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('/post', methods=['POST'])
def post():
    """Creates a new post."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    text = flask.request.form.get('post')  # Optional text content
    picture_url = None
    video_url = None

    # Validate content: Check if at least one of the fields has content (text, picture, or video)
    if not text and 'picture' not in flask.request.files and 'video' not in flask.request.files:
        flask.flash('Please provide some content for your post (text, picture, or video).', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    # Logic to handle combinations of post content
    if not text:
        text = None

    if flask.request.files['picture'].filename:
        file = flask.request.files['picture']
        if not allowed_file(file.filename, False):
            flask.flash('Please upload only a supported image format (png, jpg, jpeg, gif).', 'danger')
            return flask.redirect(flask.url_for('login.index'))
        filepath = os.path.join("static/assets/", file.filename)
        file.save(filepath)
        picture_url = filepath
        print(f'File uploaded successfully to {filepath}')

    if flask.request.files['video'].filename:
        # Only a video
        file = flask.request.files['video']
        if not allowed_file(file.filename, True):
            flask.flash('Please upload only a supported image format (mp4).', 'danger')
            return flask.redirect(flask.url_for('login.index'))
        filepath = os.path.join("static/assets/", file.filename)
        file.save(filepath)
        video_url = filepath
        print(f'File uploaded successfully to {filepath}') 

    posts.add_post(db, user,  text, picture_url, video_url)
    # Redirect to the posts page or wherever you want after posting
    flask.flash('Post created successfully!', 'success')

    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/react/<int:post_id>', methods=['POST'])
def react(post_id):
    """Handles user reactions to a post."""
    db = helpers.load_db()

    # Get the logged-in user's session information
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if not username or not password:
        flask.flash('You need to be logged in to react.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # Get the user from the database
    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid login credentials.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # Get the reaction type (integer between 1 and 6) from the form
    reaction = flask.request.form.get('reaction_type')
    try:
        reaction = int(reaction)
    except (ValueError, TypeError):
        flask.flash('Invalid reaction type. Please choose a valid reaction.', 'danger')
        return flask.redirect(flask.url_for('posts.index'))

    # Check if the reaction is valid (1-6)
    if reaction not in REACTION_EMOJIS:
        flask.flash('Invalid reaction type. Choose a reaction between 1 and 6.', 'danger')
        return flask.redirect(flask.url_for('posts.index'))

    # Get the post to react to
    post = db.posts.find_one({"post_id": post_id})
    if not post:
        flask.flash('Post not found.', 'danger')
        return flask.redirect(flask.url_for('posts.index'))

    # Add or update the reaction for this user
    # If the user already reacted, we update their reaction, otherwise, we add a new one.
    post_reactions = post.get("reactions", [])

    # Check if the user has already reacted
    existing_reaction = next((r for r in post_reactions if r['user_id'] == user["user_id"]), None)

    if existing_reaction:
        # Update the existing reaction
        existing_reaction["reaction"] = reaction
    else:
        # Add a new reaction
        post_reactions.append({"user_id": user["user_id"], "reaction": reaction})

    # Save the updated post back to the database
    db.posts.update_one(
        {"post_id": post_id},
        {"$set": {"reactions": post_reactions}}
    )

    flask.flash(f'You reacted with {REACTION_EMOJIS[reaction]}!', 'success')
    return flask.redirect(flask.url_for('posts.index'))