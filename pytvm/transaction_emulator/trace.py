import typing

from .transaction_emulator import TransactionEmulator
from .blockchain_api import BlockchainApi

from pytoniq_core import Cell, Builder, MessageAny, ShardAccount, Address, HashMap, Transaction, begin_cell, BlockIdExt

# most of the logic here is taken from https://github.com/tonkeeper/tongo/blob/master/txemulator/trace.go


EMPTY_STATE = (begin_cell()
               .store_ref(
                    begin_cell()
                    .store_bit_int(0)
                    .end_cell())
               .store_uint(0, 256)
               .store_uint(0, 64)
               .end_cell()
)


class EmulationErrorDescription(typing.TypedDict):
    message: str
    exit_code: int


class TraceResult(typing.TypedDict):
    transaction: typing.Optional[Transaction]
    vm_log: str
    error: typing.Optional[EmulationErrorDescription]
    children: typing.List['TraceResult']


def find_libs(cell: Cell, libs: list):
    if cell.type_ == 2:
        cs = cell.begin_parse()
        cs.skip_bits(8)
        libs.append(cs.preload_bytes(32))
        return True
    res = False
    for ref in cell.refs:  # trick to avoid copying, don't repeat this at home
        if find_libs(ref, libs):
            res = True
    return res


class TraceEmulator:

    def __init__(
            self,
            api: BlockchainApi,
            transaction_emulator: TransactionEmulator,
            limit: int = 100,
            block: BlockIdExt = None
    ):
        """
        :param api: blockchain api like pytoniq's LiteBalancer or LiteClient
        :param transaction_emulator: Transaction Emulator instance, can be reused
        :param limit: trace recursion limit
        :param block: block take states for accounts from. If None, last masterchain block will be used
        """
        self.api = api
        self.transaction_emulator = transaction_emulator
        self.current_states: typing.Dict[Address, ShardAccount] = {}  # address -> (ShardAccount)
        self.libs = {}
        self.counter = 0
        self.limit = limit
        self.block = block or api.last_mc_block

    def update_set_libs(self):
        def value_serializer(src: Cell, dest: Builder):
            if src is not None:
                dest.store_uint(0, 2).store_ref(src).store_maybe_ref(None)
        hm = HashMap(256, value_serializer=value_serializer)
        hm.map = {int(k, 16): v for k, v in self.libs.items() if v is not None}
        self.transaction_emulator.set_libs(hm.serialize()) if hm.serialize() is not None else None

    async def emulate(self, message: MessageAny) -> TraceResult:
        """
        Emulates message in the blockchain. Will raise exception if recursion limit is exceeded

        :param message: message to emulate. Must be internal or external in
        :return:
        """
        if self.counter >= self.limit:
            raise Exception('Trace emulation recursion limit exceeded')

        if message.is_external:
            address = message.info.dest
        elif message.is_internal:
            address = message.info.dest
        else:
            raise Exception('message should be either internal or external')

        sh = self.current_states.get(address)
        if sh is None:
            _, sh = await self.api.raw_get_account_state(address, self.block)
            self.current_states[address] = sh

        libs = []
        if sh is not None:
            find_libs(sh.cell, libs)
        find_libs(message.init.serialize(), libs) if message.init is not None else None
        to_update = []
        for lib in libs:
            if lib in self.libs:
                continue
            to_update.append(lib)
        if to_update:
            self.libs |= await self.api.get_libraries(to_update)
            self.update_set_libs()

        # todo: self.transaction_emulator.set_prev_blocks_info(await self.api.get_prev_blocks_info())
        if sh is not None:
            res = self.transaction_emulator.emulate_transaction(sh.cell, message.serialize())
        else:
            res = self.transaction_emulator.emulate_transaction(EMPTY_STATE, message.serialize())
        self.counter += 1
        result: TraceResult = {
            'transaction': None,
            'vm_log': res.get('vm_log', ''),
            'error': None,
            'children': []
        }
        if res['success']:
            result['transaction'] = res['transaction']
            self.current_states[address] = res['shard_account']
            for out_msg in res['transaction'].out_msgs:
                if out_msg.is_external_out:
                    continue
                res = await self.emulate(out_msg)
                result['children'].append(res)
            return result
        result['error'] = {
            'message': res['error'],
            'exit_code': res.get('vm_exit_code', 0)
        }
        return result
