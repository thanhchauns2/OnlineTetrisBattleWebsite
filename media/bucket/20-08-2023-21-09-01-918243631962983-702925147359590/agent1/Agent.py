import numpy
import copy
from collections import Counter

ipieces = [
    [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
    [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
    [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
]
opieces = [
    [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
]
jpieces = [
    [[0, 3, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 3, 3, 3], [0, 3, 0, 0], [0, 0, 0, 0]],
    [[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 3], [0, 0, 0, 0]],
    [[0, 0, 0, 3], [0, 3, 3, 3], [0, 0, 0, 0], [0, 0, 0, 0]],
]
lpieces = [
    [[0, 0, 4, 0], [0, 0, 4, 0], [0, 4, 4, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 4, 4, 4], [0, 0, 0, 4], [0, 0, 0, 0]],
    [[0, 0, 4, 4], [0, 0, 4, 0], [0, 0, 4, 0], [0, 0, 0, 0]],
    [[0, 4, 0, 0], [0, 4, 4, 4], [0, 0, 0, 0], [0, 0, 0, 0]],
]
zpieces = [
    [[0, 5, 0, 0], [0, 5, 5, 0], [0, 0, 5, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 5, 5, 0], [5, 5, 0, 0], [0, 0, 0, 0]],
    [[0, 5, 0, 0], [0, 5, 5, 0], [0, 0, 5, 0], [0, 0, 0, 0]],
    [[0, 0, 5, 5], [0, 5, 5, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
]
spieces = [
    [[0, 0, 6, 0], [0, 6, 6, 0], [0, 6, 0, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 6, 6, 0], [0, 0, 6, 6], [0, 0, 0, 0]],
    [[0, 0, 6, 0], [0, 6, 6, 0], [0, 6, 0, 0], [0, 0, 0, 0]],
    [[6, 6, 0, 0], [0, 6, 6, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
]
tpieces = [
    [[0, 0, 7, 0], [0, 7, 7, 0], [0, 0, 7, 0], [0, 0, 0, 0]],
    [[0, 0, 0, 0], [0, 7, 7, 7], [0, 0, 7, 0], [0, 0, 0, 0]],
    [[0, 0, 7, 0], [0, 0, 7, 7], [0, 0, 7, 0], [0, 0, 0, 0]],
    [[0, 0, 7, 0], [0, 7, 7, 7], [0, 0, 0, 0], [0, 0, 0, 0]],
]

PIECES_DICT = {
    "I": ipieces,
    "O": opieces,
    "J": jpieces,
    "L": lpieces,
    "Z": zpieces,
    "S": spieces,
    "T": tpieces,
}

PIECE_NUM2TYPE = {1: "I", 2: "O", 3: "J", 4: "L", 5: "Z", 6: "S", 7: "T", 8: "G"}
PIECE_TYPE2NUM = {val: key for key, val in PIECE_NUM2TYPE.items()}
POSSIBLE_KEYS = ["I", "O", "J", "L", "Z", "S", "T"]
GRID_WIDTH = 10
GRID_DEPTH = 20

BLOCK_LENGTH = 4
BLOCK_WIDTH = 4
import numpy as np

from copy import deepcopy

import time as t
from collections import Counter


def collide(grid, block, px, py):
    feasibles = block.get_feasible()
    for pos in feasibles:
        if px + pos[0] > GRID_WIDTH - 1:  
            return True

        if px + pos[0] < 0:  
            return True

        if py + pos[1] > len(grid[0]) - 1:  
            return True

        if py + pos[1] < 0:
            continue

        if grid[px + pos[0]][py + pos[1]] != 0:
            return True

    return False

def collideDown(grid, block, px, py):
    return collide(grid, block, px, py + 1)

def collideLeft(grid, block, px, py):
    return collide(grid, block, px - 1, py)

def collideRight(grid, block, px, py):
    return collide(grid, block, px + 1, py)
def rotateCollide(grid, block, px, py):
    feasibles = block.get_feasible()

    left_most = 100
    right_most = 0
    up_most = 100
    down_most = 0

    for pos in feasibles:
        right_most = max(right_most, pos[0])
        left_most = min(left_most, pos[0])

        down_most = max(down_most, pos[1])
        up_most = min(up_most, pos[1])

    c = Counter()
    excess = len(grid[0]) - GRID_DEPTH
    for pos in feasibles:
        if px + pos[0] > 9: 
            c.update({"right": 1})

        if px + pos[0] < 0:  # left
            c.update({"left": 1})

        if py + pos[1] > len(grid[0]) - 1:
            c.update({"down": 1})


        if 0 <= px + pos[0] <= 9 and excess <= py + pos[1] <= len(grid[0]) - 1:
            if grid[px + pos[0]][py + pos[1]] != 0:
                if pos[0] == left_most:
                    c.update({"left": 1})
                elif pos[0] == right_most:
                    c.update({"right": 1})
                elif pos[1] == down_most:
                    c.update({"down": 1})
    if len(c) == 0:
        return False
    else:
        return c.most_common()[0][0]
def tspinCheck(grid, block, px, py):
    if collideDown(grid, block, px, py) == True:
        if block.block_type() == "T":
            if px + 2 < GRID_WIDTH and py + 3 < len(grid[0]):
                if (
                    grid[px][py + 1] != 0
                    and grid[px][py + 3] != 0
                    and grid[px + 2][py + 3] != 0
                ):
                    return True
                elif (
                    grid[px][py + 3] != 0
                    and grid[px + 2][py + 3] != 0
                    and grid[px + 2][py + 1] != 0
                ):
                    return True
    return False
def rotate(grid, block, px, py, _dir=1):

    block.rotate(_dir)

    collision = rotateCollide(grid, block, px, py)
    find = 0

    if collision == "left":
        y_list = [0, 1, -1]
        for s_x in range(0, 3):
            for s_y in y_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1
    elif collision == "right":
        y_list = [0, 1, -1]
        for s_x in reversed(range(-2, 0)):
            for s_y in y_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1
    elif collision == "down":
        x_list = [0, -1, 1, -2, 2]
        for s_y in reversed(range(-1, 0)):
            for s_x in x_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1

    elif collision == "up":
        x_list = [0, -1, 1, -2, 2]
        for s_y in range(1, 2):
            for s_x in x_list:
                if not find and not collide(grid, block, px + s_x, py + s_y):
                    px += s_x
                    py += s_y
                    find = 1

    if collision != False and not find:
        block.rotate(-_dir)
    tspin = 0
    if tspinCheck(grid, block, px, py) == True:
        tspin = 1
        print("Tspin rotate")

    return block, px, py, tspin
def hardDrop(grid, block, px, py):
    y = 0
    x = 0
    if collideDown(grid, block, px, py) == False:
        x = 1
    if x == 1:
        while True:
            py += 1
            y += 1
            if collideDown(grid, block, px, py) == True:
                break

    return y


class Piece(object):
    def __init__(self, _type, possible_shapes):
        self._type = _type
        self.possible_shapes = possible_shapes

        self.current_shape_id = 0

    def block_type(self):
        return self._type

    def reset(self):
        self.current_shape_id = 0

    def return_pos_color(self, px, py):
        feasibles = []

        block = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if block[x][y] > 0:
                    feasibles.append([px + x, py + y, block[x][y]])
        return feasibles

    def return_pos(self, px, py):
        feasibles = []

        block = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if block[x][y] > 0:
                    feasibles.append([px + x, py + y])
        return feasibles

    def get_feasible(self):
        feasibles = []

        b = self.now_block()

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] > 0:
                    feasibles.append([x, y])

        return feasibles

    def now_block(self):
        return self.possible_shapes[self.current_shape_id]

    def rotate(self, _dir=1):
        self.current_shape_id += _dir
        self.current_shape_id %= len(self.possible_shapes)


def typePiece(feature):
    idx = numpy.where(feature == 1)[0][0]
    return PIECE_NUM2TYPE[idx + 1]


class Grid:
    def __init__(self):
        self.grid = np.zeros((20, 10))

    def size(self):
        return 20, 10

    def update_grid(self, grid):
        self.grid = np.copy(grid)

    def project_piece_down(self, block, px, py, workingPieceIndex):
        if collide(self.grid, block, px, py):
            return None
        add_y = hardDrop(self.grid, block, px, py)
        b = block.now_block()
        excess = len(self.grid[0]) - GRID_DEPTH
        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_LENGTH):
                if b[x][y] != 0:
                    # draw ghost grid
                    if -1 < px + x < 10 and -1 < py + y + add_y - excess < 20:
                        self.grid[px + x][py + y + add_y - excess] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.grid = [
            [0 if el == -workingPieceIndex else el for el in row] for row in self.grid
        ]

    def height_of_column(self, column):
        for i in range(0, GRID_DEPTH):
            if self.grid[column][i] != 0:
                return GRID_DEPTH - i
        return 0

    def heights(self):
        result = []
        for i in range(0, GRID_WIDTH):
            result.append(self.height_of_column(i))
        return result

    def heuristics(self):
        heights = self.heights()
        return [
            self.aggregate_height(heights),
            self.complete_line(),
            self.number_of_holes(heights),
            self.bumpinesses(heights),
        ]

    def aggregate_height(self, heights):
        result = sum(heights)
        return result

    def complete_line(self):
        result = 0
        for j in range(0, GRID_DEPTH):
            check = 1
            for i in range(0, GRID_WIDTH):
                if self.grid[i][j] == 0:
                    check = 0
                    break
            result += check
        return result * result * 3

    def bumpinesses(self, heights):
        result = []
        for i in range(0, len(heights) - 1):
            result.append(abs(heights[i] - heights[i + 1]))
        return sum(result)

    def number_of_holes(self, heights):
        result = 0
        for i in range(0, GRID_WIDTH):
            for j in range(0, GRID_DEPTH):
                if self.grid[i][j] == 0 and GRID_DEPTH - j < heights[i]:
                    result += 1
        return result * 10


class Ai:
    @staticmethod
    def best(grid, workingPieces, workingPieceIndex, weights, level):
        bestRotation = None
        bestOffset = None
        bestScore = None
        workingPieceIndex = copy.deepcopy(workingPieceIndex)
        workingPiece = workingPieces[workingPieceIndex]

        for rotation in range(0, 4):
            for offset in range(-1, 9):
                result = grid.project_piece_down(workingPiece, offset, 0, level)
                if not result is None:
                    score = None
                    if workingPieceIndex == len(workingPieces) - 1:
                        heuristics = grid.heuristics()
                        score = sum([a * b for a, b in zip(heuristics, weights)])
                        
                    else:
                        _, _, score = Ai.best(
                            grid, workingPieces, workingPieceIndex + 1, weights, 2
                        )

                    if bestScore is None or score > bestScore:
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                grid.undo(level)
            rotate(grid.grid, workingPiece, 4, 0)
        return bestOffset, bestRotation, bestScore

    @staticmethod
    def choose(initialGrid, pieces, offsetX, weights, parent):
        grid = Grid()
        grid.update_grid(copy.deepcopy(initialGrid.astype(int)))
        offset, rotation, _ = Ai.best(grid, pieces, 0, weights, 1)
        offset = offset - offsetX
        for _ in range(rotation):
            parent.actions.append(3)
        for _ in range(0, abs(offset)):
            if offset > 0:
                parent.actions.append(5)
            else:
                parent.actions.append(6)
        parent.actions.append(2)


class Agent:
    def __init__(self, turn):

        self.weights = numpy.array(
             [-4.468778652706904, 9.780525320623592, -5.91742038547056, -2.740995660706888]
        )
        self.actions = []

    def choose_action(self, obs):
        if len(self.actions) == 0:
            currType = typePiece(obs[6, 10:17])
            next1Type = typePiece(obs[1, 10:17])
            return Ai.choose(
                obs[:, :10, 0].T,
                [Piece(currType, PIECES_DICT[currType]),
                Piece(next1Type, PIECES_DICT[next1Type])],
                4,
                self.weights,
                self,
            )
        return self.actions.pop(0)
