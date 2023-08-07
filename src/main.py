#!.venv/Scripts/python
import copy
import traceback

import tcod

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon

def main() -> None:
    tcod_ver = tcod.__version__
    print('Hello, RL Dev! Using tcod version ' + tcod_ver)

    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_min_size = 6
    room_max_size = 10
    max_rooms = 40

    max_monsters_per_room = 2
    max_items_per_room = 2

    game_title = 'Yet Another Roguelike Tutorial'

    # tileset = tcod.tileset.load_tilesheet(
    #     'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
    # )

    tileset = tcod.tileset.load_tilesheet(
        'assets/terminus11x11_df_cp437.png', 16, 16, tcod.tileset.CHARMAP_CP437
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome to yet another dungeon!", color.welcome_text
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title=game_title,
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order='F')
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:   # Handle exceptions in game.
                traceback.print_exc()   # Print error to stderr
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)

if __name__ == '__main__':
    main()