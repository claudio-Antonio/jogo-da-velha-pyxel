import os
from dotenv import load_dotenv
load_dotenv()

import pyxel
from network import Network

# ===============================
# CONFIG REDE
# ===============================
IP = os.getenv("IP")
PORTA = int(os.getenv("PORTA_SERVER"))

net = Network(IP, PORTA)

# ===============================
# ESTADOS
# ===============================
STATE_MENU = 0
STATE_GAME = 1
state = STATE_MENU

# ===============================
# DADOS DO JOGO
# ===============================
board = [[""] * 3 for _ in range(3)]
winner = None
player_symbol = None
current = None


class Game:
    def __init__(self):
        pyxel.init(120, 120, title="Jogo da Velha")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        global state, board, winner, player_symbol, current

        # ===============================
        # MENU
        # ===============================
        if state == STATE_MENU:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                state = STATE_GAME
            return

        # ===============================
        # RECEBER MENSAGENS DO SERVIDOR
        # ===============================
        msg = net.receive()
        if msg:
            if msg["type"] == "start":
                player_symbol = msg["symbol"]
                board = msg["board"]
                current = msg["current"]

            elif msg["type"] == "update":
                board = msg["board"]
                winner = msg["winner"]
                current = msg["current"]

        # ===============================
        # JOGADA
        # ===============================
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x // 40
            y = pyxel.mouse_y // 40

            if 0 <= x < 3 and 0 <= y < 3:
                net.send({
                    "type": "move",
                    "row": y,
                    "col": x
                })

    def draw(self):
        pyxel.cls(0)

        # ===============================
        # MENU
        # ===============================
        if state == STATE_MENU:
            pyxel.text(35, 45, "JOGO DA VELHA", 7)
            pyxel.text(20, 65, "Clique para iniciar", 8)
            return

        # ===============================
        # TABULEIRO
        # ===============================
        for i in range(1, 3):
            pyxel.line(i * 40, 0, i * 40, 120, 7)
            pyxel.line(0, i * 40, 120, i * 40, 7)

        # ===============================
        # PEÇAS
        # ===============================
        for y in range(3):
            for x in range(3):
                if board[y][x]:
                    pyxel.text(
                        x * 40 + 18,
                        y * 40 + 18,
                        board[y][x],
                        7
                    )

        # ===============================
        # INFO
        # ===============================
        if player_symbol:
            pyxel.text(5, 110, f"Voce: {player_symbol}", 11)

        if current:
            pyxel.text(70, 110, f"Vez: {current}", 10)

        if winner:
            pyxel.text(35, 100, f"Vencedor: {winner}", 8)


Game()
