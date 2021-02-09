from .MemoryParseObject import get_memory_class

RedMageGauge=get_memory_class({
    'white_mana':('byte',0),
    'black_mana': ('byte', 1),
})
WarriorGauge=get_memory_class({
    'beast':('byte',0)
})
