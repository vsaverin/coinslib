from typing import NamedTuple


class BitcoinAccount(NamedTuple):
    public_key: str
    private_key: str
    address: str
