# Author: Zsolt Kébel
# Date: 26/10/2020

# pip install pynput

from pynput.keyboard import Listener, Key
from tkinter import *
from snake import *
import threading

ROWS = 20
COLUMNS = 20


def draw_point(canvas: Canvas, coordinate, fill="#00FF00"):
    x1 = coordinate.column * 10
    y1 = coordinate.row * 10

    x2 = x1 + 10
    y2 = y1 + 10

    return canvas.create_rectangle(x1, y1, x2, y2, outline="#000", fill=fill)


def draw_points(canvas: Canvas, coordinates, fill="#00FF00"):
    shapes = []
    for coordinate in coordinates:
        shapes.append(draw_point(canvas, coordinate, fill=fill))

    return shapes

def make_map_for_astar():
    for i in range(ROWS):
        for j in range(COLUMNS):



master = Tk()

canvas_height = ROWS * 10
canvas_width = COLUMNS * 10

canvas = Canvas(master,
                width=canvas_width,
                height=canvas_height, bg="#000")
master.resizable(False, False)

canvas.pack()


# draw_point(canvas, coordinate=new_random_coordinate(ROWS, COLUMNS))
# draw_point(canvas, coordinate=Coordinate(20, 20))


drawn_shapes = []

snake_obj = Snake()
food = new_random_coordinate(ROWS, COLUMNS, snake_obj.coordinates)

key_in_tick = None


# main logic =================
def perform_tick():
    global drawn_shapes
    global key_in_tick
    global food

    threading.Timer(0.2, perform_tick).start()  # call this in every n seconds
    print("Tick")

    # main logic
    # delete shapes draw in previous tick
    for shape in drawn_shapes:
        canvas.delete(shape)

    # move snake
    snake_obj.move()

    # check if food was eaten
    # only if head is at the coordinate of a food
    if snake_obj.coordinates[0].is_the_same(food):
        snake_obj.append()
        # spawn new food
        food = new_random_coordinate(ROWS, COLUMNS, snake_obj.coordinates)

    # reset key in tick
    key_in_tick = None

    # draw everything
    drawn_shapes = draw_points(canvas, snake_obj.coordinates)
    drawn_shapes.append(draw_point(canvas, food, fill="#FF0000"))


perform_tick()


def on_press(key):
    global key_in_tick

    print("Key pressed: {0}".format(key))
    if key_in_tick is None:
        if key == Key.up:
            key_in_tick = key
            snake_obj.change_heading(Direction.UP)
        elif key == Key.down:
            key_in_tick = key
            snake_obj.change_heading(Direction.DOWN)
        elif key == Key.left:
            key_in_tick = key
            snake_obj.change_heading(Direction.LEFT)
        elif key == Key.right:
            key_in_tick = key
            snake_obj.change_heading(Direction.RIGHT)


def on_release(key):
    print("Key pressed")


listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

mainloop()