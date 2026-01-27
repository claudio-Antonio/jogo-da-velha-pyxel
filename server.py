import json
from socket import *

PORTA = 12341

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", PORTA))

print(f"Servidor do jogo rodando na porta {PORTA}")

# ===============================
# ESTADO DO JOGO
# ===============================
board = [[""] * 3 for _ in range(3)]
players = {}        # addr -> "X" ou "O"
current = "X"
winner = None


def check_winner():
    lines = board + list(zip(*board)) + [
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)]
    ]
    for line in lines:
        if line[0] and all(cell == line[0] for cell in line):
            return line[0]
    return None


def broadcast(data):
    for addr in players:
        sock.sendto(json.dumps(data).encode(), addr)


while True:
    data, addr = sock.recvfrom(4096)
    msg = json.loads(data.decode())

    # ===============================
    # ENTRAR NO JOGO
    # ===============================
    if msg["type"] == "join":
        if addr not in players and len(players) < 2:
            symbol = "X" if "X" not in players.values() else "O"
            players[addr] = symbol

            print(f"Jogador {symbol} conectado: {addr}")

            sock.sendto(json.dumps({
                "type": "start",
                "symbol": symbol,
                "board": board,
                "current": current
            }).encode(), addr)
        continue

    # ===============================
    # JOGADA
    # ===============================
    if msg["type"] == "move":
        if addr not in players:
            continue

        symbol = players[addr]

        # só joga se for a vez dele e não acabou
        if symbol != current or winner:
            continue

        r, c = msg["row"], msg["col"]

        if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == "":
            board[r][c] = symbol
            winner = check_winner()
            current = "O" if current == "X" else "X"

            broadcast({
                "type": "update",
                "board": board,
                "winner": winner,
                "current": current
            })
