from FFxivPythonTrigger import FFxivPythonTrigger
from plugin.FFxivMemory import FFxivMemory
from plugin.GayMagician import GayMagicianPlugin
from plugin.CutsceneSkipper import CutsceneSkipper
from plugin.SuperJump import SuperJump
from plugin.Command import Command
from plugin.Zoom import ZoomPlugin
from plugin.Teleporter import Teleporter
from plugin.NamazuServer import NamazuServer
from plugin.AutoCombo import AutoCombo
from plugin.AutoCombat import AutoCombat
import logging


def show(evt):
    # if evt.channel_id == 2091:
    print(evt)


fpt = FFxivPythonTrigger([
    FFxivMemory,
    GayMagicianPlugin,
    NamazuServer,
    Command,
    CutsceneSkipper,
    SuperJump,
    ZoomPlugin,
    Teleporter,
    AutoCombo,
    AutoCombat
])
# fpt.logger.print_level=logging.DEBUG
# fpt.register_event("log_event", show)
fpt.start()
