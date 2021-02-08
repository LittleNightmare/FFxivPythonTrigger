class Magics(object):
    def __init__(self, gm):
        self.gm = gm

    def macro_command(self, command: str):
        self.gm.DoTextCommand(command)

    def echo_msg(self, msg):
        self.macro_command('/e ' + str(msg))

    def get_excel_sheet(self, sheet_name):
        return self.gm.GetExcelSheet(sheet_name)

    def get_sheet_row(self, sheet, rowId: int):
        return self.gm.GetSheetRow(sheet, rowId)

    def use_item(self, item_id, is_hq=False, target=0xE0000000):
        self.gm.UseItem(item_id, is_hq, target)
