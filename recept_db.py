import sqlite3 as sql
conn = sql.connect('recept.db')
c = conn.cursor()

def add_recipe(titel="", matvaror="" , mängd="",enhet="", portion="", instruktion=""):
    c.execute(
        "CREATE TABLE IF NOT EXISTS recept (recept_id INTEGER PRIMARY KEY AUTOINCREMENT, titel, matvaror, mängd, enhet, portion, instruktion)"
    )
    insert_recipe = "INSERT INTO recept (titel, matvaror, mängd, enhet, portion, instruktion) VALUES ('"+titel+"', '"+matvaror+"', '"+mängd+"', '"+enhet+"', '"+portion+"', '"+instruktion+"')"
    c.execute(insert_recipe)
    conn.commit()


def return_recipe():
    c.execute(
        "CREATE TABLE IF NOT EXISTS recept (recept_id INTEGER PRIMARY KEY AUTOINCREMENT, titel, matvaror, mängd, enhet, portion, instruktion)"
    )
    c.execute("SELECT * FROM recept")
    recipes = c.fetchall()
    return(recipes)

def delete_recipe(remove):
    c.execute(
        "CREATE TABLE IF NOT EXISTS recept (recept_id INTEGER PRIMARY KEY AUTOINCREMENT, titel, matvaror, mängd, enhet, portion, instruktion)"
    )
    removed_recipe="DELETE FROM recept WHERE recept_id='"+remove+"'"
    c.execute(removed_recipe)
    conn.commit()

def exit():
    conn.close()

