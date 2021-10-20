from ursina import *
from PIL import Image

app = Ursina()

#14,8
#70, 40
camera.position = 0,0
camera.orthographic = True

window.borderless = False
window.size = 1980,1080
window.center_on_screen()

SCALE = 0.125
squareBoard = {}
alphaNum = {

    1:"a",
    2:"b",
    3:"c",
    4:"d",
    5:"e",
    6:"f",
    7:"g",
    8:"h"

}

count, yChess = 0, 9
for y in range(7,-9,-2):
    count += 1
    yChess -= 1
    xChess = 0

    for x in range(-7,9,2):
        xChess += 1

        if count == 2:
            square = Button(model = "quad", color = color.black, position = (x/2 * SCALE, y/2 * SCALE), scale = SCALE)
            count = 1

        else:
            square = Button(model = "quad", color = color.white, position = (x/2 * SCALE, y/2 * SCALE), scale = SCALE)
            count = 2

        square.collider = "box"
        square.highlight_color = color.rgba(255,50,50,255/2)
        squareBoard[alphaNum[xChess]+str(yChess)] = square

# redSquare = Entity(position = squareBoard["a1"].position, model = "quad",color=color.red,scale = SCALE)
# x = Button(parent=squareBoard["a1"],color=color.red)


# chess_pieces = Sprite(load_texture("chess_pieces.png"), position = (0,0,-10), scale = SCALE/2)


app.run()
