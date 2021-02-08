from core.FFxivPythonTrigger import PluginBase

offset=0x1cb9024
default=10.4

class SuperJump(PluginBase):
    name = "Super Jump"
    def plugin_onload(self):
        self.addr=self.FPT.api.MemoryHandler.process_base.lpBaseOfDll+offset
        self.trigger_id =self.FPT.register_event("log_event", self.process_command)

    def process_command(self, evt):
        if evt.channel_id == 56 and evt.message.startswith('sjump '):
            self.FPT.api.Magic.echo_msg(self._process_command(evt.message.split(' ')[1]))

    def _process_command(self, arg):
        try:
            if arg=="default":
                arg=default
            self.FPT.api.MemoryHandler.write_float(self.addr,float(arg))
        except Exception as e:
            return str(e)
        return "set to %s"%arg
