from .MemoryParseObject import get_memory_lazy_class
from .JobGauges import *
from ..MemoryHandler import MemoryHandler

_Player = get_memory_lazy_class({
    'localContentId': ('ulong', 88),
    'job': ('byte', 106),
    'str': ('uint', 356),
    'dex': ('uint', 360),
    'vit': ('uint', 364),
    'int': ('uint', 368),
    'mnd': ('uint', 372),
    'pie': ('uint', 376),
    'tenacity': ('uint', 428),
    'attack': ('uint', 432),
    'directHit': ('uint', 440),
    'crit': ('uint', 460),
    'attackMagicPotency': ('uint', 484),
    'healMagicPotency': ('uint', 488),
    'det': ('uint', 528),
    'skillSpeed': ('uint', 532),
    'spellSpeed': ('uint', 536),
    'craft': ('uint', 632),
    'control': ('uint', 636),
})


class Player(_Player):
    gauge_addr = None

    def get_gauge(self):
        if self.gauge_addr is None:
            return None
        elif self.job == 35:
            return RedMageGauge(self.handler, self.gauge_addr)
        elif self.job == 21:
            return WarriorGauge(self.handler, self.gauge_addr)
        else:
            return None
