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
checked_square = None
turnCount = 0
kings = {}

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

def capture(src,dest,piece):
    chessboard[dest].enabled = False
    return True

#NOTE: board on x range (-4 to 3), on y range (-3 to 4)
def check_collision(src, dest, type): #returns true if there is no collison
    if chessboard[src] != None:
        if "knight" in chessboard[src].piece:
            return True

    if chessboard[dest] != None and chessboard[src] != None and type != "skip":
        if chessboard[src].piece[:5] == chessboard[dest].piece[:5]:
            return False

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

def check_attack(pos, ownColor, type = "skip"): #returns True if there is an attack
    for tuple in chessboard:
        piece = chessboard[tuple]
        if piece == None:
            continue

        if ownColor in piece.piece:
            continue

        piece.updateoptions((piece.x,piece.y))
        if "pawn" in piece.piece:
            if pos in piece.attackoptions:
                # print("passed in pawn")
                # print(piece.position, piece.attackoptions, pos)
                return True

        elif pos in piece.options:
            if check_collision((piece.x,piece.y), pos, type):
                return True

    return False
#NOTE: board on x range (-4 to 3), on y range (-3 to 4)
def returnAttackers(pos, ownColor, type = "skip"):
    returnList = []
    for tuple in chessboard:
        piece = chessboard[tuple]
        if piece == None:
            continue

        if ownColor in piece.piece:
            continue

        piece.updateoptions((piece.x,piece.y))
        if "pawn" in piece.piece:
            if type == "checkmate":
                for element in piece.attackoptions:
                    if element in piece.options:
                        piece.options.remove(element)

                if pos in piece.options:
                    returnList.append(piece)

            elif pos in piece.attackoptions:
                print(pos,piece.piece, (piece.x,piece.y))
                print(piece.options, piece.attackoptions)
                returnList.append(piece)

        elif pos in piece.options:
            if check_collision((piece.x,piece.y), pos, type):
                print(pos,piece.piece, (piece.x,piece.y))
                print(piece.options)
                returnList.append(piece)

    return returnList

def check_check(lastPlayed):

    global checked_square

    if lastPlayed == "white":kingcolor = "black"
    else:kingcolor = "white"

    if check_attack((kings[kingcolor].x,kings[kingcolor].y), kingcolor):
        checked_square = getsquare[kings[kingcolor].x,kings[kingcolor].y]
        checked_square.color = color.red
        if check_checkmate(kingcolor):
            print("checkmate!!")
        return True

    return False

#NOTE: board on x range (-4 to 3), on y range (-3 to 4)
def check_checkmate(kingcolor):

    global checked_square

    piece = kings[kingcolor]

    count = 0
    for x in range(-1,2):
        for y in range(-1,2):
            count += 1
            pos = get_position((piece.x,piece.y),(x,y))

            if x == 0  and y == 0:
                continue

            elif pos[0] <= -5 or pos[0] >= 4 or pos[1] >= 5 or pos[1] <= -4:
                continue

            elif chessboard[pos] != None:
                if kingcolor in chessboard[pos].piece:
                    continue

            if not check_attack(pos, kingcolor):
                return False

    attackers = returnAttackers((piece.x,piece.y), kingcolor)
    if len(attackers) == 1:
        attacker = attackers[0]
        if check_attack((attacker.x,attacker.y),attacker.piece[:5]):
            print("attacker can be captured")
            return False

        else:
            if "knight" in attacker.piece:return True
            coords = []
            vector = get_vector((attacker.x,attacker.y),(piece.x,piece.y))
            if vector[0] == vector[1]:
                for operand in range(1,vector[0]):
                    coords.append(get_position((attacker.x,attacker.y),(operand,operand)))

            elif vector[0] == 0:
                for operand in range(1,vector[1]):
                    coords.append(get_position((attacker.x,attacker.y),(0,operand)))

            elif vector[1] == 0:
                for operand in range(1,vector[0]):
                    coords.append(get_position((attacker.x,attacker.y),(operand,0)))

            else:
                print("ERROR; vector case not recognized",vector)

            for coord in coords:
                print("start")
                blockerList = returnAttackers(coord, attacker.piece[:5], "checkmate")
                if blockerList:
                    for blocker in blockerList:
                        if "king" in blocker.piece:continue
                        print(coords)
                        print(blocker.piece,blocker.x,blocker.y)
                        print("attacker can be blocked")
                        return False


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

        global whiteking
        global blackking

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
        #Makes a easy way to get the possible attack moves for pawns
        if "pawn" in picture:
            setattr(piece, "attackoptions", [])

        if "king" in picture or "rook" in picture:
            setattr(piece, "moved", False)

        else:
            setattr(piece, "moved", True)

        if "whiteking" == picture:
            kings["white"] = piece

        elif "blackking" == picture:
            kings["black"] = piece

        #Code to add options
        def updateoptions(position):
            piece.options = []
            if "white" in piece.piece:
                if "pawn" in piece.piece:
                    piece.attackoptions = []
                    if position[1] == -2:
                        piece.options.append(get_position(position,(0,2)))

                    for x in range(-1,2):
                        piece.options.append(get_position(position,(x,1)))
                        if x == 0:continue
                        piece.attackoptions.append(get_position(position,(x,1)))

            else:
                if "pawn" in piece.piece:
                    piece.attackoptions = []
                    if position[1] == 3:
                        piece.options.append(get_position(position,(0,-2)))

                    for x in range(-1,2):
                        piece.options.append(get_position(position,(x,-1)))
                        if x == 0:continue
                        piece.attackoptions.append(get_position(position,(x,-1)))


            if "rook" in piece.piece:
                for x in range(-4,4):
                    if x == position[0]:
                        continue
                    piece.options.append((x,position[1]))

                for y in range(-3,5):
                    if y == position[1]:
                        continue
                    piece.options.append((position[0],y))

            elif "knight" in piece.piece:
                for multiplier in range(-1,2,2):
                    #ERROR HERE
                    piece.options.append(get_position(position,(1 * multiplier,2 * multiplier)))
                    piece.options.append(get_position(position,(2 * multiplier,1 * multiplier)))
                    piece.options.append(get_position(position,(-2 * multiplier,1 * multiplier)))
                    piece.options.append(get_position(position,(-1 * multiplier,2 * multiplier)))

            #NOTE: board on x range (-4 to 3), on y range (-3 to 4)
            #bishops can double jump??
            elif "bishop" in piece.piece:
                for factor in range(-7,8):

                    finalpos = get_position(position,(factor,factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

                    finalpos = get_position(position,(factor,-factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

            elif "king" in piece.piece:
                for multiplier in range(-1,2,2):
                    piece.options.append(get_position(position,(1 * multiplier, 1 * multiplier)))
                    piece.options.append(get_position(position,(1 * multiplier, -1 * multiplier)))
                    piece.options.append(get_position(position,(0, 1 * multiplier)))
                    piece.options.append(get_position(position,(1 * multiplier, 0)))

            elif "queen" in piece.piece:
                for x in range(-4,4):
                    if x == position[0]:
                        continue
                    piece.options.append((x,position[1]))

                for y in range(-3,5):
                    if y == position[1]:
                        continue
                    piece.options.append((position[0],y))

                for factor in range(-7,8):

                    finalpos = get_position(position,(factor,factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

                    finalpos = get_position(position,(factor,-factor))
                    if finalpos[0] >= -4 and finalpos[0] <= 3 and finalpos[1] <= 4 and finalpos[1] >= -3:
                        piece.options.append(finalpos)

        setattr(piece,"updateoptions",updateoptions)
        #Things the code does right before dragging the piece
        def drag():
            piece.org_pos = (piece.x, piece.y)
            piece.updateoptions(piece.org_pos)

        #Things the code does right after dropping the piece
        def drop():

            global lastPawn
            global turnCount

            #The code to place the piece
            piece.x = round(piece.x)
            piece.y = round(piece.y)

            illegalMove, flag = False, False
            #checking if a pawn has moved into an empty square
            if ("white" in piece.piece and turnCount % 2 == 1) or ("black" in piece.piece and turnCount % 2 == 0):
                illegalMove = True

            elif "king" in piece.piece and abs(piece.x - piece.org_pos[0]) == 2 and piece.y - piece.org_pos[1] == 0:
                if "white" in piece.piece:
                    y = -3
                    ownColor = "white"

                else:
                    y = 4
                    ownColor = "black"

                if (piece.x - piece.org_pos[0]) == 2: #check if king side
                    x = 3
                    x2 = 1
                else:
                    x = -4
                    x2 = -1

                if not piece.moved:
                    for multiplier in range(0,3):
                        if check_attack((piece.org_pos[0] + (multiplier * x2), piece.org_pos[1]),ownColor): #testing required here
                            illegalMove = True
                            break

                    if check_collision((0,y),(x,y), "skip") and not chessboard[(x,y)].moved and not illegalMove:
                        chessboard[(0,y)] = None
                        chessboard[piece.x,piece.y] = piece

                        chessboard[(x,y)], chessboard[(x2,y)] = None, chessboard[(x,y)]
                        chessboard[(x2,y)].position = (x2,y)

                        piece.moved, flag = True, True

                    else:
                        illegalMove = True

                else:
                    illegalMove = True

            elif "pawn" in piece.piece and int(piece.org_pos[0] - piece.x) != 0 and chessboard[(piece.x,piece.y)] == None:
                if lastPawn != None and (piece.x,piece.org_pos[1]) == (lastPawn.position[0],lastPawn.position[1]): #checking if the square is near the pawn to be enpassant
                    if "white" in piece.piece and (piece.y - piece.org_pos[1]) != 1: #making sure the pawn doesnt enpassant backwards
                        illegalMove = True

                    elif "black" in piece.piece and (piece.y - piece.org_pos[1]) != -1:
                        illegalMove = True

                    else:
                        chessboard[(lastPawn.position[0],lastPawn.position[1])].enabled = False
                        chessboard[(lastPawn.position[0],lastPawn.position[1])] = None
                        chessboard[piece.x,piece.y] = piece

                        flag = True

                else:
                    illegalMove = True

            #checking if the move is not valid or if the piece has moved on itself (ie not moved)
            elif not (piece.x,piece.y) in piece.options or (piece.x,piece.y) == piece.org_pos:
                illegalMove = True

            elif piece.x <= -5 or piece.x >= 4 or piece.y >= 5 or piece.y <= -4:
                illegalMove = True

            else: #check if the move goes over a piece
                illegalMove =  not check_collision(piece.org_pos, (piece.x,piece.y), piece.piece)

            if turnCount % 2 == 1:
                lastPlayed = "black"
                toPlay = "white"

            else:
                lastPlayed = "white"
                toPlay = "black"

            if not illegalMove:
                temp1 = chessboard[piece.x,piece.y]

                chessboard[piece.x,piece.y] = piece
                chessboard[piece.org_pos] = None

                if check_check(toPlay): #check for illegal move that caused by check.
                    illegalMove = True

                if not check_check(lastPlayed) and checked_square != None and not illegalMove:
                    if (checked_square.x - .5) % 2 == 0 and (checked_square.y + .5) % 2 == 0:
                        checked_square.color = color.rgba(240,217,181,255)

                    else:
                        checked_square.color = color.rgba(181,136,99,255)



                chessboard[piece.x,piece.y] = temp1
                chessboard[piece.org_pos] = piece

                if not check_check(lastPlayed) and checked_square != None: #this evaluting after check therefore not working
                    if (checked_square.x - .5) % 2 == (checked_square.y + .5) % 2:
                        checked_square.color = color.rgba(240,217,181,255)

                    else:
                        checked_square.color = color.rgba(181,136,99,255)

            # check_self_check()
            if illegalMove: #if out of bounds or illegal
                piece.position = piece.org_pos

            elif not flag: #captures the piece and changing values in the dictionaries updating them.
                if chessboard[piece.x, piece.y] != None:
                    capture(piece.org_pos, (piece.x, piece.y), piece.piece)

                chessboard[piece.x,piece.y] = piece
                chessboard[piece.org_pos] = None


            if not illegalMove:
                turnCount += 1

                if "pawn" in piece.piece and abs(int(piece.org_pos[1] - piece.y)) == 2: #for enpassant rules
                    lastPawn = piece

                elif "king" in piece.piece or "rook" in piece.piece: #for castling rules
                    piece.moved = True

                else:
                    lastPawn = None

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
            pass

        y = 4 #For the top of the board

#Initializing the board
board = Square()
#Creating blank squares for the "look" of the baord
#NOTE: board on x range (-4 to 3), on y range (-3 to 4)
#NOTE: using colors rgba(181,136,99,255) (black) and rgba(240,217,181,255) (white)
getsquare = {} #change this to getsquare with a dict of coords and getting the square of those coords
for y in range(7,-9,-2):
    for x in range(-7,9,2):
        if ((x/2) - .5) % 2 == ((y/2) + .5) % 2:
            square = Entity(parent=board.sq_parent, position = (x/2,y/2), color = color.rgba(240,217,181,255), model = "quad")

        else:
            square = Entity(parent=board.sq_parent, position = (x/2,y/2), color = color.rgba(181,136,99,255), model = "quad")

        getsquare[(x/2-0.5,y/2 + 0.5)] = square

make_board()
app.run()
