#!.venv/Scripts/python
import tcod
import copy

from engine import Engine
import entity_factories as ef
from input_handlers import EventHandler
from procgen import generate_dungeon

def main() -> None:
    tcod_ver = tcod.__version__
    print('Hello, RL Dev! Using tcod version ' + tcod_ver)

    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_min_size = 6
    room_max_size = 10
    max_rooms = 30

    max_monsters_per_room = 2

    game_title = 'Yet Another Roguelike Tutorial'

    # tileset = tcod.tileset.load_tilesheet(
    #     'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
    # )

    tileset = tcod.tileset.load_tilesheet(
        'assets/terminus11x11_df_cp437.png', 16, 16, tcod.tileset.CHARMAP_CP437
    )

    event_handler = EventHandler()

    player = copy.deepcopy(ef.player)

    game_map = generate_dungeon(max_rooms, room_min_size, room_max_size, map_width, map_height, max_monsters_per_room, player)

    engine = Engine(event_handler, game_map, player)

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