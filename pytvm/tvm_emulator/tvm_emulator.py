import typing

from ..engine import EmulatorEngine
from ..utils import cell_to_b64, get_method_id, b64_to_cell

from pytoniq_core import Cell, Slice


class TvmEmulator:

    def __init__(
            self,
            code: Cell,
            data: Cell,
            verbosity_level: int = 0,
            engine: EmulatorEngine = None
    ):
        """
        :param engine: TVM Engine
        :param code: contact code
        :param data: contract data (c4 register)
        :param verbosity_level:  Verbosity level of VM log. 0 - log truncated to last 256 characters. 1 - unlimited length log. 2 - for each command prints its cell hash and offset. 3 - for each command log prints all stack values.
        """
        if engine is None:
            from ..engine import EmulatorEngineC
            engine = EmulatorEngineC.default()
        self.engine = engine

        self.emulator = self.engine.tvm_emulator_create(cell_to_b64(code), cell_to_b64(data), verbosity_level)

    def set_libraries(self, libraries: Cell):
        return self.engine.tvm_emulator_set_libraries(self.emulator, cell_to_b64(libraries))

    def set_c7(self, address: str, unixtime: int, balance: int, rand_seed_hex: str, config: Cell):
        return self.engine.tvm_emulator_set_c7(self.emulator, address.encode(), unixtime, balance, rand_seed_hex.encode(), cell_to_b64(config))

    def set_prev_blocks_info(self, prev_blocks_info: Cell):
        return self.engine.tvm_emulator_set_prev_blocks_info(self.emulator, cell_to_b64(prev_blocks_info))

    def set_gas_limit(self, gas_limit: int):
        return self.engine.tvm_emulator_set_gas_limit(self.emulator, gas_limit)

    def set_debug_enabled(self, debug_enabled: bool):
        return self.engine.tvm_emulator_set_debug_enabled(self.emulator, debug_enabled)

    def raw_run_get_method(self, method_id: int, stack: Cell):
        return self.engine.tvm_emulator_run_get_method(self.emulator, method_id, cell_to_b64(stack))

    def run_get_method(self, method: typing.Union[int, str], stack: list):
        from pytoniq_core.tlb import VmStack
        if isinstance(method, str):
            method = get_method_id(method)
        stack = VmStack.serialize(stack)
        res = self.raw_run_get_method(method, stack)
        res['stack'] = VmStack.deserialize(Slice.one_from_boc(res['stack']))
        if 'gas_used' in res:
            res['gas_used'] = int(res['gas_used'])
        return res

    def raw_send_external_message(self, message: Cell):
        return self.engine.tvm_emulator_send_external_message(self.emulator, cell_to_b64(message))

    def send_external_message(self, body: Cell):
        from pytoniq_core.tlb.transaction import OutList
        res = self.raw_send_external_message(body)
        res['new_code'] = b64_to_cell(res['new_code'])
        res['new_data'] = b64_to_cell(res['new_data'])
        res['actions'] = OutList.deserialize(Slice.one_from_boc(res['actions'])) if res['actions'] else []
        if 'gas_used' in res:
            res['gas_used'] = int(res['gas_used'])
        return res

    def raw_send_internal_message(self, message: Cell, amount: int):
        return self.engine.tvm_emulator_send_internal_message(self.emulator, cell_to_b64(message), amount)

    def send_internal_message(self, message: Cell, amount: int):
        from pytoniq_core.tlb.transaction import OutList
        res = self.engine.tvm_emulator_send_internal_message(self.emulator, cell_to_b64(message), amount)
        res['new_code'] = b64_to_cell(res['new_code'])
        res['new_data'] = b64_to_cell(res['new_data'])
        res['actions'] = OutList.deserialize(Slice.one_from_boc(res['actions']))
        if 'gas_used' in res:
            res['gas_used'] = int(res['gas_used'])
        return res

    def __del__(self):
        self.engine.tvm_emulator_destroy(self.emulator)
