# Author: Zsolt Kébel
# Date: 26/10/2020

import random
from enum import Enum

ROWS = 20
COLUMNS = 20


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Snake:
    heading = Direction.UP
    coordinates = []

    def __init__(self, body_parts=None):
        if body_parts is None:
            self.coordinates = [new_random_coordinate(ROWS, COLUMNS)]
        pass

    def change_heading(self, direction):
        if (self.heading == Direction.UP or self.heading == Direction.DOWN) and (direction == Direction.LEFT or direction == Direction.RIGHT):
            self.heading = direction
        elif (self.heading == Direction.LEFT or self.heading == Direction.RIGHT) and (direction == Direction.UP or direction == Direction.DOWN):
            self.heading = direction

    def move(self):
        prev_loc = None

        for i in range(self.length()):
            part = self.coordinates[i]

            if i == 0:
                prev_loc = part
                self.coordinates[i] = part.move_copy(self.heading)
            else:
                temp = prev_loc
                prev_loc = part
                self.coordinates[i] = temp

    def length(self):
        return len(self.coordinates)

    def append(self):
        self.coordinates.append(self.coordinates[self.length() - 1].move_copy(Direction.DOWN))

class Coordinate:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def move(self, direction):
        if direction == Direction.UP:
            if self.row == 0:
                self.row = ROWS
            else:
                self.row -= 1
        elif direction == Direction.DOWN:
            if self.row == ROWS:
                self.row = 0
            else:
                self.row += 1
        elif direction == Direction.LEFT:
            if self.column == 0:
                self.column = COLUMNS
            else:
                self.column -= 1
        elif direction == Direction.RIGHt:
            if self.column == COLUMNS:
                self.column = 0
            else:
                self.column += 1

    # move and copy
    def move_copy(self, direction):
        row = self.row
        col = self.column

        if direction == Direction.UP:
            if self.row == 0:
                row = ROWS
            else:
                row -= 1
        elif direction == Direction.DOWN:
            if self.row == ROWS:
                row = 0
            else:
                row += 1
        elif direction == Direction.LEFT:
            if self.column == 0:
                col = COLUMNS
            else:
                col -= 1
        elif direction == Direction.RIGHT:
            if self.column == COLUMNS:
                col = 0
            else:
                col += 1

        return Coordinate(row, col)

    def is_the_same(self, coordinate):
        return self.row == coordinate.row and self.column == coordinate.column


def new_random_coordinate(rows, columns, exclude=None):
    if exclude is None:
        exclude = []
    x = random.randint(0, rows)
    y = random.randint(0, columns)

    for coordinate in exclude:
        if x == coordinate.row and y == coordinate.column:
            return new_random_coordinate(rows, columns, exclude)

    return Coordinate(x, y)


class BodyPart(Coordinate):
    def __init__(self, row, column, direction):
        super().__init__(row, column)
        self.direction = direction
