from . import DarkKnight, RedMage, Warrior


class AutoCombo(
    DarkKnight.DarkKnight,
    RedMage.RedMage,
    Warrior.Warrior,
):
    name = "Auto Combo"
    combos = {
        21: Warrior.Warrior.warrior_logic,
        35: RedMage.RedMage.red_mage_logic,
        32: DarkKnight.DarkKnight.dark_knight_logic,
    }
