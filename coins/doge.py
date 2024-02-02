from .abstract_coins import BitcoinLikeChainsService
from ..providers.doge_provider import DogeRPCProvider
from .custom_exceptions import TransferToMainError


class Doge(BitcoinLikeChainsService):
    def __init__(
        self,
        rpcuser: str,
        rpcpassword: str,
        rpcaddress: str,
    ):
        self.provider = DogeRPCProvider(
            rpcuser, rpcpassword, rpcaddress, rpcversion="2.0"
        )

    async def get_sum_and_address(self, tag: str, transaction_id: str):
        data = await self.provider.get_tag_transaction(tag, transaction_id)
        return data

    async def transfer_to_main(
        self, main_address: str, transit_tag: str, amount: float
    ) -> dict:
        resp = await self.provider.send_from_tag_to_main(transit_tag, amount)
        if not resp.get("result"):
            raise TransferToMainError(str(resp))
        return resp
