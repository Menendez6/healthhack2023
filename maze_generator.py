from typing import List
from mazelib import Maze
from mazelib.generate.DungeonRooms import DungeonRooms
import random

CHAR_IDS = {
    "open": " ",
    "wall": "W",
    "door": "D",
    "key": "E",
    "entrance": "S",
    "enemy": "M",
}
CHAR_COLORS = {
    CHAR_IDS["open"]: (255, 255, 255),
    CHAR_IDS["wall"]: (0, 0, 0),
}
N = 4
M = 4
ENEMY_COUNT = 1
KEY_COUNT = 1


def string_to_matrix(string: str) -> List[List[str]]:
    return [list(row) for row in string.split("\n")]


def generate_maze(n: int, m: int) -> List[List[str]]:
    maze = Maze()
    maze.generator = DungeonRooms(N, M)
    maze.generate()
    maze.generate_entrances()
    strmaze = str(maze)
    # replace " " with CHAR_IDS["open"]
    strmaze = strmaze.replace(" ", CHAR_IDS["open"])
    # replace "#" with CHAR_IDS["wall"]
    # count
    strmaze = strmaze.replace("#", CHAR_IDS["wall"])
    # replace "E" with CHAR_IDS["door"]
    strmaze = strmaze.replace("E", CHAR_IDS["door"])
    strmaze = strmaze.replace("S", CHAR_IDS["wall"])
    # get a list of all the coordinates in the grid that are not walls
    strmaze = string_to_matrix(strmaze)
    open_coords = [
        (x, y)
        for x in range(len(strmaze))
        for y in range(len(strmaze[0]))
        if strmaze[x][y] != CHAR_IDS["wall"]
    ]
    # spawn monsters on open coordinates ranodomly
    for _ in range(ENEMY_COUNT):
        monster_x, monster_y = random.choice(open_coords)
        strmaze[monster_x][monster_y] = CHAR_IDS["enemy"]
        open_coords.remove((monster_x, monster_y))
    # spawn key on open coordinates ranodomly
    for _ in range(KEY_COUNT):
        key_x, key_y = random.choice(open_coords)
        strmaze[key_x][key_y] = CHAR_IDS["key"]
        open_coords.remove((key_x, key_y))
    # define a random starting point
    start_x, start_y = random.choice(open_coords)
    # replace "S" with CHAR_IDS["entrance"]
    strmaze[start_x][start_y] = CHAR_IDS["entrance"]
    return ["".join(s) for s in strmaze]


def main():
    maze = generate_maze(N, M)
    for row in maze:
        print(row)


if __name__ == "__main__":
    main()
