from typing import Iterable, Any
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap

# CONSTANTS
PLAYER_VISION_RANGE = 8

class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity) -> None:
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            
            self.update_fov() # Update the FOV before the player's next action.

    def update_fov(self) -> None:
        """
        Recompute the visible area based on the player's point of view.
        """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=PLAYER_VISION_RANGE
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()