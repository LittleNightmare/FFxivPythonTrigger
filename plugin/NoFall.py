from FFxivPythonTrigger import PluginBase
import logging

pattern = b"\x74.\xE8....\x48\x8B\x8B\xC8\x03\x00\x00\xF3\x0F\x10\x50\x04\xEB.\xF3\x0F\x10\x54\x24\x44\xF3\x0F" \
          b"\x10\x5C\x24\x48\xF3\x0F\x10\x4C\x24\x40\xE8....\x80\x7C\x24\x70."

command = '@nofall'


class NoFall(PluginBase):
    name = "No Fall"

    def plugin_onload(self):
        mh = self.FPT.api.MemoryHandler
        self.addr = mh.pattern_scan_main_module(pattern)
        if self.addr is None:
            offset = self.FPT.storage.data.setdefault("offset", None)
            raw = self.FPT.storage.data.setdefault("raw", None)
            if offset is None or raw is None:
                self.FPT.log("offset or raw is not found in data/searhing", logging.ERROR)
                return
            self.addr = mh.get_address_by_offset(offset)
            self.raw = bytes([int(raw[i * 2 + i * 2 + 2], 16) for i in range(len(raw) // 2)])
        else:
            self.FPT.storage.data["offset"] = self.addr - mh.process_base.lpBaseOfDll
            self.raw = mh.read_bytes(self.addr, len(pattern))
            self.FPT.storage.data["raw"] = self.raw.hex()
            self.FPT.storage.store()
