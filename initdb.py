import sqlite3
from sys import argv

con = sqlite3.connect(argv[1])
cur = con.cursor()

cur.execute("create table users ("
            "alias string primary key,"
            "nombre string not null,"
            "passwd string not null);")

cur.execute("create table atracciones("
            "id string primary key,"
            "localizacion int not null);")

# create a table for store a large string
cur.execute("create table mapa("
            "mapa string primary key);")

locs = {'A': 262, 'B': 367, 'C': 53, 'D': 150}
for i in locs:
    cur.execute("insert into atracciones (id,localizacion) "
                f"values ('{i}',{locs[i]} );")

con.commit()

for i in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(i)
print()
for i in cur.execute("select * from atracciones;"):
    print(i[0].encode())

con.close()
