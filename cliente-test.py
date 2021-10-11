import socket

PORT = 4040
IP = socket.gethostbyname(socket.gethostname())


class Cliente:
    def __init__(self, ip, port):
        self.mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.ip = ip

    def connect(self):
        try:
            self.mi_socket.connect((self.ip, self.port))
        except Exception as e:
            print("Error al conectar: ", e)

    def send(self, msg):
        try:
            self.mi_socket.send(msg.encode())
        except Exception as e:
            print("Error al enviar: ", e)

    def close(self):
        self.send("FIN")
        self.mi_socket.close()
        print("SOCKET CERRADO")


if __name__ == "__main__":
    o = ""
    c = Cliente(IP, PORT)
    c.connect()
    while o != "FIN":
        o = input(" > ")
        c.send(o)
    c.close()
