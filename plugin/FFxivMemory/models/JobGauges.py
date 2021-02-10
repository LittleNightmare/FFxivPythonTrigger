from .MemoryParseObject import get_memory_class

RedMageGauge = get_memory_class({
    'white_mana': ('byte', 0),
    'black_mana': ('byte', 1),
})
WarriorGauge = get_memory_class({
    'beast': ('byte', 0)
})
GunbreakerGauge = get_memory_class({
    'cartridges': ('byte', 0),
    'continuationMilliseconds': ('ushort', 2),
    'continuationState': ('byte', 4)
})
DarkKnightGauge = get_memory_class({
    'blood': ('byte', 0),
    'darksideMilliseconds': ('ushort', 2),
})
