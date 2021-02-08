import logging
import pymem
from .ValToBytes import long_to_bytes

pymem.logger.setLevel(logging.ERROR)


class MemoryHandler(pymem.Pymem):
    def __init__(self, name: str = None, pid: int = None):
        if name and pid:
            raise Exception("Should not call by both name and pid")

        if name is not None:
            super().__init__(name)
        elif pid is not None:
            super().__init__()
            self.open_process_from_id(pid)
        else:
            super().__init__('ffxiv_dx11.exe')

        self.main_module = pymem.process.module_from_name(self.process_handle, "ffxiv_dx11.exe")

    def pattern_scan_main_module(self, pattern: bytes):
        """
        scan memory after a byte pattern for the main module and return its corresponding memory address

        :param bytes pattern: A regex byte pattern to search for
        :return: int Memory address of given pattern, or None if one was not found
        """
        return pymem.pattern.pattern_scan_module(self.process_handle, self.main_module, pattern)

    def scan_pointer_by_pattern(self, pattern: bytes, cmd_len: int, ptr_idx: int = None):
        """
        scan memory after a byte pattern for the main module and get the upper pointer

        :param bytes pattern: A regex byte pattern to search for
        :param int cmd_len: the length from start of pattern to the end of target address
        :return:  int Memory address of given pattern
        """
        ptr_idx = ptr_idx or cmd_len - 4
        temp = self.pattern_scan_main_module(pattern)
        if temp is None: return None
        return self.read_ulong(temp + ptr_idx) + temp + cmd_len

    def read_pointer_shift(self, base, *shifts):
        ptr = base
        for shift in shifts:
            ptr = self.read_ulonglong(ptr) + shift
        return ptr

    def scan_vTable(self, signature: int):
        next_page = 0
        ans = None
        while ans is None:
            next_page, ans = pymem.pattern.scan_pattern_page(self.process_handle, next_page, long_to_bytes(signature, True))
        return ans
