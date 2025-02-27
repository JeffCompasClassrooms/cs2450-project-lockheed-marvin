import time
import tinydb

'''
This is a post. A post contains the username of the user that posted it, a post-id, text, a picture url, 
a video url, reactions, and comments. Note that the post_id is simply the number which the post is in the
system. The first post will be 1, second will be 2, etc.
'''

#Adds a post to the database.
#Takes in a user to get the username of the user who made the post.
#Takes in text.
#Takes in picture_url (if any).
#Takes in a video_url (if any)
#Returns the post
def add_post(db, user, post_id, text, picture_url, video_url):
    posts = db.table('posts')
    post_input = {
            'user': user['username'],
            'post-id': len(posts)+1, #Post id is simply the number post it is in the system.
            'text': text,
            'picture-url': picture_url,
            'video-url': video_url,
            'reactions': [],
            'comments': [],
            'time': time.time()
            }
    return posts.insert(post_input)

#Removes a post by post id, and then sets the other ids accordingly.
def remove_post(db, post_id):
    return_obj = None
    posts = db.table('posts')
    Post = tinydb.Query()
    return_obj = posts.remove((Post.post_id == post_id))

    #Iterates through all the posts after the removed post and decrements their post_id's by one.
    for item in posts.search(Post.post_id > post_id):
        item['post_id'] = item['post_id']-1
        posts.upsert(item)
    return return_obj

#Adds a comment to the given post
#Takes in a post, user, and content. The post is found by post_id, and then the comment is added to it.
def add_post_comment(post, user, content):
    posts = db.table('posts')
    Post = tinydb.Query()
    post['comments'].append([user['username'], content])
    posts.upsert(post, Post.post_id == post['post_id'])
    return 'Comment added successfully!', 'success'

#I'm thinking that the reactions will simply be a dictionary with numerical values
#mapped to emojis. This function takes a post_id, the post which to add the reaction to,
#and reaction, an integer from 1-6. The dictionary won't exist in this function; it will
#only exist in the functions that get the reactions to display them.
def add_post_reaction(post_id, reaction):
    posts = db.table('posts')
    Post = tinydb.Query()
    post['reactions'].append(reactions)
    posts.upsert(post, Post.post_id == post_id)
    return 'Reaction added successfully!', 'success'

#Gets all posts attached to a given user
def get_posts(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'])
