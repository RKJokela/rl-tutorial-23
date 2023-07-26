from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from engine import Engine

# TODO: Put keybindings in a settings file for customizing. Later, allow them to be changed from in-game.

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue
            
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.KP_8:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.KP_2:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.KP_4:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.KP_6:
            action = BumpAction(player, dx=1, dy=0)

        # Diagonal Movements
        elif key == tcod.event.KeySym.KP_7:         # UPLEFT
            action = BumpAction(player, dx=-1, dy=-1)
        elif key == tcod.event.KeySym.KP_9:         # UPRIGHT
            action = BumpAction(player, dx=1, dy=-1)
        elif key == tcod.event.KeySym.KP_1:         # DOWNLEFT
            action = BumpAction(player, dx=-1, dy=1)
        elif key == tcod.event.KeySym.KP_3:         # DOWNRIGHT
            action = BumpAction(player, dx=1, dy=1)

        # Wait in place
        # elif key == tcod.event.KeySym.KP_5:
        #     action = TODO_WaitAction()

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        # No valid key was pressed
        return action