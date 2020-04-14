import pyglet
from pyglet.window import key

window = pyglet.window.Window(1350, 855)
d = 15
pyglet.gl.glClearColor(1, 1, 1, 1)
cell_batch = pyglet.graphics.Batch()
neighbours = [(0, 1), (1, 1), (-1, 1), (1, 0),
              (-1, 0), (0, -1), (1, -1), (-1, -1)]
cells = [[{"alive":False, "n":0} for n in range(0, window.height//d)]
         for i in range(0, window.width//d)]

class Grid():
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        for x in range(1, window.width//d):
            self.batch.add(4, pyglet.graphics.GL_QUADS, None,
                           ('v2i', (x * d, 0,
                                    x * d + 1, 0,
                                    x * d + 1, window.height,
                                    x * d, window.height)),
                           ('c3B', (0, 0, 0) * 4)
                          )
        for y in range(1, window.height//d):
            self.batch.add(4, pyglet.graphics.GL_QUADS, None,
                           ('v2i', (0, y * d,
                                    window.width, y * d,
                                    window.width, y * d + 1,
                                    0, y * d + 1)),
                           ('c3B', (0, 0, 0) * 4)
                          )

    def draw(self):
        self.batch.draw()

class LivingCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vertex_list = cell_batch.add(4, pyglet.graphics.GL_QUADS, None,
                       ('v2i', (x * d + 1, y * d + 1,
                                x * d + d, y * d + 1,
                                x * d + d, y * d + d,
                                x * d + 1, y * d + d)),
                       ('c3B', (0, 255, 0) * 4)
                      )

def next_gen(dt):
    def process_cell(x, y):
        for n in neighbours:
            if 0 <= x+n[0] < window.width//d \
               and 0 <= y+n[1] < window.height//d \
               and cells[x+n[0]][y+n[1]]["alive"]:
                cells[x][y]["n"] += 1
    for x in range(0, window.width//d):
        for y in range(0, window.height//d):
            process_cell(x, y)
    for x in range(0, window.width//d):
        for y in range(0, window.height//d):
            if cells[x][y]["alive"]:
                if not 1 < cells[x][y]["n"] < 4:
                    cells[x][y]["alive"].vertex_list.delete()
                    cells[x][y]["alive"] = False
            else:
                if cells[x][y]["n"] == 3:
                    cells[x][y]["alive"] = LivingCell(x, y)
            cells[x][y]["n"] = 0

grid = Grid()

@window.event()
def on_mouse_press(rx, ry, button, mod):
    x = rx//d
    y = ry//d
    if button == pyglet.window.mouse.LEFT:
        if cells[x][y]["alive"]:
            cells[x][y]["alive"].vertex_list.delete()
            cells[x][y]["alive"] = False
        else:
            cells[x][y]["alive"] = LivingCell(x, y)

@window.event()
def on_key_press(symbol, mod):
    if symbol == key.N:
        next_gen(0)
    if symbol == key.RETURN:
        pyglet.clock.schedule_interval(next_gen, 1/3)
    if symbol == key.BACKSPACE:
        pyglet.clock.unschedule(next_gen)

@window.event()
def on_draw():
    window.clear()
    grid.draw()
    cell_batch.draw()

pyglet.app.run()
