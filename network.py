import json
from socket import *

class Network:
    def __init__(self, host, porta):
        self.addr = (host, porta)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.settimeout(0.1)

        # entra no jogo
        self.send({"type": "join"})

    def send(self, data):
        self.sock.sendto(json.dumps(data).encode(), self.addr)

    def receive(self):
        try:
            data, _ = self.sock.recvfrom(4096)
            return json.loads(data.decode())
        except timeout:
            return None
