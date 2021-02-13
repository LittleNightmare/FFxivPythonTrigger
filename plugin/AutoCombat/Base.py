from FFxivPythonTrigger import PluginBase
from .Defines import AutoCombatData
from asyncio import sleep
import traceback

command = "@aCombat"


class AutoCombatBase(PluginBase):
    def get_me(self):
        return self.FPT.api.FFxivMemory.actorTable[0]

    def plugin_onload(self):
        self.work = False
        self.autoCombatData = AutoCombatData(self.FPT.api.MemoryHandler, self.FPT.api.MemoryHandler.process_base.lpBaseOfDll)
        self.use = False
        self.single = True
        self.FPT.api.command.register(command, self.process_command)
        self.action_sheet = self.FPT.api.Magic.get_excel_sheet('Action')

    def use_skill_current_target(self, skill_id):
        self.use_skill(skill_id, self.get_target().id)

    def get_skill_colldown_group(self, action_id):
        gp = self.FPT.api.Magic.get_sheet_row(self.action_sheet, action_id).CooldownGroup
        return self.autoCombatData.coolDownGroups[gp]

    def use_skill(self, skill_id, target_id):
        self.autoCombatData['skillQueueAbilityId'] = skill_id
        self.autoCombatData['skillQueueTargetId'] = target_id
        self.autoCombatData['skillQueueMark2'] = 1
        self.autoCombatData['skillQueueMark1'] = 1

    def get_target(self):
        try:
            return self.FPT.api.FFxivMemory.actorTable[self.get_me().pcTargetId]
        except:
            return None

    def set_target(self, targetId):
        try:
            self.autoCombatData['playerTargetPtr'] = self.FPT.api.FFxivMemory.actorTable[targetId]
            return True
        except IndexError:
            return False

    def get_remain_gcd(self):
        return self.autoCombatData['playerGcdTotal'] - self.autoCombatData['playerGcdTime']

    def is_in_fight(self):
        return bool(self.autoCombatData['isInFight'])

    def plugin_onunload(self):
        self.work = False
        self.FPT.api.command.unregister(command)

    def get_status_string(self):
        if self.use:
            return "Auto Combat is active in %s mode." % ("Single" if self.single else "Multi")
        else:
            return "AutoCombat is inactive."

    def process_command(self, args):
        if args[0] == "off":
            self.use = False
        elif args[0] == "on":
            self.use = True
            if len(args) > 1:
                if args[1] == "s":
                    self.single = True
                elif args[1] == "m":
                    self.single = False
                else:
                    self.FPT.api.Magic.echo_msg("unknown args: %s" % args[1])
        else:
            self.FPT.api.Magic.echo_msg("unknown args: %s" % args[0])
        self.FPT.api.Magic.echo_msg(self.get_status_string())

    async def plugin_start(self):
        self.work = True
        player_info = self.FPT.api.FFxivMemory.playerInfo
        while self.work:
            try:
                target = self.get_target()
                if self.use and target is not None and self.is_in_fight() and player_info.job in self.combat_strategy:
                    use_skill = self.combat_strategy[player_info.job](self)
                    if use_skill is not None:
                        self.use_skill(use_skill, target.id)
            except:
                traceback.print_exc()
            await sleep(0.1)

    combat_strategy = dict()
