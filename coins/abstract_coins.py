from eth_account.signers.local import LocalAccount

from web3 import AsyncWeb3

from ..providers.btc_provider import BitcoinRPCProvider
from .custom_exceptions import OnNodeWalletCreationError, GetTransactionError
from ..providers.eth_provider import EtherProvider


class BitcoinLikeChainsService:
    def __init__(
        self,
        rpcuser: str,
        rpcpassword: str,
        rpcaddress: str,
    ):
        self.provider = BitcoinRPCProvider(rpcuser, rpcpassword, rpcaddress)

    async def create_wallet(self, tag: str) -> str:
        resp = await self.provider.create_wallet(tag)
        if not resp.get("result"):
            raise OnNodeWalletCreationError(
                f'On-node wallet creation error ({resp.get("error")})'
            )
        address = await self.provider.get_address_from_name(tag)
        await self.provider.unload_wallet_by_tag(tag)
        return address

    @classmethod
    async def satoshi_to_btc(self, amwount: int):
        return int(amwount) / 100000000

    async def balance(self):
        return await self.provider.get_base_wallet_balance()

    async def get_balance(self, wallet):
        return await self.provider.get_balance_from_node(wallet)

    async def transfer_to_main(
        self, main_address: str, transit_tag: str, amount: float
    ) -> dict:
        resp = await self.provider.send_from_tag(main_address, transit_tag, amount)
        return resp

    async def send(self, wallet: str, amount: float) -> str:
        return await self.provider.send_from_base_wallet(wallet, amount)

    async def get_sum_and_address(self, tag: str, transaction_id: str) -> dict:
        data = await self.provider.get_tag_transaction(tag, transaction_id)
        data = data.get("result")
        if not data:
            return {"error": "Transaction not found"}
        summ = data.get("amount")
        confs = data.get("confirmations")
        try:
            details = data.get("details")[0]
            address = details.get("address")
            type = details.get("category")
        except KeyError:
            return {"error": "Address not found"}
        return {"sum": summ, "address": address, "confirmations": confs, "type": type}

    async def load_wallet(self, wallet: str) -> dict:
        resp = await self.provider.load_wallet_by_tag(wallet)
        return resp

    async def unload_wallet(self, wallet: str) -> dict:
        resp = await self.provider.unload_wallet_by_tag(wallet)
        return resp

    async def get_confs(self, txid: str) -> int:
        resp = await self.provider.get_confs_from_network(txid)
        confs = resp.get("confirmations")
        if not confs:
            raise GetTransactionError(resp.get("error"))
        return confs

    async def get_unspent_wallet_data(self, tag: str, repository):
        await self.load_wallet(tag)
        txid = await self.provider.list_transactions_last(tag, repository)
        await self.unload_wallet(tag)
        return {"txid": txid, "tag": tag}


class EtherLikeService:
    def __init__(self, rpcuser: str, rpcpassword: str, rpcaddress: str):
        self.provider = EtherProvider(
            rpcaddress=rpcaddress, rpcpassword=rpcpassword, rpcuser=rpcuser
        )
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpcaddress))

    def create_wallet(self, tag: str) -> LocalAccount:
        return self.w3.eth.account.create()

    async def balance(self, account: str) -> float:
        balance = await self.w3.eth.get_balance(account)
        return self.w3.from_wei(balance, "ether")

    async def send(
        self, address: str, amount: float | str, sender_public: str, sender_private: str
    ) -> str:
        if type(address) is str:
            address = address
        else:
            address = address.address
        nonce = await self.w3.eth.get_transaction_count(sender_public)
        gas_price = await self.w3.eth.gas_price
        gas = await self.w3.eth.estimate_gas(
            {
                "to": address,
                "from": sender_public,
                "value": self.w3.to_wei(amount, "ether"),
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            dict(
                nonce=nonce + 1,
                maxFeePerGas=gas_price,
                maxPriorityFeePerGas=3000000000,
                gas=gas,
                to=address,
                value=self.w3.to_wei(amount, "ether"),
                data=b"",
                type=2,
                chainId=1,
            ),
            sender_private,
        )
        result = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txid = "0x" + result.hex()
        return txid

    async def transfer_to_main(self, main_address, wallet, amount):
        try:
            await self.send(
                main_address, amount, wallet["address"], wallet["private_key"]
            )
        except TypeError:
            await self.send(main_address, amount, wallet.address, wallet.private_key)

    async def get_confs(self, txid: str):
        try:
            transaction = await self.w3.eth.get_transaction(txid)
        except Exception:
            return -1

        if transaction is None:
            return -1

        try:
            latest_block_number = await self.w3.eth.block_number
        except Exception:
            return -1

        confirmation_count = latest_block_number - transaction["blockNumber"]

        return confirmation_count
