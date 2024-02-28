import typing

from .transaction_emulator import TransactionEmulator
from .blockchain_api import BlockchainApi

from pytoniq_core import Cell, Builder, MessageAny, ShardAccount, Address, HashMap, Transaction


# most of the logic here is taken from https://github.com/tonkeeper/tongo/blob/master/txemulator/trace.go


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
        libs.append(cell.begin_parse().preload_bytes(32))
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
    ):
        self.api = api
        self.transaction_emulator = transaction_emulator
        self.current_states: typing.Dict[Address, ShardAccount] = {}  # address -> (ShardAccount)
        self.libs = {}

    def update_set_libs(self):
        def value_serializer(dest: Builder, src: Cell):
            if src is not None:
                dest.store_uint(0, 2).store_ref(src).store_maybe_ref(None)
        hm = HashMap(256, value_serializer=value_serializer)
        hm.map = self.libs
        self.transaction_emulator.set_libs(hm.serialize())

    async def emulate(self, message: MessageAny):
        if message.is_external:
            address = message.info.dest
        elif message.is_internal:
            address = message.info.dest
        else:
            raise Exception('message should be either internal or external')

        sh = self.current_states.get(address)
        if sh is None:
            _, sh = await self.api.raw_get_account_state(address)
            self.current_states[address] = sh

        libs = []
        find_libs(sh.cell, libs)
        find_libs(message.init.serialize(), libs) if message.init is not None else None
        to_update = []
        for lib in libs:
            if lib in self.libs:
                continue
            to_update.append(lib)
        if to_update:
            self.libs |= self.api.get_libraries(to_update)  # todo: there can be more than 16 libs, need to check this
            self.update_set_libs()

        # todo: self.transaction_emulator.set_prev_blocks_info(await self.api.get_prev_blocks_info())

        res = self.transaction_emulator.emulate_transaction(sh.cell, message.serialize())
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
