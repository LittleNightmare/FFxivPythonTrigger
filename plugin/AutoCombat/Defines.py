from plugin.FFxivMemory.models.MemoryParseObject import get_memory_lazy_class, get_memory_lazy_array, get_memory_class

PlayerGCDTime_offset = 0x1CB96E8
PlayerTargetModel_offset = 0x1D05160
SkillQueueMark1_offset = 0x1cb9138
IsInFight_offset = 0x1D5553A
CoolDownGroup_offset = 0x1CB9258

CoolDownGroup = get_memory_class({
    'currentCooldown': ('float', 8),
    'maxCooldown': ('float', 12),
})

CoolDownGroups = get_memory_lazy_array(CoolDownGroup, 0x14, 100)

AutoCombatData = get_memory_lazy_class({
    'playerGcdTime': ('float', PlayerGCDTime_offset),
    'playerGcdTotal': ('float', PlayerGCDTime_offset + 4),
    'playerTargetPtr': ('ulonglong', PlayerTargetModel_offset),
    'skillQueueMark1': ('ulong', SkillQueueMark1_offset),
    'skillQueueMark2': ('ulong', SkillQueueMark1_offset + 4),
    'skillQueueAbilityId': ('ulong', SkillQueueMark1_offset + 8),
    'skillQueueTargetId': ('ulong', SkillQueueMark1_offset + 16),
    'isInFight': ('byte', IsInFight_offset),
    'coolDownGroups': (CoolDownGroups, CoolDownGroup_offset),
}, 0.01)
