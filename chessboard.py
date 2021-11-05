from ursina import *
from PIL import Image
app = Ursina()
camera.position = 0,0,-1000
camera.orthographic = True

window.borderless = False
window.size = 1980,1080
window.center_on_screen()

SCALE = 40

class Square(Entity):
    def __init__(self):
        super().__init__(
            model = 'quad',
            scale = SCALE,
            texture = 'white_cube',
            texture_scale = (8,8),
            # color = color.red,
            )

        self.sq_parent = Entity(parent=self, scale=(1/8,1/8))

    def append(self,item):
        global piece
        piece = Draggable(
            parent = board.sq_parent,
            model = "quad",
            texture = load_texture("whiteking.png"),
            color = color.white,
            origin = (-.5,.5),
            z = -10,
        )

        def drag():
            piece.org_pos = (piece.x, piece.y)

        def drop():
            piece.x = round(piece.x)
            piece.y = round(piece.y)

            if piece.x <= -5 or piece.x >= 4 or piece.y >= 5 or piece.y <= -4:
                piece.position = (piece.org_pos)
                return

        piece.drag = drag
        piece.drop = drop


board = Square()

count, yChess = 0, 9
for y in range(7,-9,-2):
    count += 1
    yChess -= 1
    xChess = 0

    for x in range(-7,9,2):
        xChess += 1

        if count == 2:
            square = Entity(parent=board.sq_parent, position = (x/2,y/2), color = color.black, model = "quad")
            count = 1

        else:
            square = Entity(parent=board.sq_parent, position = (x/2,y/2), color = color.white, model = "quad")
            count = 2

board.append("test")
def update():print(piece.position)
app.run()
