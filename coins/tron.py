from tronpy.keys import PrivateKey
from tronpy import Tron as TronNetwork
from tronpy.providers import HTTPProvider
from hexbytes import HexBytes
import os


from .custom_exceptions import TronTransferError
from ..providers.tron_provider import TronProvider


class Tron:
    def __init__(self, rpcuser: str, rpcpassword: str, rpcaddress: str):
        self.provider = TronProvider(
            rpcaddress=rpcaddress, rpcpassword=rpcpassword, rpcuser=rpcuser
        )
        self._tron = TronNetwork(HTTPProvider(api_key=os.environ.get("TRON_API_KEY")))

    async def create_wallet(self, tag: str) -> dict:
        return await self.provider.create_wallet(tag)

    async def get_balance(self, address: str) -> float:
        return await self.provider.get_base_wallet_balance(address)

    async def send(self, address, amount, wallet) -> str:
        usdt_contract = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        usdt_abi = [
            {
                "outputs": [{"type": "bool"}],
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"},
                ],
                "name": "transfer",
                "stateMutability": "Nonpayable",
                "type": "Function",
            }
        ]
        txid = await self._transfer(
            wallet.get("private_key"),
            str(address),
            int(amount),
            usdt_contract,
            usdt_abi,
        )
        return txid

    async def _transfer(
        self,
        private_key: str,
        to_address: str,
        amount: int,
        contract_address: str,
        abi: str = None,
    ) -> HexBytes:
        pk = PrivateKey(bytes.fromhex(private_key))

        contract = self._tron.get_contract(contract_address)
        contract.abi = abi

        tx = (
            contract.functions.transfer(to_address, amount * 1000000)
            .with_owner(pk.public_key.to_base58check_address())
            .fee_limit(1_000_000_000)
            .build()
            .sign(pk)
        )

        broadcasted_tx = tx.broadcast().wait()
        if broadcasted_tx.get("result"):
            if broadcasted_tx["result"] == "FAILED":
                raise TronTransferError(str(broadcasted_tx["resMessage"]))
        return broadcasted_tx["id"]

    async def get_confs(self, txid: str) -> int:
        transaction = self._tron.get_transaction(txid)
        if transaction["ret"][0]["contractRet"] == "SUCCESS":
            return 6
        elif transaction["ret"][0]["contractRet"] == "PENDING":
            return 0
        elif transaction["ret"][0]["contractRet"] == "FAILED":
            return 0
