from abc import ABC, abstractmethod
import typing

from pytoniq_core import ShardAccount, Address, Cell, BlockIdExt


class BlockchainApi(ABC):

    last_mc_block: BlockIdExt

    @abstractmethod
    async def raw_get_account_state(self, address: typing.Union[str, Address], block: BlockIdExt = None, *args, **kwargs) -> typing.Union[typing.Any, ShardAccount]:
        ...

    @abstractmethod
    async def get_libraries(self, library_list: typing.List[typing.Union[bytes, str]]) -> typing.Dict[str, typing.Optional[Cell]]:
        ...
