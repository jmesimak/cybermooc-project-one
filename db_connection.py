# -*- coding: utf-8 -*-

import sqlite3

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def query(q):
    conn = sqlite3.connect('develop')
    c = conn.cursor()
    c.execute(q)
    rows = c.fetchall()
    conn.close()
    return rows

def insert(statement, params):
    conn = sqlite3.connect('develop')
    c = conn.cursor()
    c.execute(statement, params)
    conn.commit()
    conn.close()

# Recipe:
# name
# freely formatted text (save as html, print as is)
def add_recipe(recipe):
    conn = sqlite3.connect('develop')
    c = conn.cursor()
    c.execute(
        '''
            INSERT INTO recipe (uuid, owner, title, content, image) VALUES (?, ?, ?, ?, ?)
        ''',
        [recipe['recipe_id'], recipe['owner'], recipe['title'], recipe['content'], recipe['image']]
    )
    conn.commit()
    conn.close()

def get_n_latest_recipes(n):
    conn = sqlite3.connect('develop')
    c = conn.cursor()
    c.execute("SELECT * FROM recipe")
    rows = c.fetchall()
    conn.close()
    return rows

def search_recipes(keyword=""):
    conn = sqlite3.connect('develop')
    c = conn.cursor()
    query = 'SELECT * FROM recipe where title like "{0}"'.format("%"+keyword+"%")
    print query
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows
