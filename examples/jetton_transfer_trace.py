import asyncio

from pytvm.transaction_emulator import TraceEmulator, TraceResult, TransactionEmulator
from pytoniq import Address, Cell, Transaction, LiteBalancer, Contract, begin_cell

WALLET = Address("kQCBc6PP9EndBCsJdgU2PCkMTxriH74NQcDOaDUKRG555TEp")
JETTON_WALLET = Address("kQAVmLElV4C6J1KKt5fqGn4e8NR-DFiL9Dhy29WCJh57wC90")
DESTINATION = Address("kQCSES0TZYqcVkgoguhIb8iMEo4cvaEwmIrU5qbQgnN8ftBF")

def create_jetton_transfer_payload(
        destination: Address | str,
        amount: int,
        query_id: int = 0,
        response_address: Address | str | None = None,
        custom_payload: Cell | None = None,
        forward_amount: int = 0,
        forward_payload: Cell | None = None
    ) -> Cell:
        return (
            begin_cell()
            .store_uint(0xf8a7ea5, 32)
            .store_uint(query_id, 64)
            .store_coins(amount)
            .store_address(destination)
            .store_address(response_address)
            .store_maybe_ref(custom_payload)
            .store_coins(forward_amount)
            .store_maybe_ref(forward_payload)
            .end_cell()
        )

def trace_result_simple_format(tr: TraceResult) -> str:
    def address_format(address: Address) -> str:
        return address.to_str(is_test_only=True)

    def transaction_format(tx: Transaction) -> str:
        msg = tx.in_msg
        if msg is None:
            return ""
        if msg.is_external:
            return f"External: {address_format(msg.info.dest)}" 
        if msg.is_internal:
            return f"Internal: {address_format(msg.info.src)} -> {address_format(msg.info.dest)}" 
        if msg.is_external_out:
            return f"External out: {msg.info.src}"
        return ""

    def trace_format(tr: TraceResult, depth: int = 0) -> str:
        tx = tr["transaction"]
        s = ""
        if tx is not None:
            s = "."*depth + transaction_format(tx)
        for child in tr["children"]:
            s += '\n'
            s += trace_format(child, depth + 1)
        return s

    return trace_format(tr)

async def main():
    async with LiteBalancer.from_testnet_config(2) as provider:
        body = create_jetton_transfer_payload(DESTINATION, 1*10**9, forward_amount=1, response_address=WALLET)
        message = Contract.create_internal_msg(value=1*10**9, body=body, src=WALLET, dest=JETTON_WALLET)
        emulator = TraceEmulator(provider, TransactionEmulator())
        result = await emulator.emulate(message)
        print(trace_result_simple_format(result))

asyncio.run(main())
