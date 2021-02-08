from core.FFxivPythonTrigger import FFxivPythonTrigger
from plugin.FFxivMemory.FFxivMemory import FFxivMemory
from plugin.GayMagician.GayMagicianPlugin import GayMagicianPlugin
from plugin.CutsceneSkipper import CutsceneSkipper
from plugin.SuperJump import SuperJump
from plugin.Command import Command

fpt=FFxivPythonTrigger([
    FFxivMemory,
    GayMagicianPlugin,
    CutsceneSkipper,
    SuperJump,
    Command,
]).start()
