from .MemoryHandler import MemoryHandler
from .ChatLogProcess import ChatLogProcess
from core.FFxivPythonTrigger import PluginBase
import asyncio


class FFxivMemory(PluginBase):
    name = "FFxiv Memory Plugin"

    def plugin_onload(self):
        self.handler = MemoryHandler()
        self.chatLogProcess = ChatLogProcess(self.handler)
        self.work = False
        #self.FPT.register_event("log_event", print)
        self.FPT.register_api('MemoryHandler', self.handler)

    def plugin_onunload(self):
        self.work = False

    async def plugin_start(self):
        self.work = True
        while self.work:
            events = list()
            events += self.chatLogProcess.check_update()
            for event in events:
                self.FPT.process_event(event)
            await asyncio.sleep(0.1)
