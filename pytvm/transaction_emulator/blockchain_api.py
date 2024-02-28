from abc import ABC, abstractmethod
import typing

from pytoniq_core import ShardAccount, Address, Cell


class BlockchainApi(ABC):

    @abstractmethod
    def raw_get_account_state(self, address: typing.Union[str, Address], *args, **kwargs) -> typing.Union[typing.Any, ShardAccount]:
        ...

    @abstractmethod
    def get_libraries(self, library_list: typing.List[typing.Union[bytes, str]]) -> typing.Dict[str, typing.Optional[Cell]]:
        ...
