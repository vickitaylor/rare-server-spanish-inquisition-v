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
