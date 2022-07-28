import sqlite3
import json

from models import Comment, Post, User


def get_all_comments():

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            c.id,
            c.post_id,
            c.author_id,
            c.content
        FROM Comments c
        
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['post_id'],
                              row['author_id'], row['content'])

            comments.append(comment.__dict__)

        return json.dumps(comments)


def create_comment(new_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            (post_id, author_id, content )
        VALUES
            ( ?, ?, ?);
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content']))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)


def get_comments_by_post_id(post_id):
    """Return Comments belonging to a Post"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT * FROM Comments c
        JOIN Users u ON u.id = c.author_id
        JOIN Posts p ON p.id = c.post_id
        WHERE post_id = ?
        """, (post_id, ))

        # Initialize an empty list to hold all entry representations
        comments = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Set representations
        comments = create_from_query_dict_list(dataset)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(comments)


def create_from_query_dict_list(dataset):
    """Return list of Comment dictionary objects"""

    comments = []
    # Iterate list of data returned from database
    for row in dataset:
        # Set representations
        create_dict_with_embedded_properties_comments = create_from_query_dict_comment(
            row)

        # Add the dictionary representation of the post to the list
        comments.append(create_dict_with_embedded_properties_comments)

    return comments


def create_from_query_dict_comment(row):
    """Returns Comment dictionary object"""

    # Create a comment instance from the current row.
    # Note that the database fields are specified in
    # exact order of the parameters defined in the
    # Entry class above.
    comment = Comment(row['id'], row['post_id'],
                      row['author_id'], row['content'])

    # Create an User instance from the current row
    user = User(row['author_id'],
                row['first_name'],
                row['last_name'],
                row['email'],
                row['bio'],
                row['username'],
                row['profile_image_url'],
                row['created_on'],
                row['active'])

    # Add the dictionary representation of the user to the comment
    comment.user = user.__dict__

    # Create a Post instance from the current row
    post = Post(row['post_id'], row['title'],
                row['publication_date'], row['image_url'], row['content'], row['approved'], row['author_id'], row['category_id'])
    # Add the dictionary representation of the post to the comment
    comment.post = post.__dict__

    return comment.__dict__
