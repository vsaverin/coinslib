from .abstract_coins import BitcoinLikeChainsService
from ..providers.ltc_provider import LtcRPCProvider


class Litecoin(BitcoinLikeChainsService):
    def __init__(
        self,
        rpcuser: str,
        rpcpassword: str,
        rpcaddress: str,
    ):
        self.provider = LtcRPCProvider(rpcuser, rpcpassword, rpcaddress)
