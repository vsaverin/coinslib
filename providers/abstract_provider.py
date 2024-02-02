import os
from abc import ABC, abstractmethod
import aiohttp
from asyncio import sleep


IS_DEV = os.environ.get("IS_DEV")


class AbstractRPCProvider(ABC):
    def __init__(
        self, rpcuser: str, rpcpassword: str, rpcaddress: str, rpcversion: str = "1.0"
    ):
        self.rpcaddress = rpcaddress
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.rpcversion = rpcversion

    async def _send_request(
        self, method: str, params: str = None, wallet_tag: str = ""
    ):
        if wallet_tag:
            address = self.rpcaddress + f"/wallet/{wallet_tag}"
        else:
            address = self.rpcaddress
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=address,
                json={
                    "id": "1",
                    "jsonrpc": self.rpcversion,
                    "method": method,
                    "params": params,
                },
                auth=aiohttp.BasicAuth(login=self.rpcuser, password=self.rpcpassword),
            ) as resp:
                return await resp.json()

    @abstractmethod
    async def get_base_wallet_balance(self):
        ...

    @abstractmethod
    async def send_from_base_wallet(self, wallet, amount):
        ...

    @abstractmethod
    async def get_balance_from_node(self, wallet):
        ...

    @abstractmethod
    async def get_transactions_list(self, blockhash) -> list[str]:
        ...

    @abstractmethod
    async def get_data_by_txid(self, txid: str) -> dict:
        ...

    @abstractmethod
    async def send_from_tag(self, to_address: str, from_tag: str, amwount: float):
        ...

    @abstractmethod
    async def create_wallet(self, tag: str):
        ...

    @abstractmethod
    async def get_address_from_name(self, tag: str):
        ...

    @abstractmethod
    async def get_tag_transaction(self, tag: str, transaction_id: str):
        ...


class BitcoinLikeProvider(AbstractRPCProvider):
    async def get_base_wallet_balance(self):
        if IS_DEV:
            wallet = "dev_main"
        else:
            wallet = "main"
        response = await self._send_request("getbalance", ["*"], wallet_tag=wallet)
        return response.get("result")

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

    async def get_balance_from_node(self, wallet) -> int:
        response = await self._send_request("getbalance", [wallet])
        return int(response["result"])

    async def get_transactions_list(self, blockhash) -> list[str]:
        response = await self._send_request("getblock", [blockhash])
        return response["tx"]

    async def get_data_by_txid(self, txid: str) -> dict:
        response = await self._send_request("getrawtransaction", [txid])
        return response

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

    async def create_wallet(self, tag: str):
        resp = await self._send_request(
            "createwallet",
            {
                "wallet_name": tag,
            },
        )
        return resp

    async def get_address_from_name(self, tag: str):
        await self._send_request("getnewaddress", [], wallet_tag=tag)
        resp = await self._send_request("getaddressesbylabel", [""], wallet_tag=tag)
        return next(iter(resp.get("result")))

    async def get_tag_transaction(self, tag: str, transaction_id: str):
        attempts = 0
        while attempts < 20:
            await self.load_wallet_by_tag(tag)
            resp = await self._send_request(
                "gettransaction", [transaction_id], wallet_tag=tag
            )
            if resp.get("result"):
                break
            attempts += 1
            await sleep(1)
        await self.unload_wallet_by_tag(tag)
        return resp

    async def load_wallet_by_tag(self, tag: str) -> dict:
        resp = await self._send_request("loadwallet", [tag])
        return resp

    async def unload_wallet_by_tag(self, tag: str) -> dict:
        if "main" in tag:
            return
        resp = await self._send_request("unloadwallet", [tag])
        return resp

    async def get_confs_from_network(self, txid: str) -> dict:
        tag = "dev_main" if IS_DEV else "main"
        resp = await self._send_request("gettransaction", [txid], wallet_tag=tag)
        return resp.get("result")

    async def list_transactions_last(self, tag, repository):
        result = await self._send_request("listtransactions", [], wallet_tag=tag)
        result = result.get("result")
        if not result:
            return
        last_transaction = None
        for transaction in reversed(result):
            if transaction["amount"] < 0:
                continue
            exists = await repository.income_exists(transaction["txid"])
            if exists:
                continue
            last_transaction = transaction
            break
        return last_transaction["txid"]


class EtherLikeProvider(AbstractRPCProvider):
    async def get_base_wallet_balance(self):
        ...

    async def send_from_base_wallet(self, wallet, amount):
        ...

    async def get_balance_from_node(self, wallet) -> int:
        ...

    async def get_transactions_list(self, blockhash) -> list[str]:
        ...

    async def get_data_by_txid(self, txid: str) -> dict:
        ...

    async def send_from_tag(
        self, to_address: str, from_tag: str, amount: float
    ) -> dict:
        ...

    async def create_wallet(self, tag: str):
        ...

    async def get_address_from_name(self, tag: str):
        ...

    async def get_tag_transaction(self, tag: str, transaction_id: str):
        ...
