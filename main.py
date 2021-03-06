# Author: Zsolt Kébel
# Date: 26/10/2020

# pip install pynput

from pynput.keyboard import Listener, Key
from tkinter import *
from snake import *

ROWS = 20
COLUMNS = 20
score = 0


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


master = Tk()

canvas_height = (ROWS+1) * 10
canvas_width = (COLUMNS+1) * 10

canvas = Canvas(master,
                width=canvas_width,
                height=canvas_height, bg="#000")
master.resizable(False, False)

canvas.pack()

drawn_shapes = []

snake_obj = Snake()
food = new_random_coordinate(ROWS, COLUMNS, snake_obj.coordinates)
score_count = canvas.create_text(10, 20, text=str(score), fill="white", tag="score_count")
key_in_tick = None
game_over = False

# main logic =================
def perform_tick():
    global drawn_shapes, key_in_tick, food, score, score_count, canvas_height, canvas_width, game_over
#    print("Tick")

    # main logic
    # delete shapes draw in previous tick
    for shape in drawn_shapes:
        canvas.delete(shape)
    canvas.delete(score_count)

    # move snake
    snake_obj.move()
    # check if food was eaten
    # only if head is at the coordinate of a food
    if snake_obj.coordinates[0].is_the_same(food):
        snake_obj.append()
        score+=1
        # spawn new food
        food = new_random_coordinate(ROWS, COLUMNS, snake_obj.coordinates)
    for i in range(len(snake_obj.coordinates)-1):
        if snake_obj.coordinates[0].is_the_same(snake_obj.coordinates[i+1]) and len(snake_obj.coordinates)>3:
            canvas.create_text(canvas_width/2,canvas_height/2, text=f'GAME OVER\n your score is {score}', fill="white")
            game_over = True

    # reset key in tick
    key_in_tick = None

    # draw everything
    drawn_shapes = draw_points(canvas, snake_obj.coordinates)
    score_count = canvas.create_text(20, 10, text=str(score), fill="white")
    drawn_shapes.append(draw_point(canvas, food, fill="#FF0000"))

    if not game_over:
        canvas.after(200, perform_tick)


perform_tick()


def on_press(key):
    global key_in_tick

    # print("Key pressed: {0}".format(key))
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


#def on_release(key):
#    print("Key pressed")


listener = Listener(on_press=on_press, on_release=None)
listener.start()

mainloop()