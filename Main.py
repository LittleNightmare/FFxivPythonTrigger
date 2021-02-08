from core.FFxivPythonTrigger import FFxivPythonTrigger
from plugin.FFxivMemory.FFxivMemory import FFxivMemory
from plugin.GayMagician.GayMagicianPlugin import GayMagicianPlugin
from plugin.CutsceneSkipper import CutsceneSkipper
from plugin.SuperJump import SuperJump
from plugin.Command import Command
from plugin.Zoom import ZoomPlugin

fpt = FFxivPythonTrigger([
    FFxivMemory,
    GayMagicianPlugin,
    Command,
    CutsceneSkipper,
    SuperJump,
    ZoomPlugin,
]).start()
