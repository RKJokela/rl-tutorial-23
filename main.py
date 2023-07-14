import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon

def draw_entity(console:tcod.console.Console, entity:Entity):
    console.print(x=entity.x, y=entity.y, string=entity.char, fg = entity.color)

def main() -> None:
    tcod_ver = tcod.__version__
    print('Hello, RL Dev! Using tcod version ' + tcod_ver)

    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    game_title = 'Yet Another Roguelike Tutorial'

    tileset = tcod.tileset.load_tilesheet(
        'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width, map_height)

    engine = Engine(entities, event_handler, game_map, player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title=game_title,
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order='F')
        while True:

            engine.render(root_console, context)

            events = tcod.event.wait()            
            engine.handle_events(events)

if __name__ == '__main__':
    main()