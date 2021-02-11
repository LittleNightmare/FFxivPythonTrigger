from .ChatLogMemory import ChatLogMemory
from FFxivPythonTrigger import EventBase
from datetime import datetime


class ChatLogEvent(EventBase):
    id = "log_event"
    name = "log event"

    def __init__(self, time, channel_id, player, message):
        self.time = datetime.fromtimestamp(time)
        self.channel_id = channel_id
        self.player = player if player else None
        self.message = message

    def __str__(self):
        return "{}\t{}\t{}\t{}".format(self.time, self.channel_id, self.player or 'n/a', self.message)


class ChatLogProcess(object):
    def __init__(self, memoryHandler):
        self.chatLogMemory = ChatLogMemory(memoryHandler)
        self.update_sign = self.chatLogMemory.get_update_sign()
        self.msg_count = self.chatLogMemory.count()

    def check_update(self):
        ans = []
        new_sign = self.chatLogMemory.get_update_sign()
        if self.update_sign != new_sign:
            self.update_sign = new_sign
            self.msg_count = 0
        new_count = self.chatLogMemory.count()
        while self.msg_count < new_count:
            ans.append(ChatLogEvent(*self.chatLogMemory[self.msg_count]))
            self.msg_count += 1
        return ans
