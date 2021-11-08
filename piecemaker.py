from PIL import Image
import os

im  = Image.open(r"chess_pieces.png")
pieces = ["king","queen","bishop","knight","rook","pawn"]

colors = ["white","black"]

left, top, right, bottom = 0, -200, 0, 0
for row in range(0,2):

    bottom += 200
    top += 200

    right, left = 0, 0

    for column in range(0,6):

        right += 200
        left = right - 200

        im1 = im.crop((left, top, right, bottom))
        if not os.path.exists("pieces/"):
            os.mkdir("pieces/")

        if not os.path.exists(f"pieces/{colors[row]}{pieces[column]}.png"):
            print(f"Creating {colors[row]}{pieces[column]}.png")
            im1.save(f"{colors[row]}{pieces[column]}.png")
            os.rename(f"{colors[row]}{pieces[column]}.png", f"pieces/{colors[row]}{pieces[column]}.png")

im.close()
