import json
from socket import *

PORTA = 12341

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", PORTA))

print(f"Servidor do jogo rodando na porta {PORTA}")

board = [[""] * 3 for _ in range(3)]
players = []
current = "X"


def check_winner():
    lines = board + list(zip(*board)) + [
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)]
    ]
    for line in lines:
        if line[0] and all(cell == line[0] for cell in line):
            return line[0]
    return None

while True:
    data, addr = sock.recvfrom(4096)
    msg = json.loads(data.decode())

    # registrar jogadores
    if msg["type"] == "join" and addr not in players:
        players.append(addr)
        print(f"Jogador conectado: {addr}")

    # jogada
    if msg["type"] == "move":
        r, c = msg["row"], msg["col"]
        if board[r][c] == "":
            board[r][c] = current
            winner = check_winner()
            current = "O" if current == "X" else "X"

            resposta = {
                "board": board,
                "winner": winner
            }

            for p in players:
                sock.sendto(json.dumps(resposta).encode(), p)

