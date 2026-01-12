import pyxel
from network import Network

net = Network("192.168.0.106", 12341)
board = [[""] * 3 for _ in range(3)]
winner = None

class Game:
    def __init__(self):
        pyxel.init(120, 120, title="Jogo da Velha")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        global board, winner

        # clique do mouse → envia jogada
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x // 40
            y = pyxel.mouse_y // 40
            if 0 <= x < 3 and 0 <= y < 3:
                net.send({
                    "type": "move",
                    "row": y,
                    "col": x
                })

        # recebe estado do servidor
        msg = net.receive()
        if msg:
            board = msg["board"]
            winner = msg["winner"]

    def draw(self):
        pyxel.cls(0)

        # linhas
        for i in range(1, 3):
            pyxel.line(i * 40, 0, i * 40, 120, 7)
            pyxel.line(0, i * 40, 120, i * 40, 7)

        # peças
        for y in range(3):
            for x in range(3):
                if board[y][x]:
                    pyxel.text(x * 40 + 18, y * 40 + 18, board[y][x], 7)

        if winner:
            pyxel.text(10, 110, f"Vencedor: {winner}", 8)

Game()
