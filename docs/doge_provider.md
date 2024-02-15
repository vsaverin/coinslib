# DogeRPCProvider

DogeRPCProvider is a Python module that provides an asynchronous interface to interact with the Dogecoin RPC (Remote Procedure Call) API. It extends the `BitcoinLikeProvider` class and implements specific functionalities related to Dogecoin.

## Usage

To use the `DogeRPCProvider` class, you need to instantiate an object and call its methods. Here are some examples of how to use the provided methods:

### Creating a Wallet

```python
provider = DogeRPCProvider()
wallet_address = await provider.create_wallet("my_wallet_tag")
```

This method creates a new wallet with the specified tag and returns the newly generated wallet address.

### Getting Address from Name

```python
tag = "my_wallet_tag"
address = await provider.get_address_from_name(tag)
```

Retrieve the wallet address associated with the specified tag.

### Getting Transaction Information

```python
tag = "my_wallet_tag"
transaction_id = "123456789"
transaction_info = await provider.get_tag_transaction(tag, transaction_id)
```

Get detailed information about a specific transaction associated with a given wallet tag.

### Sending Dogecoins

```python
to_address = "DABC123XYZ"
from_tag = "my_wallet_tag"
amount = 100.0
result = await provider.send_from_tag(to_address, from_tag, amount)
```

Send Dogecoins from a specific wallet tag to a specified destination address.

### Getting Wallet Balance

```python
balance = await provider.get_base_wallet_balance()
```

Retrieve the balance of the main wallet associated with the environment (development or production).

### Handling Transactions

The `_get_transaction_category` method categorizes transactions into different types, such as send, receive, transit, send_and_receive, etc.

## Configuration

The DogeRPCProvider class supports the following environment variables:

- `IS_DEV`: If set, the provider uses the development wallet (`dev_main` tag) instead of the production wallet (`main` tag).

## Dependencies

- Python 3.7+
- [BitcoinLikeProvider](./abstract_provider.py): The abstract provider class that DogeRPCProvider extends.

## Note

Ensure that you have the Dogecoin daemon running and properly configured, and the RPC server is accessible for this module to function correctly.

**Disclaimer:** This module is intended for educational purposes and may require proper configuration and security measures before use in a production environment. Use it at your own risk.

Feel free to contribute, report issues, or suggest improvements!