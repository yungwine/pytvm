import typing

from ..engine import EmulatorEngine
from ..utils import cell_to_b64, DEFAULT_CONFIG_BOC

from pytoniq_core import Cell, Slice


class TransactionEmulator:

    def __init__(
            self,
            config: typing.Union[Cell, str] = None,
            verbosity_level: int = 0,
            engine: EmulatorEngine = None
    ):
        """
        :param engine: TVM Engine
        :param config: blockchain config boc or Cell, if None - default config will be used
        :param verbosity_level:  Verbosity level of VM log. 0 - log truncated to last 256 characters. 1 - unlimited length log. 2 - for each command prints its cell hash and offset. 3 - for each command log prints all stack values.
        """
        if engine is None:
            from ..engine import EmulatorEngineC
            engine = EmulatorEngineC.default()
        self.engine = engine

        if isinstance(config, Cell):
            config = cell_to_b64(config)
        if config is None:
            config = DEFAULT_CONFIG_BOC.encode()

        self.emulator = self.engine.transaction_emulator_create(config, verbosity_level)

    def set_unixtime(self, unixtime: int):
        return self.engine.transaction_emulator_set_unixtime(self.emulator, unixtime)

    def set_lt(self, lt: int):
        return self.engine.transaction_emulator_set_lt(self.emulator, lt)

    def set_rand_seed(self, rand_seed_hex: str):
        return self.engine.transaction_emulator_set_rand_seed(self.emulator, rand_seed_hex.encode())

    def set_ignore_chksig(self, ignore_chksig: bool):
        return self.engine.transaction_emulator_set_ignore_chksig(self.emulator, ignore_chksig)

    def set_config(self, config: Cell):
        return self.engine.transaction_emulator_set_config(self.emulator, cell_to_b64(config))

    def set_libs(self, libs: Cell):
        return self.engine.transaction_emulator_set_libs(self.emulator, cell_to_b64(libs))

    def set_prev_blocks_info(self, prev_blocks_info: Cell):
        return self.engine.transaction_emulator_set_prev_blocks_info(self.emulator, cell_to_b64(prev_blocks_info))

    def set_debug_enabled(self, debug_enabled: bool):
        return self.engine.transaction_emulator_set_debug_enabled(self.emulator, debug_enabled)

    def raw_emulate_transaction(self, shard_account: Cell, message: Cell):
        return self.engine.transaction_emulator_emulate_transaction(self.emulator, cell_to_b64(shard_account), cell_to_b64(message))

    @staticmethod
    def _process_tr_emulation_result(result: dict):
        from pytoniq_core.tlb.transaction import Transaction, OutList
        from pytoniq_core.tlb.account import ShardAccount
        if result['success']:
            result['actions'] = OutList.deserialize(Slice.one_from_boc(result['actions'])) if result['actions'] else []
            result['shard_account'] = ShardAccount.deserialize(Slice.one_from_boc(result['shard_account']))
            result['transaction'] = Transaction.deserialize(Slice.one_from_boc(result['transaction']))
        return result

    def emulate_transaction(self, shard_account: Cell, message: Cell):
        res = self.raw_emulate_transaction(shard_account, message)
        return self._process_tr_emulation_result(res)

    def raw_emulate_tick_tock_transaction(self, shard_account: Cell, is_tock: bool):
        return self.engine.transaction_emulator_emulate_tick_tock_transaction(self.emulator, cell_to_b64(shard_account), is_tock)

    def emulate_tick_tock_transaction(self, shard_account: Cell, is_tock: bool):
        res = self.raw_emulate_tick_tock_transaction(shard_account, is_tock)
        return self._process_tr_emulation_result(res)

    def __del__(self):
        self.engine.transaction_emulator_destroy(self.emulator)
