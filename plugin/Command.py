from core.FFxivPythonTrigger import PluginBase


class Command(PluginBase):
    name="command controller"
    def deal_chat_log(self, event):
        if event.channel_id == 56 and event.message.startswith('fpt '):
            args = event.message.split(' ')[1:]
            if args[0] == 'close':
                self.FPT._fpt.close()

    def plugin_onload(self):
        self.FPT.register_event("log_event", self.deal_chat_log)
