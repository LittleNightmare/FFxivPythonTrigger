from core.FFxivPythonTrigger import PluginBase
from plugin.FFxivMemory.models.MemoryParseObject import get_memory_lazy_class
from asyncio import sleep

prev_combo_pattern = b"\xF3\x0F......\xF3\x0F...\xE8....\x48\x8B.\x48\x8B.\x0F\xB7"
ComboState = get_memory_lazy_class({
    'duration': ('float', 0),
    'actionId': ('uint', 4),
}, 0)
keys = {
    'rdm': {
        'single': (1, 1),
        'multi': (1, 2),
        'combo': (1, 3),
    },
    'war': {
        'single': (1, 1),
        'multi': (1, 2),
    }
}


class AutoCombo(PluginBase):
    name = "auto combo"

    def get_me(self):
        return self.FPT.api.FFxivMemory.actorTable[0]

    def plugin_onload(self):
        combo_addr = self.FPT.api.MemoryHandler.scan_pointer_by_pattern(prev_combo_pattern, 8)
        self.comboState = ComboState(self.FPT.api.MemoryHandler, combo_addr)
        self.FPT.register_api('ComboState', self.comboState)
        self.work = False
        self.keyTemp = {i: {j: None for j in range(12)} for i in range(10)}

    def plugin_onunload(self):
        self.work = False

    def change_skill(self, row, block, name, *cases):
        lv = self.get_me().level
        for case in cases:
            if case[0] > lv:
                name = case[1]
            else:
                break
        if self.keyTemp and self.keyTemp[row][block] != name:
            self.keyTemp[row][block] = name
            self.FPT.api.Magic.macro_command("/hotbar set %s %s %s" % (name, row, block))

    async def plugin_start(self):
        self.work = True
        playerInfo = self.FPT.api.FFxivMemory.playerInfo
        while self.work:
            if playerInfo.job in self.combos:
                getattr(self, self.combos[playerInfo.job])()
            await sleep(0.1)

    def RedMageLogic(self):
        meActor = self.get_me()
        effects = {effect.buffId: effect for effect in meActor.effects if effect.buffId != 0}
        speedSpell = 1249 in effects or 167 in effects
        gauge = self.FPT.api.FFxivMemory.playerInfo.get_gauge()
        white = gauge.white_mana <= gauge.black_mana
        if speedSpell:
            self.change_skill(*keys['rdm']['multi'], '散碎')
            if white:
                self.change_skill(*keys['rdm']['single'], '赤疾风', (10, '赤闪雷'), (4, '摇荡'))
            else:
                self.change_skill(*keys['rdm']['single'], '赤闪雷', (4, '摇荡'))
        else:
            if 1234 in effects:
                self.change_skill(*keys['rdm']['single'], '赤火炎')
            elif 1235 in effects:
                self.change_skill(*keys['rdm']['single'], '赤飞石')
            else:
                self.change_skill(*keys['rdm']['single'], '摇荡')
            if white:
                self.change_skill(*keys['rdm']['multi'], '赤烈风', (22, '赤震雷'), (18, '散碎'))
            else:
                self.change_skill(*keys['rdm']['multi'], '赤震雷', (18, '散碎'))
        combo_id = self.comboState.actionId
        if combo_id == 7504:
            self.change_skill(*keys['rdm']['combo'], '交击斩', (35, '回刺'))
        elif combo_id == 7512:
            self.change_skill(*keys['rdm']['combo'], '连攻', (50, '回刺'))
        elif combo_id == 7529:
            if white:
                self.change_skill(*keys['rdm']['combo'], '赤疾风', (70, '赤闪雷'), (68, '回刺'))
            else:
                self.change_skill(*keys['rdm']['combo'], '赤闪雷', (68, '回刺'))
        elif combo_id == 7525 or combo_id == 7526:
            self.change_skill(*keys['rdm']['combo'], '摇荡', (80, '回刺'))
        else:
            self.change_skill(*keys['rdm']['combo'], '回刺')

    def WarriorLogic(self):
        meActor = self.get_me()
        effects = {effect.buffId: effect for effect in meActor.effects if effect.buffId != 0}
        combo_id = self.comboState.actionId
        if combo_id == 31:
            self.change_skill(*keys['war']['single'], '凶残裂', (4, '重劈'))
        elif combo_id == 37:
            if 90 in effects and effects[90].timer > 5:
                self.change_skill(*keys['war']['single'], '暴风斩', (26, '重劈'))
            else:
                self.change_skill(*keys['war']['single'], '暴风碎', (50, '暴风斩'), (26, '重劈'))
        else:
            self.change_skill(*keys['war']['single'], '重劈')
        if combo_id==41:
            self.change_skill(*keys['war']['multi'], '秘银暴风', (40, '超压斧'))
        else:
            self.change_skill(*keys['war']['multi'], '超压斧')

    combos = {
        35: 'RedMageLogic',
        21: 'WarriorLogic',
    }
