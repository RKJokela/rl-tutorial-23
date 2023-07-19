from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.
        
        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def __init__(self, dx: int, dy: int, target: Entity) -> None:
        super().__init__(dx, dy)
        self.target = target

    def perform(self, engine: Engine, entity: Entity) -> None:
        if not self.target:
            print("WARNING: MeleeAction performed with no target")
            return  # No entity to attack.
        
        print(f"You kick the {self.target.name}!")

class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        if not engine.game_map.in_bounds(dest_x, dest_y):
            print("WARNING: Tried to move out of bounds")
            return  # Destination is not out-of-bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            print("You bump into the wall.")
            return  # Destination can be walked on
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            print("INVALID CODE PATH: MovementAction is blocked by entity. Should be MeleeAction!")
            return  # Destination is blocked by an entity
        
        entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        blocking_entity = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)

        if blocking_entity:
            return MeleeAction(self.dx, self.dy, blocking_entity).perform(engine, entity)

        return MovementAction(self.dx, self.dy).perform(engine, entity)