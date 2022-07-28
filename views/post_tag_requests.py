import json
import sqlite3
from models import PostTag

def create_post_tags(postTagList):
    """This method will take a list of PostTag dictionaries, add them to the PostTag table"""

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        #Create empty array that will store post_tag dictionaries
        post_tags = []

        #Loop through PostTagList
        for postTag in postTagList:
            #Make SQL call for current postTag to insert into db
            db_cursor.execute("""
            INSERT INTO PostTags
                ( post_id, tag_id )
            VALUES
                ( ?, ?);
            """, (postTag['post_id'], postTag['tag_id'],))

            #Find the id for the postTag
            postTagId = db_cursor.lastrowid

            #Assign post tag id that we just got from cursor 
            postTag['id'] = postTagId

            #Add post tag dict to post_tags
            post_tags.append(postTag)

        return json.dumps(post_tags)

def get_all_post_tags():
    """ Gets all post from the database

    Returns:
        string: JSON serialized string of the contents of the categories table
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            p.id,
            p.post_id,
            p.tag_id
        FROM PostTags p
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])

            post_tags.append(post_tag.__dict__)

    return json.dumps(post_tags)