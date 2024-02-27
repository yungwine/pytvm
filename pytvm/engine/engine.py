from abc import abstractmethod, ABC


class EmulatorEngine(ABC):

    @abstractmethod
    def transaction_emulator_create(self, config_boc: bytes, verbosity_level: int):
        ...

    @abstractmethod
    def transaction_emulator_set_unixtime(self, emulator, unixtime: int) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_lt(self, emulator, lt: int) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_rand_seed(self, emulator, rand_seed_hex: bytes) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_ignore_chksig(self, emulator, ignore_chksig: bool) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_config(self, emulator, config_boc: bytes) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_libs(self, emulator, libraries_boc: bytes) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_debug_enabled(self, emulator, debug_enabled: bool) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_set_prev_blocks_info(self, emulator, prev_blocks_info_boc: bytes) -> bool:
        ...

    @abstractmethod
    def transaction_emulator_emulate_transaction(self, emulator, shard_account_boc: bytes, message_boc: bytes) -> dict:
        ...

    @abstractmethod
    def transaction_emulator_emulate_tick_tock_transaction(self, emulator, shard_account_boc: bytes, is_tock: bool) -> dict:
        ...

    @abstractmethod
    def transaction_emulator_destroy(self, emulator):
        ...

    def emulator_set_verbosity_level(self, verbosity_level: int) -> bool:
        ...

    @abstractmethod
    def tvm_emulator_create(self, code_boc: bytes, data_boc: bytes, verbosity_level: int):
        ...

    @abstractmethod
    def tvm_emulator_set_libraries(self, emulator, libraries_boc: bytes) -> bool:
        ...

    @abstractmethod
    def tvm_emulator_set_c7(self, emulator, address: bytes, unixtime: int, balance: int, rand_seed_hex: bytes, config_boc: bytes) -> bool:
        ...

    @abstractmethod
    def tvm_emulator_set_prev_blocks_info(self, emulator, prev_blocks_info_boc: bytes) -> bool:
        ...

    @abstractmethod
    def tvm_emulator_set_gas_limit(self, emulator, gas_limit: int) -> bool:
        ...

    @abstractmethod
    def tvm_emulator_set_debug_enabled(self, emulator, debug_enabled: bool) -> bool:
        ...

    @abstractmethod
    def tvm_emulator_run_get_method(self, emulator, method_id: int, stack_boc: bytes) -> dict:
        ...

    @abstractmethod
    def tvm_emulator_send_external_message(self, emulator, message_boc: bytes) -> dict:
        ...

    @abstractmethod
    def tvm_emulator_send_internal_message(self, emulator, message_boc: bytes, amount: int) -> dict:
        ...

    @abstractmethod
    def tvm_emulator_destroy(self, emulator):
        ...
