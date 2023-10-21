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
    maze.generator = DungeonRooms(n, m)
    maze.generate()
    maze.generate_entrances()
    strmaze = str(maze)
    strmaze = strmaze.replace(" ", CHAR_IDS["open"])
    strmaze = strmaze.replace("#", CHAR_IDS["wall"])
    strmaze = strmaze.replace("E", CHAR_IDS["door"])
    strmaze = strmaze.replace("S", CHAR_IDS["wall"])
    strmaze = string_to_matrix(strmaze)
    open_coords = [
        (x, y)
        for x in range(len(strmaze))
        for y in range(len(strmaze[0]))
        if strmaze[x][y] != CHAR_IDS["wall"]
    ]
    # get all the closed coords not in the borders
    closed_coords = [
        (x, y)
        for x in range(1, len(strmaze) - 1)
        for y in range(1, len(strmaze[0]) - 1)
        if strmaze[x][y] == CHAR_IDS["wall"]
    ]
    for _ in range(ENEMY_COUNT):
        monster_x, monster_y = random.choice(closed_coords)
        strmaze[monster_x][monster_y] = CHAR_IDS["enemy"]
    for _ in range(KEY_COUNT):
        # key can't be in 0,0 0,1 1,0 1,1 if possible
        key_coords = [
            (x, y)
            for x, y in open_coords
            if x > 1 and y > 1
        ]
        if len(key_coords) == 0:
            key_coords = open_coords
        key_x, key_y = random.choice(key_coords)
        strmaze[key_x][key_y] = CHAR_IDS["key"]
        open_coords.remove((key_x, key_y))
    start_x, start_y = random.choice(open_coords)
    strmaze[start_x][start_y] = CHAR_IDS["entrance"]
    # get all the closed coords not in the borders
    closed_coords = [
        (x, y)
        for x in range(1, len(strmaze) - 1)
        for y in range(1, len(strmaze[0]) - 1)
        if strmaze[x][y] == CHAR_IDS["wall"]
    ]
    opennes = 0.1
    # set n of them to open
    closeto_open = max(1, int(opennes * len(closed_coords)))
    n_coords_to_open = random.randint(1, closeto_open)
    for _ in range(n_coords_to_open):
        x, y = random.choice(closed_coords)
        strmaze[x][y] = CHAR_IDS["open"]
        closed_coords.remove((x, y))
    return ["".join(s) for s in strmaze]


def main():
    maze = generate_maze(N, M)
    for row in maze:
        print(row)


if __name__ == "__main__":
    main()
