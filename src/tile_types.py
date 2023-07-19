from typing import Tuple
import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),         # True if this tile can be walked over.
        ("transparent", bool),      # True if this tile doesn't block FOV.
        ("dark", graphic_dt),       # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),      # Graphics for when this tile is in FOV.
    ]
)

def new_tile(
    *,  # Enforces use of keywords so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# Put Tile character data into constants here
# TODO: Get this from a config file instead
CHAR_SHROUD     = ord(" ")
CHAR_FLOOR      = ord(" ")
CHAR_WALL       = ord(" ")

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((CHAR_SHROUD, (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(CHAR_FLOOR, (255, 255, 255), (50, 50, 100)),
    light=(CHAR_FLOOR, (255, 255, 255), (75, 75, 150))
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(CHAR_WALL, (255, 255, 255), (25, 25, 25)),
    light=(CHAR_FLOOR, (255, 255, 255), (50, 50, 50))
)