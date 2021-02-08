from os import path
from core.FFxivPythonTrigger import PluginBase
import clr
from.Magics import Magics

clr.AddReference(path.join(path.dirname(path.realpath(__file__)),'res', 'GayMagician'))
from GayMagician import GayMagician


class GayMagicianPlugin(PluginBase):
    name = "Gay Magician"

    def plugin_onload(self):
        self.gm = GayMagician()
        self.gm.LoadGameProcess(self.FPT.api.MemoryHandler.process_id)
        self.magic= Magics(self.gm)
        self.FPT.register_api('Magic', self.magic)
        self.magic.echo_msg('GayMagician loaded')

    def plugin_onunload(self):
        self.gm.Detach()
