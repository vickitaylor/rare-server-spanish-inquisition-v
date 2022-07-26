import sqlite3
import json

from models import Post

def get_post_by_user(user_id):

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

    # SQL query where user_id = ?
    db_cursor.execute("""
    SELECT
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.image_url,
        p.content,
        p.approved
    FROM Posts p
    WHERE p.user_id = ?
    """, (user_id))

    posts = []
    dataset = db_cursor.fetchall()

    for row in dataset:
        post = Post(row['id'], row['title'], row['publication_date'], row['image_url'],
                    row['content'], row['approved'])
        posts.append(post.__dict__)

    return json.dumps(posts)
