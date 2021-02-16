import time

from FFxivPythonTrigger.Simulator.Manager import SkillManager, BallManager
from FFxivPythonTrigger.Simulator.Status import Status
from . import StageBase

AllowBuffs = {
    '阔步': '阔步',
    '改革': '改革',
    '俭约': '俭约',
    '长期俭约': '俭约',
    '掌握': '掌握',
    '观察': '观察'
}
AllowSkillSet = {
    '坯料加工',
    '集中加工',
    '俭约加工',
    '比尔格的祝福',
    '注视加工',
}


class Stage3(StageBase):
    def __init__(self, solver):
        super().__init__(solver)
        self.Prequeue = []

    def allowSkills(self, status: Status):
        rCp = status.currentCp
        rDur = status.currentDurability
        ans = list()
        if rCp < 0: return ans
        if rCp >= SkillManager.getCp('精修', status) and status.target.maxDurability - rDur >= 30:
            ans.append(['精修'])
        if status.ball == BallManager.RedBall:
            ans.append(['秘诀'])
        for buff in AllowBuffs:
            if not status.has_buff(buff) and rCp >= SkillManager.getCp(buff, status):
                ans.append([buff])
        for skill in AllowSkillSet:
            if rDur > SkillManager.getDurability(skill, status) and rCp >= SkillManager.getCp(skill, status) and SkillManager[skill].can_use(status):
                ans.append([skill])
        return ans

    def try_solve(self, status: Status, timeLimit=None):
        best = None
        queue = [[status, []]]
        self.solver.cli_logger.hideTag("Math")
        record = set()
        start = time.perf_counter()
        while queue:
            if timeLimit is not None and time.perf_counter() - start > timeLimit:
                self.solver.cli_logger.showTag("Math")
                return best
            tempData = queue.pop(0)
            allow = self.allowSkills(tempData[0])
            for skills in allow:
                tempStats = tempData[0]
                for i, skill in enumerate(skills):
                    tempStats = tempStats.use_skill(SkillManager[skill])
                    if tempStats.ball != BallManager.WhiteBall: tempStats.ball = BallManager.WhiteBall
                if tempStats.get_status_string() not in record:
                    record.add(tempStats.get_status_string())
                    newData = [tempStats, tempData[1] + skills]
                    if tempStats.currentDurability and skills[-1] not in AllowBuffs and (best is None or tempStats.currentQuality > best[0].currentQuality):
                            best = newData
                    if skills[-1]!='比尔格的祝福':
                        queue.append(newData)
        self.solver.cli_logger.showTag("Math")
        return best

    def is_finished(self, status, prev_skill=None):
        if not bool(self.Prequeue) or (status.ball != BallManager.WhiteBall and status.ball != BallManager.YellowBall):
            start = time.perf_counter()
            ans = self.try_solve(status, 5)
            if ans:
                self.Prequeue = ans[1]
                self.log("new plan in {:.2f}s:{}({})".format(time.perf_counter() - start, self.Prequeue, ans[0].currentQuality))
        return not bool(self.Prequeue)

    def deal(self, status, prev_skill=None):
        self.log(self.Prequeue)
        return self.Prequeue.pop(0)

    def reset(self):
        self.Prequeue.clear()
