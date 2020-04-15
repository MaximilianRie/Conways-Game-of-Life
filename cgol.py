import pyglet
from pyglet.window import key
import os.path

window = pyglet.window.Window(1350, 855)
pyglet.resource.path = [os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "res")]
pyglet.resource.reindex()
play_img = pyglet.resource.image("play.png")
stop_img = pyglet.resource.image("stop.png")
D = 15
REDUCED_HEIGHT = window.height-60
TILES_HEIGHT = REDUCED_HEIGHT//D
pyglet.gl.glClearColor(1, 1, 1, 1)
cell_batch = pyglet.graphics.Batch()
button_batch = pyglet.graphics.Batch()
NEIGHBOURS = [(0, 1), (1, 1), (-1, 1), (1, 0),
              (-1, 0), (0, -1), (1, -1), (-1, -1)]
clock = False
CLOCK_SPEED = 1/3
cells = [[{"alive":False, "n":0} for n in range(0, window.height//D)]
         for i in range(0, window.width//D)]

class Grid():
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        for x in range(1, window.width//D):
            self.batch.add(4, pyglet.graphics.GL_QUADS, None,
                           ('v2i', (x * D, 0,
                                    x * D + 1, 0,
                                    x * D + 1, REDUCED_HEIGHT,
                                    x * D, REDUCED_HEIGHT)),
                           ('c3B', (0, 0, 0) * 4)
                          )
        for y in range(1, TILES_HEIGHT+1):
            self.batch.add(4, pyglet.graphics.GL_QUADS, None,
                           ('v2i', (0, y * D,
                                    window.width, y * D,
                                    window.width, y * D + 1,
                                    0, y * D + 1)),
                           ('c3B', (0, 0, 0) * 4)
                          )

    def draw(self):
        self.batch.draw()

class LivingCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vertex_list = cell_batch.add(4, pyglet.graphics.GL_QUADS, None,
                       ('v2i', (x * D + 1, y * D + 1,
                                x * D + D, y * D + 1,
                                x * D + D, y * D + D,
                                x * D + 1, y * D + D)),
                       ('c3B', (0, 255, 0) * 4)
                      )

class Button:
    def __init__(self, img, x, y, w, h):
        self.x = x
        self.y = y
        self.img = img
        self.w = w
        self.h = h
        self.sprite = pyglet.sprite.Sprite(img=img, x=x, y=y,
                                           batch=button_batch)

class PlayButton(Button):
    def on_click(self):
        global clock
        if clock:
            self.sprite.image = play_img
            pyglet.clock.unschedule(next_gen)
        else:
            self.sprite.image = stop_img
            pyglet.clock.schedule_interval(next_gen, CLOCK_SPEED)
        clock = not clock

def next_gen(dt):
    def process_cell(x, y):
        for n in NEIGHBOURS:
            if 0 <= x+n[0] < window.width//D \
               and 0 <= y+n[1] < window.height//D \
                and cells[x+n[0]][y+n[1]]["alive"]:
                cells[x][y]["n"] += 1
    for x in range(0, window.width//D):
        for y in range(0, TILES_HEIGHT):
            process_cell(x, y)
    for x in range(0, window.width//D):
        for y in range(0, TILES_HEIGHT):
            cell = cells[x][y]
            if cell["alive"]:
                if not 1 < cell["n"] < 4:
                    cell["alive"].vertex_list.delete()
                    cell["alive"] = False
            else:
                if cell["n"] == 3:
                    cell["alive"] = LivingCell(x, y)
            cell["n"] = 0

grid = Grid()
buttons = [PlayButton(play_img, 10, window.height-45, 32, 32)]

@window.event()
def on_mouse_press(rx, ry, button, mod):
    x = rx//D
    y = ry//D
    cell = cells[x][y]
    if button == pyglet.window.mouse.LEFT and y < TILES_HEIGHT:
        if cell["alive"]:
            cell["alive"].vertex_list.delete()
            cell["alive"] = False
        else:
            cell["alive"] = LivingCell(x, y)
    elif button == pyglet.window.mouse.LEFT:
        for button in buttons:
            if button.x < rx < button.x + button.w \
               and button.y < ry < button.y + button.h:
                button.on_click()

@window.event()
def on_key_press(symbol, mod):
    if symbol == key.N:
        next_gen(0)
    if symbol == key.RETURN or symbol == key.BACKSPACE:
        buttons[0].on_click()

@window.event()
def on_draw():
    window.clear()
    grid.draw()
    cell_batch.draw()
    button_batch.draw()

pyglet.app.run()
