from FFxivPythonTrigger import PluginBase
from plugin.FFxivMemory.models.MemoryParseObject import get_memory_lazy_class
from asyncio import sleep
import traceback
import logging

prev_combo_pattern = b"\xF3\x0F......\xF3\x0F...\xE8....\x48\x8B.\x48\x8B.\x0F\xB7"
ComboState = get_memory_lazy_class({
    'duration': ('float', 0),
    'actionId': ('uint', 4),
}, 0.01)


class AutoComboBase(PluginBase):
    log_combo_action_id = False

    def get_me(self):
        return self.FPT.api.FFxivMemory.actorTable[0]

    def plugin_onload(self):
        combo_addr = self.FPT.api.MemoryHandler.scan_pointer_by_pattern(prev_combo_pattern, 8)
        self.comboState = ComboState(self.FPT.api.MemoryHandler, combo_addr)
        self.FPT.register_api('ComboState', self.comboState)
        self.work = False
        self.keyTemp = {i: {j: None for j in range(12)} for i in range(10)}
        self.prev_combo_action_id = None

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
        player_info = self.FPT.api.FFxivMemory.playerInfo
        while self.work:
            if self.log_combo_action_id and self.comboState.actionId != self.prev_combo_action_id:
                self.prev_combo_action_id = self.comboState.actionId
                self.FPT.log('new combo action %s' % self.prev_combo_action_id, logging.DEBUG)
            if player_info.job in self.combos:
                try:
                    self.combos[player_info.job](self)
                except:
                    traceback.print_exc()
            await sleep(0.1)

    combos = dict()
