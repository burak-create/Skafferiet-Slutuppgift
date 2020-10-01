import sqlite3 as sql
conn = sql.connect('skafferi.db')
c = conn.cursor()


def add_supply(matvaror="",mängd="",enhet=""):
    c.execute(
        "CREATE TABLE IF NOT EXISTS skafferi (skafferi_id INTEGER PRIMARY KEY  AUTOINCREMENT, matvaror, mängd, enhet)"
        )
    insert_supply = "INSERT INTO skafferi (matvaror, mängd, enhet) VALUES ('"+matvaror+"', '"+mängd+"', '"+enhet+"')"

    c.execute(insert_supply)
    conn.commit()

def list_supply():
    c.execute(
        "CREATE TABLE IF NOT EXISTS skafferi (skafferi_id INTEGER PRIMARY KEY  AUTOINCREMENT, matvaror, mängd, enhet)"
        )
    c.execute("SELECT * FROM skafferi")
    supplies = c.fetchall()

    for i in supplies:
        for k in i:
            print(k, end=" ")
        print("")

def return_supplies():
    c.execute(
        "CREATE TABLE IF NOT EXISTS skafferi (skafferi_id INTEGER PRIMARY KEY  AUTOINCREMENT, matvaror, mängd, enhet)"
        )
    c.execute("SELECT * FROM skafferi")
    supplies = c.fetchall()
    return(supplies)

def increment_supply(upp_to_date,uptSupply,uptAmount,uptUnit):
    c.execute(
        "CREATE TABLE IF NOT EXISTS skafferi (skafferi_id INTEGER PRIMARY KEY  AUTOINCREMENT, matvaror, mängd, enhet)"
        )
    uppdatedSupply = "UPDATE skafferi SET matvaror='"+uptSupply+"',mängd='"+uptAmount+"',enhet='"+uptUnit+"' WHERE skafferi_id = '"+upp_to_date+"'"
    c.execute(uppdatedSupply)
    conn.commit()

#def uppdate_supply(upp_to_date):
#    c.execute(
#        "CREATE TABLE IF NOT EXISTS pantry (skafferi_id INTEGER PRIMARY KEY  AUTOINCREMENT, matvaror, mängd, enhet)"
#        )
#    uptSupply = input("Redigera matvaran: ")
#    uptAmount = input("Redigera mängden: ")
#    uptUnit = input("Redigera enheten: ")
#    uppdatedSupply = "UPDATE pantry SET matvaror='"+uptSupply+"',mängd='"+uptAmount+"',enhet='"+uptUnit+"' WHERE skafferi_id = '"+upp_to_date+"'"
#    c.execute(uppdatedSupply)
#    conn.commit()

def delete_supply(remove):
    c.execute(
        "CREATE TABLE IF NOT EXISTS skafferi (skafferi_id INTEGER PRIMARY KEY  AUTOINCREMENT, matvaror, mängd, enhet)"
        )
    removed_supply="DELETE FROM skafferi WHERE matvaror='"+remove+"'"
    c.execute(removed_supply)
    conn.commit()

def exit():
    conn.close()
