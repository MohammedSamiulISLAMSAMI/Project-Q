from ursina import *

app = Ursina()

#14,8
#x, 40
camera.position = 0,0
camera.orthographic = True

window.borderless = False
window.size = 1980,1080
window.center_on_screen()

SCALE = 5

count = 0
for y in range(7,-9,-2):
    count += 1

    for x in range(-7,9,2):

        if count == 2:
            square = Entity(model = "quad", color = color.black, position = (x/2 * SCALE, y/2 * SCALE), scale = SCALE)
            count = 1

        else:
            square = Entity(model = "quad", color = color.white, position = (x/2 * SCALE, y/2 * SCALE), scale = SCALE)
            count = 2

app.run()
