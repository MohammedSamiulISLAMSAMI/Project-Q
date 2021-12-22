from ursina import *
from PIL import Image
import piecemaker

app = Ursina()
#every square is 5x5 px
camera.position = 0,0,-1000
camera.orthographic = True

window.borderless = False
window.size = 1980,1080
window.center_on_screen()

lastPawn = None

chessboard = {}
for x in range(-4,4):
    for y in range(-3,5):
        chessboard[(x,y)] = None

def get_position(src, vector):
    finalpos = (vector[0] + src[0], vector[1] + src[1])
    return finalpos

def get_vector(src, dest):
    vector = (int(dest[0] - src[0]), int(dest[1] - src[1]))
    return vector

def check_collision(src, dest, piece):

    if chessboard[dest] != None:
        chessboard[dest].enabled = False

    if "knight" in piece:
        return True

    vector = get_vector(src,dest)
    step = 1

    if vector[0] == 0:
        if vector[1] < 0:step = -1

        for y in range(1*step,vector[1],step):
            checkTuple = src[0],src[1]+y

            if chessboard[checkTuple] != None:
                return False

    elif vector[1] == 0:
         if vector[0] < 0:step = -1

         for x in range(1*step,vector[0],step):
             checkTuple = src[0]+x,src[1]

             if chessboard[checkTuple] != None:
                 return False

    elif abs(vector[0]) == abs(vector[1]):
        stepx, stepy = 1, 1
        if vector[0] < 0:stepx = -1
        if vector[1] < 0:stepy = -1

        for x in range(1,abs(vector[0])):
            checkTuple = src[0] + (x * stepx), src[1] + (x * stepy)
            if chessboard[checkTuple] != None:
                return False

    else:
        print("ERROR; vector case not recognized",vector)

    # print(f"Source: {src}, Dest: {dest}, Vector: {vector}")
    return True

#The class for the board.
class Square(Entity):

    #The initializing of the 8x8 skeleton of the board
    def __init__(self):
        super().__init__(
            model = 'quad',
            scale = 40,
            texture = 'white_cube',
            texture_scale = (8,8),
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

        chessboard[coord] = piece

        #Makes a easy way to get the piece type
        setattr(piece, "piece", picture)
        #Makes a easy way to get the possible moves
        setattr(piece, "options", [])

        #Code to add options
        def updateoptions():
            piece.options = []
            if "white" in piece.piece:
                if "pawn" in piece.piece:
                    if piece.org_pos[1] == -2:
                        piece.options.append(get_position(piece.org_pos,(0,2)))

                    for x in range(-1,2):
                        piece.options.append(get_position(piece.org_pos,(x,1)))

            else:
                if "pawn" in piece.piece:
                    if piece.org_pos[1] == 3:
                        piece.options.append(get_position(piece.org_pos,(0,-2)))

                    for x in range(-1,2):
                        piece.options.append(get_position(piece.org_pos,(x,-1)))


            if "rook" in piece.piece:
                for x in range(-4,4):
                    if x == piece.org_pos[0]:
                        continue
                    piece.options.append((x,piece.org_pos[1]))

                for y in range(-3,5):
                    if y == piece.org_pos[1]:
                        continue
                    piece.options.append((piece.org_pos[0],y))

            elif "knight" in piece.piece:
                for multiplier in range(-1,2,2):
                    #ERROR HERE
                    piece.options.append(get_position(piece.org_pos,(1 * multiplier,2 * multiplier)))
                    piece.options.append(get_position(piece.org_pos,(2 * multiplier,1 * multiplier)))
                    piece.options.append(get_position(piece.org_pos,(-2 * multiplier,1 * multiplier)))
                    piece.options.append(get_position(piece.org_pos,(-1 * multiplier,2 * multiplier)))

            #NOTE: board on x range (-4 to 3), on y range (-3 to 4)
            #bishops can double jump??
            elif "bishop" in piece.piece:
                for factor in range(-7,8):

                    finalpos = get_position(piece.org_pos,(factor,factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

                    finalpos = get_position(piece.org_pos,(factor,-factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

            elif "king" in piece.piece:
                for multiplier in range(-1,2,2):
                    piece.options.append(get_position(piece.org_pos,(1 * multiplier, 1 * multiplier)))
                    piece.options.append(get_position(piece.org_pos,(1 * multiplier, -1 * multiplier)))
                    piece.options.append(get_position(piece.org_pos,(0, 1 * multiplier)))
                    piece.options.append(get_position(piece.org_pos,(1 * multiplier, 0)))

            elif "queen" in piece.piece:
                for x in range(-4,4):
                    if x == piece.org_pos[0]:
                        continue
                    piece.options.append((x,piece.org_pos[1]))

                for y in range(-3,5):
                    if y == piece.org_pos[1]:
                        continue
                    piece.options.append((piece.org_pos[0],y))

                for factor in range(-7,8):

                    finalpos = get_position(piece.org_pos,(factor,factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

                    finalpos = get_position(piece.org_pos,(factor,-factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

        #Things the code does right before dragging the piece
        def drag():
            piece.org_pos = (piece.x, piece.y)
            updateoptions()

        #Things the code does right after dropping the piece
        def drop():

            global lastPawn

            #The code to place the piece
            piece.x = round(piece.x)
            piece.y = round(piece.y)

            illegalMove = False
            if "pawn" in piece.piece and int(piece.org_pos[0] - piece.x) != 0 and chessboard[(piece.x,piece.y)] == None:
                if lastPawn != None and (piece.x,piece.org_pos[1]) == (lastPawn.position[0],lastPawn.position[1]):
                    chessboard[(lastPawn.position[0],lastPawn.position[1])].enabled = False
                else:
                    illegalMove = True

            elif not (piece.x,piece.y) in piece.options or (piece.x,piece.y) == piece.org_pos:
                illegalMove = True

            else:
                illegalMove =  not check_collision(piece.org_pos, (piece.x,piece.y), piece.piece)

            if piece.x <= -5 or piece.x >= 4 or piece.y >= 5 or piece.y <= -4 or illegalMove:
                piece.position = piece.org_pos

            else:
                chessboard[piece.x,piece.y] = piece
                chessboard[piece.org_pos] = None

                if "pawn" in piece.piece and abs(int(piece.org_pos[1] - piece.y)) == 2:
                    lastPawn = piece
                    print(lastPawn)

                else:
                    lastPawn = None
                    print(lastPawn)



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

        if color == "white":
            y += 1
        else:
            y -= 1

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
