import color
from components.ai import HostileEnemy
from components.consumable import HealingConsumable
from components.fighter import Fighter
from entity import Actor, Item

player = Actor(
    char="@", 
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5)
)

orc = Actor(
    char="o", 
    color=(127, 191, 127),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3)
)

troll = Actor(
    char="T", 
    color=(63, 191, 63),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4)
)

health_potion = Item(
    char='!',
    color=(127, 0, 255),
    name="Health Potion",
    consumable=HealingConsumable(amount=5)
)