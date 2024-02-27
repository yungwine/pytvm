import os.path

from .engine import EmulatorEngine

import ctypes
import json


class EmulatorEngineC(EmulatorEngine):

    def __init__(self, path: str) -> None:
        lib = ctypes.CDLL(path)

        # define signatures

        lib.transaction_emulator_create.restype = ctypes.c_void_p
        lib.transaction_emulator_create.argtypes = [ctypes.c_char_p, ctypes.c_int]

        lib.transaction_emulator_set_unixtime.restype = ctypes.c_bool
        lib.transaction_emulator_set_unixtime.argtypes = [ctypes.c_void_p, ctypes.c_uint]

        lib.transaction_emulator_set_lt.restype = ctypes.c_bool
        lib.transaction_emulator_set_lt.argtypes = [ctypes.c_void_p, ctypes.c_uint]

        lib.transaction_emulator_set_rand_seed.restype = ctypes.c_bool
        lib.transaction_emulator_set_rand_seed.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.transaction_emulator_set_ignore_chksig.restype = ctypes.c_bool
        lib.transaction_emulator_set_ignore_chksig.argtypes = [ctypes.c_void_p, ctypes.c_bool]

        lib.transaction_emulator_set_config.restype = ctypes.c_bool
        lib.transaction_emulator_set_config.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.transaction_emulator_set_libs.restype = ctypes.c_bool
        lib.transaction_emulator_set_libs.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.transaction_emulator_set_debug_enabled.restype = ctypes.c_bool
        lib.transaction_emulator_set_debug_enabled.argtypes = [ctypes.c_void_p, ctypes.c_bool]

        lib.transaction_emulator_set_prev_blocks_info.restype = ctypes.c_bool
        lib.transaction_emulator_set_prev_blocks_info.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.transaction_emulator_emulate_transaction.restype = ctypes.c_char_p
        lib.transaction_emulator_emulate_transaction.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

        lib.transaction_emulator_emulate_tick_tock_transaction.restype = ctypes.c_char_p
        lib.transaction_emulator_emulate_tick_tock_transaction.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]

        lib.transaction_emulator_destroy.restype = None
        lib.transaction_emulator_destroy.argtypes = [ctypes.c_void_p]

        lib.emulator_set_verbosity_level.restype = ctypes.c_bool
        lib.emulator_set_verbosity_level.argtypes = [ctypes.c_int]

        lib.tvm_emulator_create.restype = ctypes.c_void_p
        lib.tvm_emulator_create.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]

        lib.tvm_emulator_set_libraries.restype = ctypes.c_bool
        lib.tvm_emulator_set_libraries.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.tvm_emulator_set_c7.restype = ctypes.c_bool
        lib.tvm_emulator_set_c7.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_char_p]

        lib.tvm_emulator_set_prev_blocks_info.restype = ctypes.c_bool
        lib.tvm_emulator_set_prev_blocks_info.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.tvm_emulator_set_gas_limit.restype = ctypes.c_bool
        lib.tvm_emulator_set_gas_limit.argtypes = [ctypes.c_void_p, ctypes.c_int]

        lib.tvm_emulator_set_debug_enabled.restype = ctypes.c_bool
        lib.tvm_emulator_set_debug_enabled.argtypes = [ctypes.c_void_p, ctypes.c_bool]

        lib.tvm_emulator_run_get_method.restype = ctypes.c_char_p
        lib.tvm_emulator_run_get_method.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]

        lib.tvm_emulator_send_external_message.restype = ctypes.c_char_p
        lib.tvm_emulator_send_external_message.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

        lib.tvm_emulator_send_internal_message.restype = ctypes.c_char_p
        lib.tvm_emulator_send_internal_message.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]

        lib.tvm_emulator_destroy.restype = None
        lib.tvm_emulator_destroy.argtypes = [ctypes.c_void_p]

        self.lib = lib

    def transaction_emulator_create(self, config_boc: bytes, verbosity_level: int):
        return self.lib.transaction_emulator_create(config_boc, verbosity_level)

    def transaction_emulator_set_unixtime(self, emulator, unixtime: int) -> bool:
        return self.lib.transaction_emulator_set_unixtime(emulator, unixtime)

    def transaction_emulator_set_lt(self, emulator, lt: int) -> bool:
        return self.lib.transaction_emulator_set_lt(emulator, lt)

    def transaction_emulator_set_rand_seed(self, emulator, rand_seed_hex: bytes) -> bool:
        return self.lib.transaction_emulator_set_rand_seed(emulator, rand_seed_hex)

    def transaction_emulator_set_ignore_chksig(self, emulator, ignore_chksig: bool) -> bool:
        return self.lib.transaction_emulator_set_ignore_chksig(emulator, ignore_chksig)

    def transaction_emulator_set_config(self, emulator, config_boc: bytes) -> bool:
        return self.lib.transaction_emulator_set_config(emulator, config_boc)

    def transaction_emulator_set_libs(self, emulator, libraries_boc: bytes) -> bool:
        return self.lib.transaction_emulator_set_libs(emulator, libraries_boc)

    def transaction_emulator_set_debug_enabled(self, emulator, debug_enabled: bool) -> bool:
        return self.lib.transaction_emulator_set_debug_enabled(emulator, debug_enabled)

    def transaction_emulator_set_prev_blocks_info(self, emulator, prev_blocks_info_boc: bytes) -> bool:
        return self.lib.transaction_emulator_set_prev_blocks_info(emulator, prev_blocks_info_boc)

    def transaction_emulator_emulate_transaction(self, emulator, shard_account_boc: bytes, message_boc: bytes) -> dict:
        return json.loads(self.lib.transaction_emulator_emulate_transaction(emulator, shard_account_boc, message_boc))

    def transaction_emulator_emulate_tick_tock_transaction(self, emulator, shard_account_boc: bytes, is_tock: bool) -> dict:
        return json.loads(self.lib.transaction_emulator_emulate_tick_tock_transaction(emulator, shard_account_boc, is_tock))

    def transaction_emulator_destroy(self, emulator):
        self.lib.transaction_emulator_destroy(emulator)

    def emulator_set_verbosity_level(self, verbosity_level: int) -> bool:
        return self.lib.emulator_set_verbosity_level(verbosity_level)

    def tvm_emulator_create(self, code_boc: bytes, data_boc: bytes, verbosity_level: int):
        return self.lib.tvm_emulator_create(code_boc, data_boc, verbosity_level)

    def tvm_emulator_set_libraries(self, emulator, libraries_boc: bytes) -> bool:
        return self.lib.tvm_emulator_set_libraries(emulator, libraries_boc)

    def tvm_emulator_set_c7(self, emulator, address: bytes, unixtime: int, balance: int, rand_seed_hex: bytes, config_boc: bytes) -> bool:
        return self.lib.tvm_emulator_set_c7(emulator, address, unixtime, balance, rand_seed_hex, config_boc)

    def tvm_emulator_set_prev_blocks_info(self, emulator, prev_blocks_info_boc: bytes) -> bool:
        return self.lib.tvm_emulator_set_prev_blocks_info(emulator, prev_blocks_info_boc)

    def tvm_emulator_set_gas_limit(self, emulator, gas_limit: int) -> bool:
        return self.lib.tvm_emulator_set_gas_limit(emulator, gas_limit)

    def tvm_emulator_set_debug_enabled(self, emulator, debug_enabled: bool) -> bool:
        return self.lib.tvm_emulator_set_debug_enabled(emulator, debug_enabled)

    def tvm_emulator_run_get_method(self, emulator, method_id: int, stack_boc: bytes) -> dict:
        return json.loads(self.lib.tvm_emulator_run_get_method(emulator, method_id, stack_boc))

    def tvm_emulator_send_external_message(self, emulator, message_boc: bytes) -> dict:
        return json.loads(self.lib.tvm_emulator_send_external_message(emulator, message_boc))

    def tvm_emulator_send_internal_message(self, emulator, message_boc: bytes, amount: int) -> dict:
        return json.loads(self.lib.tvm_emulator_send_internal_message(emulator, message_boc, amount))

    def tvm_emulator_destroy(self, emulator):
        self.lib.tvm_emulator_destroy(emulator)

    @classmethod
    def default(cls, verbosity_level: int = 0):
        import pkg_resources
        files = pkg_resources.resource_listdir('pytvm', f'engine/')
        for f in files:
            if f.startswith('libemulator'):
                res = cls(os.path.join(pkg_resources.resource_filename('pytvm', f'engine/'), f))
                res.emulator_set_verbosity_level(verbosity_level)
                return res
        raise ImportError('No emulator binaries found: install from source')
