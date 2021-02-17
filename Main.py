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
from plugin.WebChat import WebChat
from plugin.NoFall import NoFall
import logging


def show(evt):
    # if evt.channel_id == 2091:
    print(evt)


fpt = FFxivPythonTrigger([
    FFxivMemory,
    GayMagicianPlugin,
    WebChat,
    NamazuServer,
    Command,
    CutsceneSkipper,
    SuperJump,
    ZoomPlugin,
    Teleporter,
    # NoFall,
    AutoCombo,
    AutoCombat,
])
# fpt.logger.print_level=logging.DEBUG
#fpt.register_event("log_event", show)
fpt.start()
