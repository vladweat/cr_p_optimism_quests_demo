import config

from loguru import logger
from decimal import Decimal
from web3 import Web3, HTTPProvider


class OptimismClient:
    def __init__(self, run: str, network: str) -> None:
        if (
            run
            == "Special for https://t.me/importweb3, creator - https://t.me/vladweat"
        ):
            # logger.info(f"{run}") USE FOR PROD
            pass
        else:
            logger.error(f"Fatal error in script. FO!")
            raise SystemExit(1)

        # self._web3 = Web3(HTTPProvider(config.OPTIMISM_RPC))
        # self._web3 = Web3(HTTPProvider(config.ARBITRUM_RPC))
        self._web3 = self._set_web3_rpc(network)
        self._wallets_dict = self.__create_wallets_dict()
        self._len_wallets_dict = self.__get_len_wallets_dict()

    def _set_web3_rpc(self, network: str) -> Web3:
        """RPC setter

        Args:
            network (str): string with name of network

        Raises:
            SystemExit: if wrong network string input

        Returns:
            Web3: Web3 class
        """
        from web3.middleware import geth_poa_middleware

        if network == "arbitrum":
            return Web3(HTTPProvider(config.ARBITRUM_RPC))
        elif network == "optimism":
            web3 = Web3(HTTPProvider(config.OPTIMISM_RPC))
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            return web3
        else:
            logger.error(f"Wrong network RPC. Change it!")
            raise SystemExit(1)

    def _change_network_rpc(self, network: str) -> None:
        """Change network rpc by string

        Args:
            network (str): string with name of network
        """
        self._web3 = self._set_web3_rpc(network)

    def _check_connection(self) -> bool:
        """Check connection to RPC URL

        Returns:
            bool: connection status
        """
        try:
            return self._web3.isConnected()
        except Exception as e:
            logger.error(e)

    def _get_private_keys(self) -> list:
        """Return list of private keys from wallets.txt

        Returns:
            list: keys
        """
        try:
            with open("private_keys.txt", "r") as file:
                keys = file.read().splitlines()

            return keys

        except Exception as e:
            logger.error(e)

    def _check_private_keys(self):
        """Checking private keys for validity

        Raises:
            SystemExit: if 'Non-hexadecimal digit found' raised
        """
        if None in self._wallets_dict.values():
            logger.error(f"Fatal error in script. Change keys above!")
            raise SystemExit(1)
        else:
            logger.success(f"Private key verification passed!")

    def _get_address(self, private_key: str = None) -> str:
        """Return address from _wallets_dict[private_key]

        Args:
            private_key (str, optional): private key. Defaults to None.

        Returns:
            str: address from _wallets_dict[private_key]
        """
        try:
            address = self._wallets_dict.get(private_key)
            return address
        except Exception as e:
            logger.error(e)

    def _get_balance(self, private_key: str = None) -> float:
        """Get balance of address generated from _get_address(private_key)

        Args:
            private_key (str, optional): private key. Defaults to None.

        Returns:
            float: address balance
        """
        try:
            address = self._get_address(private_key)
            # balance = self._convert_from_ether_format(
            #     self._web3.eth.get_balance(address)
            # )
            balance = self._web3.eth.get_balance(address)
            return balance
        except Exception as e:
            logger.error(e)

    def _get_nonce(self, private_key: str):
        """Return nonce of address from private_key

        Args:
            private_key (str): private key

        Returns:
            int: nonce
        """
        try:
            address = self.__get_address(private_key)
            nonce = self._web3.eth.get_transaction_count(address)
            return nonce
        except Exception as e:
            logger.error(e)

    def _convert_from_ether_format(self, num: int = None) -> float:
        """Convert Wei to Ether format
        100000000000000000000 -> 100

        Args:
            num (integer): wei format integer

        Returns:
            float: _description_
        """
        try:
            ether_format = self._web3.fromWei(num, "ether")
            return ether_format
        except Exception as e:
            logger.error(e)

    def _convert_to_ether_format(self, num: float = None) -> int:
        """Convert Ether to Wei format
        100 -> 100000000000000000000
        Args:
            num (float): ether format integer

        Returns:
            int: _description_
        """
        try:
            wei_format = self._web3.toWei(Decimal(num), "ether")
            return wei_format
        except Exception as e:
            logger.error(e)

    def _convert_from_mwei_format(self, num: int = None) -> float:
        """Convert Wei to Mwei format
        1000000 -> 1
        Args:
            num (integer): wei format integer

        Returns:
            float: _description_
        """
        try:
            ether_format = self._web3.fromWei(num, "mwei")
            return ether_format
        except Exception as e:
            logger.error(e)

    def _convert_to_mwei_format(self, num: float = None) -> int:
        """Convert Mwei to Wei format
        1 -> 1000000
        Args:
            num (float): ether format integer

        Returns:
            int: _description_
        """
        try:
            wei_format = self._web3.toWei(Decimal(num), "mwei")
            return wei_format
        except Exception as e:
            logger.error(e)

    def _get_checksum_address(self, address: str) -> str:
        """Return toChecksumAddress(address)

        Args:
            address (str): address

        Returns:
            str: toChecksumAddress(address)
        """
        try:
            checksum_address = self._web3.toChecksumAddress(address)
            return checksum_address
        except Exception as e:
            logger.error(e)

    def _sign_transaction(self, transaction, private_key: str):
        """Wrapper for web.eth.account.sign_transaction

        Args:
            transaction (_type_): transaction.method().buildTransaction()
            private_key (str): private key

        Returns:
            signed_tx: web3.eth.account.sign_transaction()
        """
        try:
            signed_tx = self._web3.eth.account.sign_transaction(
                transaction, private_key
            )
            return signed_tx
        except Exception as e:
            logger.error(e)

    def _send_raw_transaction(self, sign_txn):
        """Wrapper for web3.eth.send_raw_transaction

        Args:
            sign_txn (_type_): sign_txn

        Returns:
            raw_tx_hash: raw_tx_hash
        """
        try:
            raw_tx_hash = self._web3.eth.send_raw_transaction(sign_txn.rawTransaction)
            return raw_tx_hash
        except Exception as e:
            logger.error(e)

    def _get_tx_hash(self, raw_tx_hash):
        """Wrapper for web3.toHex

        Args:
            raw_tx_hash (_type_): raw_tx_hash

        Returns:
            tx_hash: tx_hash
        """  
        try:
            tx_hash = self._web3.toHex(raw_tx_hash)
            return tx_hash
        except Exception as e:
            logger.error(e)

    def __create_wallets_dict(self) -> dict:
        """Created dict with key:address args

        Returns:
            dict: dict{ private_key: 'address' }
        """
        try:
            private_keys = self._get_private_keys()
            wallets_dict = {}

            for key in private_keys:
                wallets_dict[key] = self.__get_address(key)

            return wallets_dict
        except Exception as e:
            logger.error(e)

    def __get_len_wallets_dict(self) -> int:
        """Return length of self._wallets_dict

        Returns:
            int: len of self._wallets_dict
        """
        return len(self._wallets_dict)

    def __get_address(self, private_key: str = None) -> str:
        """Return address generated from private_key

        Args:
            private_key (str, optional): private key. Defaults to None.

        Returns:
            str: address generated with web3.eth.account.from_key
        """
        if type(private_key) == str:
            try:
                account = self._web3.eth.account.from_key(private_key)
                return account.address

            except Exception as e:
                logger.error(f'{e}: Change key "{private_key}"')
        else:
            logger.error(
                f"Сan't get address from private key. Private key format is {type(private_key)}, must be <class 'str'>!"
            )
