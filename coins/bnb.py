import web3

from .abstract_coins import EtherLikeService
from .bep20abi import abi_list


class BinanceCoin(EtherLikeService):
    async def _send_via_contract(
        self,
        account,
        smart_contract_address,
        recipient_address,
        amount_in_wei,
        gas_limit,
        gas_price,
        nonce,
    ):
        contract = self.w3.eth.contract(address=smart_contract_address, abi=abi_list)

        transaction = await contract.functions.transfer(
            recipient_address, amount_in_wei
        ).build_transaction(
            {
                "gas": gas_limit,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": 56,
            }
        )

        signed_txn = account.sign_transaction(transaction)
        txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash.hex()

    async def send(
        self,
        address: str,
        amount: float | str,
        sender_public: str,
        private_key: str,
        smart_contract_address: str | None = None,
    ) -> str:
        if type(address) is str:
            address = address
        else:
            address = address.address
        account = self.w3.eth.account.from_key(private_key)
        recipient_address = web3.Web3.to_checksum_address(address)
        amount_in_wei = self.w3.to_wei(amount, "ether")
        gas_price = await self.w3.eth.gas_price
        nonce = await self.w3.eth.get_transaction_count(account.address)
        gas_limit = 21000
        smart_contract_address = web3.Web3.to_checksum_address(smart_contract_address)
        if smart_contract_address:
            return await self._send_via_contract(
                account,
                smart_contract_address,
                recipient_address,
                amount_in_wei,
                gas_limit,
                gas_price,
                nonce,
            )
        transaction = {
            "to": recipient_address,
            "value": amount_in_wei,
            "gas": gas_limit,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": 56,
        }
        signed_txn = account.sign_transaction(transaction)
        txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash.hex()
