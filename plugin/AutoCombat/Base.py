from FFxivPythonTrigger import PluginBase
from asyncio import sleep
import traceback

command = "@aCombat"

PlayerGCDTime_offset = 0x1CB96E8
PlayerTargetModel_offset = 0x1D05160
SkillQueueMark1_offset = 0x1cb9138
IsInFight_offset = 0x1D5553A
CoolDownGroup_offset = 0x1CB9258


class AutoCombatBase(PluginBase):
    def get_me(self):
        return self.FPT.api.FFxivMemory.actorTable[0]

    def plugin_onload(self):
        self.state = self.FPT.storage.data.setdefault('default_state', dict())
        self.work = False
        self.state.setdefault('use', False)
        self.state.setdefault('single', True)
        self.comboState = self.FPT.api.FFxivMemory.combatData.comboState
        self.FPT.api.command.register(command, self.process_command)
        self.action_sheet = self.FPT.api.Magic.get_excel_sheet('Action')
        self.FPT.api.Magic.echo_msg(self.get_status_string())

    def use_skill_current_target(self, skill_id):
        self.use_skill(skill_id, self.get_target().id)

    def get_skill_colldown_group(self, action_id):
        gp = self.FPT.api.Magic.get_sheet_row(self.action_sheet, action_id).CooldownGroup
        return self.FPT.api.FFxivMemory.combatData.coolDownGroups[gp]

    def use_skill(self, skill_id, target_id):
        skillQueue = self.FPT.api.FFxivMemory.combatData.skillQueue
        skillQueue['abilityId'] = skill_id
        skillQueue['targetId'] = target_id
        skillQueue['mark2'] = 1
        skillQueue['mark1'] = 1

    def get_target(self):
        try:
            return self.FPT.api.FFxivMemory.actorTable[self.get_me().pcTargetId]
        except:
            return None

    def set_target(self, targetId):
        try:
            self.FPT.api.FFxivMemory.combatData['playerTargetPtr'] = self.FPT.api.FFxivMemory.actorTable[targetId]
            return True
        except IndexError:
            return False

    def get_remain_gcd(self):
        return self.FPT.api.FFxivMemory.combatData.gcd.remain

    def is_in_fight(self):
        return bool(self.FPT.api.FFxivMemory.combatData.isInFight)

    def plugin_onunload(self):
        self.work = False
        self.FPT.api.command.unregister(command)

    def get_status_string(self):
        if self.state['use']:
            return "Auto Combat is active in %s mode." % ("Single" if self.state['single'] else "Multi")
        else:
            return "AutoCombat is inactive."

    def process_command(self, args):
        if args[0] == "off":
            self.state['use'] = False
        elif args[0] == "on":
            self.state['use'] = True
            if len(args) > 1:
                if args[1] == "s":
                    self.state['single'] = True
                elif args[1] == "m":
                    self.state['single'] = False
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
                me=self.get_me()
                if self.state['use'] and\
                        target is not None and\
                        self.get_me() is not None and\
                        self.is_in_fight() and \
                        not self.FPT.api.FFxivMemory.combatData.skillQueue.mark1 and \
                        player_info.job in self.combat_strategy and \
                        me.id!=target.id:
                    use_skill = self.combat_strategy[player_info.job](self)
                    if use_skill is not None:
                        self.use_skill(use_skill, target.id)
            except:
                traceback.print_exc()
            await sleep(0.1)

    combat_strategy = dict()
