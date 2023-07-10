from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

# TODO: Put keybindings in a settings file for customizing. Later, allow them to be changed from in-game.

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.KP_8:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.KP_2:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.KP_4:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.KP_6:
            action = MovementAction(dx=1, dy=0)

        # Diagonal Movements
        elif key == tcod.event.KeySym.KP_7:         # UPLEFT
            action = MovementAction(dx=-1, dy=-1)
        elif key == tcod.event.KeySym.KP_9:         # UPRIGHT
            action = MovementAction(dx=1, dy=-1)
        elif key == tcod.event.KeySym.KP_1:         # DOWNLEFT
            action = MovementAction(dx=-1, dy=1)
        elif key == tcod.event.KeySym.KP_3:         # DOWNRIGHT
            action = MovementAction(dx=1, dy=1)

        # Wait in place
        # elif key == tcod.event.KeySym.KP_5:
        #     action = TODO_WaitAction()

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action