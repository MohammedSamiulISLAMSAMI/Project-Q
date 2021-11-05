from PIL import Image
import os

im  = Image.open(r"chess_pieces.png")
piece = ["king","queen","bishop","knight","rook","pawn"]
color = ["white","black"]

left, top, right, bottom = 0, -200, 0, 0
for row in range(0,2):

    bottom += 200
    top += 200

    right, left = 0, 0

    for column in range(0,6):

        right += 200
        left = right - 200

        print(left, top, right, bottom)

        im1 = im.crop((left, top, right, bottom))

        if not os.path.exists(f"pieces/{color[row]}{piece[column]}.png"):

            im1.save(f"{color[row]}{piece[column]}.png")
            os.rename(f"{color[row]}{piece[column]}.png", f"pieces/{color[row]}{piece[column]}.png")
