import tinydb

'''
This is a secondary user. They only have a profile picture, username, and password.
'''


#Creates a new user with username, password, and default attributes. If username != any other username,
#returns the new user. Otherwise, returns None.
def new_user(db, username, password):
    users2 = db.table('secondary-users')
    User2 = tinydb.Query()
    if users2.get(User2.username == username):
        return None
    user_record = {
            'username': username,
            'password': password,
            'profile_picture': "assets/default.jpg"
            }
    return users2.insert(user_record)

#Deletes the secondary user from the database given a username and password.
#Should probably have an "are you sure?" option before calling this function.
def delete_user(db, username, password):
    users2 = db.table('secondary-users')
    User2 = tinydb.Query()
    return users2.remove((User2.username == username) &
            (User2.password == password))