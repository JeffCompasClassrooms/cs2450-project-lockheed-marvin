import tinydb

'''
This is a user. A user is their username, password, background-color(background-color of their page),
foreground color(color of the boxes containing text, videos, etc.), text-color, flag-image-url, friends,
and favorites.
'''


#Creates a new user with username, password, and default attributes. If username != any other username,
#returns the new user. Otherwise, returns None.
def new_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    user_record = {
            'username': username,
            'password': password,
            'background-color': "#000000",
            'foreground-color': "#FFFFFF",
            'text-color': "#000000",
            'flag-image-url': "default-flag.jpg",
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

#Returns a user given just a user name.
def get_user_by_name(db, username):
    users = db.table('users')
    User = tinydb.Query()
    return users.get(User.username == username)

#Deletes the user from the database.
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

#Given a new color, and the type of color to edit, updates the color of that type to the new color.
#For color type, put in the type of color. For example: 'background-color', 'foreground-color', 'text-color'
def edit_user_colors(db, user, color, color_type):
    users = db.table('users')
    User = tinydb.Query()
    user[color_type] = color
    users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
    return 'Comment added successfully!', 'success'

#Edits the user's flag. Replaces the current flag_url with a new flag_url.
#MAKE SURE TO UPLOAD THE FLAG BEFORE ADDING THIS FUNCTION!
def edit_user_flag(db, user, flag_url):
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
    return 'Favorite {}, added successfully!'.format('favorites'[0] + ': ' + 'favorites'[1]), 'success'