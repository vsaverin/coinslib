# Bitcoin and Ethereum-like Chains Service

This Python module provides a convenient interface for interacting with Bitcoin-like and Ethereum-like blockchains. The module includes two classes: `BitcoinLikeChainsService` for Bitcoin-like chains and `EtherLikeService` for Ethereum-like chains.

## BitcoinLikeChainsService Class

### Initialization
```python
class BitcoinLikeChainsService:
    def __init__(
        self,
        rpcuser: str,
        rpcpassword: str,
        rpcaddress: str,
    ):
        self.provider = BitcoinRPCProvider(rpcuser, rpcpassword, rpcaddress)
```

#### Methods

1. **create_wallet(tag: str) -> str:**
   - Creates a wallet on the node.
   - Parameters:
     - `tag`: A string to identify the wallet.
   - Returns the wallet address.

2. **satoshi_to_btc(amwount: int) -> float:**
   - Converts the given amount in satoshis to BTC.
   - Parameters:
     - `amwount`: Amount in satoshis.
   - Returns the amount in BTC.

3. **balance() -> float:**
   - Retrieves the balance of the base wallet.
   - Returns the balance in BTC.

4. **get_balance(wallet: str) -> float:**
   - Retrieves the balance of a specific wallet.
   - Parameters:
     - `wallet`: Wallet address.
   - Returns the balance in BTC.

5. **transfer_to_main(main_address: str, transit_tag: str, amount: float) -> dict:**
   - Transfers a specified amount from a transit wallet to the main wallet.
   - Parameters:
     - `main_address`: Main wallet address.
     - `transit_tag`: Transit wallet tag.
     - `amount`: Amount to transfer in BTC.
   - Returns the transaction details.

6. **send(wallet: str, amount: float) -> str:**
   - Sends a specified amount from the base wallet to the given wallet address.
   - Parameters:
     - `wallet`: Receiver's wallet address.
     - `amount`: Amount to send in BTC.
   - Returns the transaction ID.

7. **get_sum_and_address(tag: str, transaction_id: str) -> dict:**
   - Retrieves transaction details such as sum, address, confirmations, and type.
   - Parameters:
     - `tag`: Wallet tag.
     - `transaction_id`: Transaction ID.
   - Returns a dictionary with transaction details.

8. **load_wallet(wallet: str) -> dict:**
   - Loads a wallet on the node.
   - Parameters:
     - `wallet`: Wallet address.
   - Returns the response from the node.

9. **unload_wallet(wallet: str) -> dict:**
   - Unloads a wallet from the node.
   - Parameters:
     - `wallet`: Wallet address.
   - Returns the response from the node.

10. **get_confs(txid: str) -> int:**
    - Retrieves the confirmations for a specific transaction.
    - Parameters:
      - `txid`: Transaction ID.
    - Returns the number of confirmations.

11. **get_unspent_wallet_data(tag: str, repository) -> dict:**
    - Retrieves unspent wallet data.
    - Parameters:
      - `tag`: Wallet tag.
      - `repository`: Repository information.
    - Returns a dictionary with transaction ID and tag.

## EtherLikeService Class

### Initialization
```python
class EtherLikeService:
    def __init__(self, rpcuser: str, rpcpassword: str, rpcaddress: str):
        self.provider = EtherProvider(
            rpcaddress=rpcaddress, rpcpassword=rpcpassword, rpcuser=rpcuser
        )
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpcaddress))
```

#### Methods

1. **create_wallet(tag: str) -> LocalAccount:**
   - Creates a new Ethereum wallet.
   - Parameters:
     - `tag`: A string to identify the wallet.
   - Returns a LocalAccount object containing the wallet information.

2. **balance(account: str) -> float:**
   - Retrieves the balance of a specific Ethereum account.
   - Parameters:
     - `account`: Ethereum account address.
   - Returns the balance in Ether.

3. **send(address: str, amount: float | str, sender_public: str, sender_private: str) -> str:**
   - Sends Ether from one account to another.
   - Parameters:
     - `address`: Receiver's Ethereum address.
     - `amount`: Amount to send in Ether.
     - `sender_public`: Sender's public key.
     - `sender_private`: Sender's private key.
   - Returns the transaction ID.

4. **transfer_to_main(main_address, wallet, amount):**
   - Transfers Ether from a wallet to the main address.
   - Parameters:
     - `main_address`: Main Ethereum address.
     - `wallet`: Wallet information (dictionary or LocalAccount object).
     - `amount`: Amount to transfer in Ether.

5. **get_confs(txid: str) -> int:**
   - Retrieves the confirmations for a specific Ethereum transaction.
   - Parameters:
     - `txid`: Transaction ID.
   - Returns the number of confirmations. If the transaction is not found, returns -1.

**Note:** Proper error handling should be implemented when using these classes to handle potential exceptions.