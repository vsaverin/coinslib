import os

from tronpy.providers import AsyncHTTPProvider
from tronpy import AsyncTron

from .abstract_provider import AbstractRPCProvider


class TronProvider(AbstractRPCProvider):
    async def create_wallet(self, tag: str):
        async with AsyncTron() as client:
            return client.generate_address()

    async def get_base_wallet_balance(self, address: str):
        contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        base = address
        async_provider = AsyncHTTPProvider(api_key=os.environ.get("TRON_API_KEY"))
        async with AsyncTron(provider=async_provider, network="mainnet") as client:
            cntr = await client.get_contract(contract_address)
            precision = await cntr.functions.decimals()
            balance = await cntr.functions.balanceOf(base)
            balance = balance / 10**precision
            return balance

    async def send_from_base_wallet(self, wallet, amount):
        ...

    async def get_balance_from_node(self, wallet):
        ...

    async def get_transactions_list(self, blockhash) -> list[str]:
        ...

    async def get_data_by_txid(self, txid: str) -> dict:
        ...

    async def send_from_tag(self, to_address: str, from_tag: str, amwount: float):
        ...

    async def get_address_from_name(self, tag: str):
        ...

    async def get_tag_transaction(self, tag: str, transaction_id: str):
        ...
