import sqlite3
import json

from models import Category

def get_all_categories():
    """ Gets all categories from the database

    Returns:
        string: JSON serialized string of the contents of the categories table
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            c.id,
            c.label
        FROM Categories c
        ORDER BY c.label
        """)

        categories = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    return json.dumps(categories)

def create_category(new_cat):
    """Creates a new category and adds it to the list

    Args:
        new_cat (dict): The new category to be added

    Returns:
        dict: The category that was added with the new id for it.
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories
            ( label )
        VALUES
            ( ? );
        """, (new_cat['label'], ))

        id = db_cursor.lastrowid

        new_cat['id'] = id

    return json.dumps(new_cat)

def delete_category(id):
    """
    Removes the selected category from the list

    Args:
        id(int): The id of the category to be deleted
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE from Categories
            WHERE id= ?
            """, (id, ))

def edit_category(id, new_category):
    """edit category method
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True