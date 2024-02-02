import os

from .abstract_provider import BitcoinLikeProvider


class DogeRPCProvider(BitcoinLikeProvider):
    async def create_wallet(self, tag: str):
        result = await self._send_request("getnewaddress", [tag])
        return result

    async def get_address_from_name(self, tag: str) -> str:
        resp = await self._send_request("getaccountaddress", [tag])
        return resp.get("result")

    async def _receive_in_transaction(self, details: list[dict]) -> bool:
        for transaction in details:
            if transaction.get("category") == "receive":
                return transaction
        return None

    async def _send_in_transaction(self, details: list[dict]) -> bool:
        for transaction in details:
            if transaction.get("category") == "send":
                return transaction
        return None

    async def _get_transaction_category(self, details: list[dict]) -> str:
        send = await self._send_in_transaction(details)
        receive = await self._receive_in_transaction(details)
        # Если в транзакциях только отправка, это вывод средств
        if send and not receive:
            return {"type": "send", "amount": send.get("amount")}
        # Если только получение, это ввод с внешнего кошелька
        if receive and not send:
            return {
                "type": "receive",
                "tag": receive.get("account"),
                "receive_amount": receive.get("amount"),
                "address": receive.get("address"),
            }
        # Если есть отправитель main и получатель, это вывод на др. TW
        if send.get("account") == "main" and receive:
            return {
                "type": "send_and_receive",
                "tag": receive.get("account"),
                "send_amount": send.get("amount"),
                "receive_amount": receive.get("amount"),
                "address": receive.get("address"),
            }
        # Если есть отправитель НЕ main, а получатель main, это внутр. транзит
        if send.get("account") != "main" and receive.get("account") == "main":
            return {"type": "transit"}

    async def get_tag_transaction(self, tag: str, transaction_id: str) -> dict:
        resp = await self._send_request("gettransaction", [transaction_id])
        resp = resp.get("result")
        return {
            "transaction": resp,
            "error": resp.get("error"),
            "confirmations": resp.get("confirmations"),
            "info": await self._get_transaction_category(resp.get("details")),
        }

    async def send_from_base_wallet(self, wallet, amount):
        main_tag = "dev_main" if os.environ.get("IS_DEV") else "main"
        resp = await self._send_request("sendfrom", [main_tag, str(wallet), amount])
        if not resp.get("result"):
            raise ValueError(resp.get("error"))
        return resp.get("result")

    async def get_base_wallet_balance(self):
        if os.environ.get("IS_DEV"):
            wallet = "dev_main"
        else:
            wallet = "main"
        response = await self._send_request("getbalance", [wallet])
        return response.get("result")

    async def send_from_tag(
        self, to_address: str, from_tag: str, amount: float
    ) -> dict:
        resp = await self._send_request("sendfrom", [from_tag, to_address, amount])
        if not resp.get("result"):
            raise ValueError(resp.get("error"))
        return resp.get("result")

    async def send_from_tag_to_main(self, from_tag, amount):
        to_main = "dev_main" if os.environ.get("IS_DEV") else "main"
        resp = await self._send_request("move", [from_tag, to_main, amount])
        return resp

    async def get_confs_from_network(self, txid: str) -> dict:
        resp = await self._send_request("gettransaction", [txid])
        return resp.get("result")
