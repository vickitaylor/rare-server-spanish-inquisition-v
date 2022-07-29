import sqlite3
import json

from models import Tag

def get_all_tags():
    """ Gets all tags from the database

    Returns:
        string: JSON serialized string of the contents of the tags table
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            t.id,
            t.label
        FROM Tags t
        ORDER BY lower(t.label)
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)

def create_tag(new_tag):
    """Creates a new tag and adds it to the list

    Args:
        new_tag (dict): The new tag to be added

    Returns:
        dict: The tag that was added with the new id for it.
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
            ( ? );
        """, (new_tag['label'], ))

        id = db_cursor.lastrowid

        new_tag['id'] = id

    return json.dumps(new_tag)

def delete_tag(id):
    """
    Removes the selected tag from the list

    Args:
        id(int): The id of the tag to be deleted
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE from Tags
            WHERE id= ?
            """, (id, ))

def edit_tag(id, updated_tag):
    """ Updates an existing tag

    Args:
        id (int): Id of the tag being updated
        updated_tag (string): string of the updated data

    Returns:
        dict: The updated tag dictionary
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
            WHERE id = ?
        """, (updated_tag['label'], id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
