from ursina import *
from PIL import Image
import piecemaker

app = Ursina()
camera.position = 0,0,-1000
camera.orthographic = True

window.borderless = False
window.size = 1980,1080
window.center_on_screen()

chessboard = []

#The class for the board.
class Square(Entity):

    #The initializing of the 8x8 skeleton of the board
    def __init__(self):
        super().__init__(
            model = 'quad',
            scale = 40,
            texture = 'white_cube',
            texture_scale = (8,8)
            )

        #Information of the initialized class so we can parent it, and scale it accordingly
        self.sq_parent = Entity(parent=self, scale=(1/8,1/8))

    #Code to add a draggable piece easily
    def add(self,picture,coord):
        piece = Draggable(
            parent = board.sq_parent,
            model = "quad",
            texture = load_texture(picture),
            color = color.white,
            origin = (-.5,.5),
            z = -10,
            position = coord
        )

        #Things the code does right before dragging the piece
        def drag():
            piece.org_pos = (piece.x, piece.y)

        #Things the code does right after dropping the piece
        def drop():

            #The code to place the piece
            piece.x = round(piece.x)
            piece.y = round(piece.y)

            if piece.x <= -5 or piece.x >= 4 or piece.y >= 5 or piece.y <= -4:
                piece.position = (piece.org_pos)

        piece.drag = drag
        piece.drop = drop

def make_board():

    y = -3 #For the bottom of the board

    #Twice for each color
    for color in piecemaker.colors:

        #Adding the pieces to the board.
        board.add(f"{color}rook",(-4,y))
        board.add(f"{color}knight",(-3,y))
        board.add(f"{color}bishop",(-2,y))
        board.add(f"{color}queen",(-1,y))
        board.add(f"{color}king",(0,y))
        board.add(f"{color}bishop",(1,y))
        board.add(f"{color}knight",(2,y))
        board.add(f"{color}rook",(3,y))

        if color == "white":y += 1
        else:y -= 1

        for x in range(-4,4):
            board.add(f"{color}pawn",(x,y))

        y = 4 #For the top of the board

#Initializing the board
board = Square()

#Creating blank squares for the "look" of the baord
#NOTE: board on x range (-4 to 3), on y range (-3 to 4)
#NOTE: using colors rgba(181,136,99,255) (black) and rgba(240,217,181,255) (white)
count, yChess = 0, 9
for y in range(7,-9,-2): #The amount of rows
    count += 1
    yChess -= 1
    xChess = 0

    for x in range(-7,9,2): #The amount of columns
        xChess += 1

        if count == 2: #Creating the black squares
            square = Entity(parent=board.sq_parent, position = (x/2,y/2), color = color.rgba(240,217,181,255), model = "quad")
            count = 1

        else: #Creating the white squares
            square = Entity(parent=board.sq_parent, position = (x/2,y/2), color = color.rgba(181,136,99,255), model = "quad")
            count = 2


make_board()
app.run()
