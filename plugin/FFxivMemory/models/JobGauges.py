from .MemoryParseObject import get_memory_class, get_memory_array
from enum import Enum

RedMageGauge = get_memory_class({
    'white_mana': ('byte', 0),
    'black_mana': ('byte', 1),
})
WarriorGauge = get_memory_class({
    'beast': ('byte', 0)
})
GunbreakerGauge = get_memory_class({
    'cartridges': ('byte', 0),
    'continuationMilliseconds': ('ushort', 2),  # Is 15000 if and only if continuationState is not zero.
    'continuationState': ('byte', 4)
})
DarkKnightGauge = get_memory_class({
    'blood': ('byte', 0),
    'darksideMilliseconds': ('ushort', 2),
})
PaladinGauge = get_memory_class({
    'oath': ('byte', 0),
})


class BardGauge(get_memory_class({
    'songMilliseconds': ('ushort', 0),
    'songProcs': ('byte', 2),
    'soulGauge': ('byte', 3),
    'songType': ('byte', 4)
})):
    class Song(Enum):
        none = 0
        ballad = 5  # Mage's Ballad.
        paeon = 10  # Army's Paeon.
        minuet = 15  # The Wanderer's Minuet.


class DancerGauge(get_memory_class({
    'feathers': ('byte', 0),
    'step': (get_memory_array('byte', 1, 4, 0), 2),
    'currentStep': ('byte', 6)
})):
    class Step(Enum):
        none = 0
        emboite = 1
        entrechat = 2
        jete = 3
        pirouette = 4


class DragoonGauge(get_memory_class({
    'blood_or_life_ms': ('ushort', 0),
    'stance': ('byte', 2),  # 0 = None, 1 = Blood, 2 = Life
    'eyesAmount': ('byte', 3),
})):
    @property
    def bloodMilliseconds(self):
        return self.blood_or_life_ms if self.stance == 1 else 0

    @property
    def lifeMilliseconds(self):
        return self.blood_or_life_ms if self.stance == 2 else 0


NinjaGauge = get_memory_class({
    'hutonMilliseconds': ('uint', 0),
    'ninkiAmount': ('byte', 4),
    'hutonCount': ('byte', 5),
})

ThaumaturgeGauge = get_memory_class({
    'umbralMilliseconds': ('ushort', 2),  # Number of ms left in umbral fire/ice.
    'umbralStacks': ('sbyte', 4),  # Positive = Umbral Fire Stacks, Negative = Umbral Ice Stacks.
})


class BlackMageJobMemory(get_memory_class({
    'nextPolyglotMilliseconds': ('ushort', 0),
    'umbralMilliseconds': ('ushort', 2),
    'umbralStacks': ('sbyte', 4),
    'umbralHearts': ('byte', 5),
    'foulCount': ('byte', 6),
    'enochain_state': ('byte', 7),
})):
    @property
    def enochain_active(self):
        return self.enochain_state & 1 != 0

    @property
    def polygot_active(self):
        return self.enochain_state & 1 << 1 != 0


WhiteMageGauge = get_memory_class({
    'lilyMilliseconds': ('ushort', 2),
    'lilyStacks': ('byte', 4),
    'bloodlilyStacks': ('byte', 5),
})

ArcanistGauge = get_memory_class({
    'aetherflowStacks':('byte', 4),
})

class SummonerGauge(get_memory_class({
    'stanceMilliseconds':('ushort',0),
    'bahamutStance':('byte',2),
    'bahamutSummoned':('byte',3),
    'stacks':('byte',3),
})):pass