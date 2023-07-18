from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def contains(self, point: Tuple[int, int]) -> bool:
        """Return true if point is inside this room."""
        x, y = point
        return (
            self.x1 < x and x < self.x2 and
            self.y1 < y and y < self.y2
        )

    def intersects(self, other: RectangularRoom) -> bool:
        """Return true if this intersects with the other RectangularRoom."""
        return (
            self.x1 <= other.x2
            and other.x1 <= self.x2
            and self.y1 <= other.y2
            and other.y1 <= self.y2
        )

def tunnel_between(
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:   # 50% chance
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist()[1:-1]:
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist()[:-1]:
        yield x, y

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int, 
    map_height: int,
    player: Entity
) -> GameMap:
    """Generate a new dungeon map"""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        room_x = random.randint(0, dungeon.width - room_width - 1)
        room_y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(room_x, room_y, room_width, room_height)

        # returns true (and discards) if the new room intersects any previous room
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        # Room is valid. Dig out its area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # Place player in first room
            player.x, player.y = new_room.center
        else:
            # Tunnel from THIS room to previous room (order matters!)
            for x, y in tunnel_between(new_room.center, rooms[-1].center):
                # Reduce redundant tunnels. If you hit a tile that's already floor (but not part of this room), end the tunnel there.
                # It's already connected to the dungeon.
                if dungeon.tiles[x, y] == tile_types.floor and not new_room.contains((x, y)):
                    break
                dungeon.tiles[x, y] = tile_types.floor
        
        rooms.append(new_room)

    return dungeon