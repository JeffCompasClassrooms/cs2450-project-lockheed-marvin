import tinydb

'''
This is a user. A user is their username, password, profile picture, background-color(background-color of their page),
foreground color(color of the boxes containing text, videos, etc.), text-color, flag-image-url, friends, viewability,
and favorites.
'''


#Creates a new user with username, password, and default attributes. If username != any other username,
#returns the new user. Otherwise, returns None.
#Viewability-list is a list of users whos subusers can view this user.
#View-permissions-list is a list of users who this user's secondary users can view
def new_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    user_record = {
            'username': username,
            'password': password,
            'profile_pic_url': "static/assets/default_user.jpg",
            'background-color': "#000000",
            'foreground-color': "#FFFFFF",
            'text-color': "#000000",
            'flag-image-url': "static/assets/default-flag.jpg",
            'viewability-list': [],
            'view-permissions-list': [],
            'friends': [],
            'favorites': []
            }
    return users.insert(user_record)


#Returns a user using a given username and password.
def get_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.get((User.username == username) &
            (User.password == password))

#Returns a user given just a user name. Used to display profiles.
def get_user_by_name(db, username):
    users = db.table('users')
    User = tinydb.Query()
    return users.get(User.username == username)

#Deletes the user from the database given a username and password.
#Should probably have an "are you sure?" option before calling this function.
def delete_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.remove((User.username == username) &
            (User.password == password))

#Adds a friend to the user's friends list
def add_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend not in user['friends']:
        if users.get(User.username == friend):
            user['friends'].append(friend)
            users.upsert(user, (User.username == user['username']) &
                    (User.password == user['password']))
            return 'Friend {} added successfully!'.format(friend), 'success'
        return 'User {} does not exist.'.format(friend), 'danger'
    return 'You are already friends with {}.'.format(friend), 'warning'

#Removes a friend from the user's friends list
def remove_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend in user['friends']:
        user['friends'].remove(friend)
        users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
        return 'Friend {} successfully unfriended!'.format(friend), 'success'
    return 'You are not friends with {}.'.format(friend), 'warning'

#Returns the user's friends list
def get_user_friends(db, user):
    users = db.table('users')
    User = tinydb.Query()
    friends = []
    for friend in user['friends']:
        friends.append(users.get(User.username == friend))
    return friends

#Edits the user's profile picture. Replaces the current profile_pic_url with a new profile_pic_url].
#MAKE SURE TO UPLOAD THE PROFILE PICTURE TO ASSETS BEFORE CALLING THIS FUNCTION!
def set_user_profile_picture(db, user, profile_pic_url):
    users = db.table('users')
    User = tinydb.Query()
    user['profile_pic_url'] = profile_pic_url
    users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
    return 'Profile picture {} added successfully!'.format(flag_url), 'success'

#Given a new color, and the type of color to edit, updates the color of that type to the new color.
#For color type, put in the type of color. For example: 'background-color', 'foreground-color', 'text-color'
def set_user_colors(db, user, color, color_type):
    users = db.table('users')
    User = tinydb.Query()
    user[color_type] = color
    users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
    return '{} updated successfully!'.format(color_type), 'success'

#Edits the user's flag. Replaces the current flag_url with a new flag_url.
#MAKE SURE TO UPLOAD THE FLAG TO ASSETS BEFORE CALLING THIS FUNCTION!
def set_user_flag(db, user, flag_url):
    users = db.table('users')
    User = tinydb.Query()
    user['flag_url'] = flag_url
    users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
    return 'Flag {} added successfully!'.format(flag_url), 'success'

#Takes a user and a favorite. The favorite is a tuple of (category, thing)
#For example (food, spaghetti)
def add_favorite(db, user, favorite):
    users = db.table('users')
    User = tinydb.Query()
    user['favorites'].append(favorite)
    users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
    return 'Favorite {}, added successfully!'.format(favorite[0] + ': ' + favorite[1]), 'success'

#Takes a user, mode, and sub_mode
#User is the user in the database that this function is editing
#mode is the overall mode of this change. Is this affecting the subusers of this user (view-permissions-list),
#or the subusers of other users? (viewability-list)
#sub_mode is the category of viewability that is being applied:
#friends- applied to all friends of this user
#open- applied to all users
#closed- list is empty
def set_subuser_view_permission(db, user, mode, sub_mode):
    users = db.table('users')
    User = tinydb.Query()

    if mode == "this_user":
        if sub_mode == "friends":
            for friend_username in user['friends']:
                user['viewability-list'].append(friend_username)
        elif sub_mode == "open":
            for item in users.all():
                user['viewability-list'].append(item)
        else:
            user['viewability-list'] = []
    else:
        if sub_mode == "friends":
            for friend_username in user['friends']:
                user['view-permissions-list'].append(friend_username)
        elif sub_mode == "open":
            for item in users.all():
                user['view-permissions-list'].append(item)
        else:
            user['view-permissions-list'] = []
    users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
    return return_obj
