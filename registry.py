"""
    Se encarga de registrar a los usuarios conforme las credenciales que les manden
"""
import socket
import threading
from sys import argv
import re

IP = socket.gethostbyname(socket.gethostname())
MAX_CONEXIONES = 2


def registrar(alias: str, nombre: str, passwd: str) -> bool:
    """
    TODO
    :param alias: indice y nick del usuario
    :param nombre: nombre real del usuario
    :param passwd: contrasenna de que va a usar el usuario
    :return: True/False si se ha registrado con exito o no
    """
    return True


def handle_client(conn, addr):
    HEADER = 10
    print(f"NUEVA CONEXION: {addr}")
    credentials = {'alias':'', 'name':'','passwd':''}
    for i in credentials:
        print('a')
        c_length = int(conn.recv(HEADER))
        credentials[i] = conn.recv(c_length).decode()
        print(f"recibido [{i}] = {credentials[i]}")

    print(f'registro de  {addr} - '
          f'alias:{credentials["alias"]} '
          f'nombre:{credentials["name"]} '
          f'passwd:{credentials["passwd"]}')
    if registrar(credentials["alias"], credentials["name"], credentials["passwd"]):
        print(f"REGISTRADO CON EXITO ")
        conn.send(b'ok')
    else:
        print(f"ERROR AL REGISTRAR: ")
        conn.send(b'no')
    conn.close()
    print(f"CONEXION FINALIZADA {addr}")


def repartidor(server):
    server.listen()
    print(f"ESCICHANDO EN {IP}:{PORT}")
    num_conexiones = threading.active_count() - 1
    print(f"N CONEXIONES ACTUAL: {num_conexiones}")
    while True:
        conn, addr = server.accept()
        num_conexiones = threading.active_count()
        if num_conexiones >= MAX_CONEXIONES:
            print("LIMITE DE CONEXIONES EXCEDIDO")
            conn.send(b"EL SERVIDOR HA EXCEDIDO EL LIMITE DE CONEXIONES")
            conn.close()
            num_conexiones = threading.active_count() - 1
        else:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {num_conexiones}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES - num_conexiones)


def filtra(args: list) -> bool:
    """
    Indica si el formato de los argumentos es el correcto
    :param args: Argumentos del programa
    """
    if len(args) != 2:
        print("Numero incorrecto de argumentos")
        return False

    regex_1 = '^[0-9]{1,5}$'
    if not re.match(regex_1, args[1]):
        print("Puerto incorrecta")
        return False
    return True


if __name__ == '__main__':
    if not filtra(argv):
        print("ERROR: Argumentos incorrectos")
        print("Usage: registry.py <puerto> ")
        print("Example: registry.py 5054 ")
        exit()

    PORT = int(argv[1])

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((IP, PORT))
    try:
        repartidor(serversocket)
    except Exception as e:
        print("ERROR: ", e)
    finally:
        serversocket.close()

