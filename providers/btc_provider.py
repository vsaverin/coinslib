import os
from .abstract_provider import BitcoinLikeProvider


IS_DEV = os.environ.get("IS_DEV")


class BitcoinRPCProvider(BitcoinLikeProvider):
    async def send_from_base_wallet(self, wallet, amount):
        wallet_tag = "dev_main" if IS_DEV else "main"
        response = await self._send_request(
            "sendtoaddress",
            [
                str(wallet),
                amount,
                "withdraw_sended",
                "withdraw_received",
                False,
                True,
                None,
                "unset",
                None,
                50,
            ],
            wallet_tag=wallet_tag,
        )
        if not response.get("result"):
            raise ValueError(response.get("error"))
        return response.get("result")

    async def send_from_tag(
        self, to_address: str, from_tag: str, amount: float
    ) -> dict:
        await self.load_wallet_by_tag(from_tag)
        response = await self._send_request(
            "sendtoaddress",
            [
                str(to_address),
                amount,
                "transit_from",
                "transit_to",
                True,
                True,
                None,
                "unset",
                None,
                51,
            ],
            wallet_tag=from_tag,
        )
        await self.unload_wallet_by_tag(from_tag)
        if not response.get("result"):
            raise ValueError(response.get("error"))
        return response.get("result")
