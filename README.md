# Blockchain Services Documentation

Welcome to the documentation for our Blockchain Services Python module. This module provides a simplified interface for interacting with Bitcoin-like and Ethereum-like blockchains. Below, you'll find an overview of the main classes and their functionalities.

## Table of Contents

1. [BitcoinLikeChainsService Class](./docs/abstract_coins.md)

2. [EtherLikeService Class](./docs/abstract_coins.md)

Please refer to the `/docs` folder for detailed documentation on how to use the provided services.


Each documentation file provides detailed explanations of the classes, methods, and parameters available for interacting with the respective blockchain services.

## Getting Started

To get started, navigate to the `/docs` folder and explore the documentation for the blockchain services provided in this repository.

## Issues and Contributions

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or pull request on GitHub.

## BitcoinLikeChainsService Class

### Methods

- `create_wallet(tag: str) -> str`
- `satoshi_to_btc(amwount: int) -> float`
- `balance() -> float`
- `get_balance(wallet: str) -> float`
- `transfer_to_main(main_address: str, transit_tag: str, amount: float) -> dict`
- `send(wallet: str, amount: float) -> str`
- `get_sum_and_address(tag: str, transaction_id: str) -> dict`
- `load_wallet(wallet: str) -> dict`
- `unload_wallet(wallet: str) -> dict`
- `get_confs(txid: str) -> int`
- `get_unspent_wallet_data(tag: str, repository) -> dict`

## EtherLikeService Class

### Methods

- `get_base_wallet_balance(self)`
- `send_from_base_wallet(self, wallet, amount)`
- `get_balance_from_node(self, wallet) -> int`
- `get_transactions_list(self, blockhash) -> list[str]`
- `get_data_by_txid(self, txid: str) -> dict`
- `send_from_tag(self, to_address: str, from_tag: str, amount: float) -> dict`
- `create_wallet(self, tag: str)`
- `get_address_from_name(self, tag: str)`
- `get_tag_transaction(self, tag: str, transaction_id: str)`
