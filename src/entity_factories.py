import color
from components.ai import HostileEnemy
from components.consumable import HealingConsumable
from components.fighter import Fighter
from entity import Actor, Item

player = Actor(
    char="@", 
    color=color.player_color,
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5)
)

orc = Actor(
    char="o", 
    color=color.monster_orc,
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3)
)

troll = Actor(
    char="T", 
    color=color.monster_troll,
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4)
)

health_potion = Item(
    char='!',
    color=color.health_potion,
    name="Health Potion",
    consumable=HealingConsumable(amount=5)
)