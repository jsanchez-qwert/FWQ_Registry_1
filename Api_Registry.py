import requests as req
import sys
import json
import socket
import sqlite3
from flask import Flask, request, jsonify
import hashlib

"""
def login(alias, passwd) -> bool::
def modificar(alias, passwd, n_alias, n_nombre, n_passwd) -> bool:
def registrar(alias: str, nombre: str, passwd: str) -> bool:
"""

app = Flask(__name__)
api = req.session()
DATABASE = sys.argv[2]

def registrar(alias: str, nombre: str, passwd: str) -> bool:
    """
    :param alias: indice y nick del usuario
    :param nombre: nombre real del usuario
    :param passwd: contrasenna de que va a usar el usuario
    :return: True/False si se ha registrado con exito o no
    """
    final = True
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    # hash the password
    passwd = hashlib.sha256(passwd.encode()).hexdigest()



    sql_comand = f"insert into users (alias, nombre, passwd)" \
                 f" values ('{alias}','{nombre}','{passwd}');"
    try:
        cur.execute(sql_comand)
        con.commit()
        print(f"REGISTRADO CON EXITO ")
    except Exception as e:
        print("ERROR al registrar", e)
        final = False
    finally:
        con.close()
        return final


def login(alias, passwd):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    sol = False
    passwd = hashlib.sha256(passwd.encode()).hexdigest()
    for _ in cur.execute(f"select * from users "
                         f"where "
                         f"alias like '{alias}' and "
                         f"passwd like '{passwd}' ;"):
        sol = True
    con.close()
    return sol


def modificar(alias, passwd, n_alias, n_nombre, n_passwd) -> bool:
    passwd = hashlib.sha256(passwd.encode()).hexdigest()
    n_passwd = hashlib.sha256(n_passwd.encode()).hexdigest()

    final = True
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    print("actualizando")
    try:
        if n_alias != '':
            cur.execute(
                f"update users set alias = '{n_alias}' where alias like '{alias}';"
            )
            alias = n_alias
            print("actualizado alias")
        if n_nombre != '':
            cur.execute(
                f"update users set nombre = '{n_nombre}' where alias like '{alias}';"
            )
            print("actualizado nombre")
        if n_passwd != '':
            cur.execute(
                f"update users set passwd = '{n_passwd}' where alias like '{alias}';"
            )
            print("actualizado passwd")
        print("antes del commit")
        con.commit()
        print(f"ACTUALIZADO CON EXITO ")
    except Exception as e:
        print("ERROR al updatear", e)
        final = False
    finally:
        con.close()
        return final


@app.route('/login', methods=['POST'])
def login_api():
    data = request.get_json()
    alias = data['alias']
    passwd = data['passwd']
    print(f"alias: {alias} ", f"passwd: {passwd}")
    return 'ok'


@app.route('/modificar', methods=['POST'])
def modificar_api():
    data = request.get_json()
    alias = data['alias']
    passwd = data['passwd']
    n_alias = data['n_alias']
    n_nombre = data['n_nombre']
    n_passwd = data['n_passwd']
    print(f"Modificando usuario, alias: {alias} ", f"passwd: {passwd}")
    print(f"n_alias: {n_alias} ", f"n_nombre: {n_nombre} ", f"n_passwd: {n_passwd}")
    if not login(alias, passwd):
        return 'El usuario que se intenta modificar no existe'
    if modificar(alias, passwd, n_alias, n_nombre, n_passwd):
        return 'ok'
    return "Error al modificar"


@app.route('/registrar', methods=['POST'])
def registrar_api():
    data = request.get_json()
    print(f"data: {data}")
    alias = data['alias']
    nombre = data['nombre']
    passwd = data['passwd']
    if registrar(alias, nombre, passwd):
        return 'ok'
    else:
        return 'El usuario que se intenta registrar ya existe'

@app.route('/', methods=['GET'])
def index():
    return 'API_Registry.py mensaje de bienvenida'

if __name__ == '__main__':
    m_port = sys.argv[1]
    # get the ip of the machine
    IP = socket.gethostbyname(socket.gethostname())
    
    cert_path = './cert.pem'
    context = (cert_path, './key.pem')
    print("Running in port: " + m_port)
    app.run(debug=True, port=m_port, ssl_context=context, host=IP)
    print('Finalizado')
