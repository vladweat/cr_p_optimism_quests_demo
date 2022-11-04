import time
import random
import config
import datetime
import requests

from loguru import logger
from optimism_core import OptimismClient


class QuestsEngine:
    def __init__(self, core: OptimismClient) -> None:
        self.optimism_core = core
        self._arbiscan_api_key = config.ARBISCAN_API_KEY
        self._optimismscan_api_key = config.OPTIMISM_API_KEY

    def _get_arbitrum_abi(self, contract: str) -> list:
        """Return contract abi from https://arbiscan.io/

        Args:
            contract (str): contract address

        Returns:
            list: abi - json responce['result']
        """
        API_KEY = self._arbiscan_api_key
        try:
            arbiscan_contract_url = f"https://api.arbiscan.io/api?module=contract&action=getabi&address={contract}&apikey={API_KEY}"
            request = requests.get(arbiscan_contract_url)
            data = request.json()

            if data["status"] == "1":
                abi = data["result"]
                return abi
            else:
                logger.error(f'Failed to get abi. Error: {data["result"]}')

        except Exception as e:
            logger.error(e)

    def _get_optimism_abi(self, contract: str) -> list:
        """Return contract abi from https://optimistic.etherscan.io/

        Args:
            contract (str): contract address

        Returns:
            list: abi - json responce['result']
        """
        API_KEY = self._optimismscan_api_key
        try:
            arbiscan_contract_url = f"https://api-optimistic.etherscan.io/api?module=contract&action=getabi&address={contract}&apikey={API_KEY}"
            request = requests.get(arbiscan_contract_url)
            data = request.json()

            if data["status"] == "1":
                abi = data["result"]
                return abi
            else:
                logger.error(f'Failed to get abi. Error: {data["result"]}')

        except Exception as e:
            logger.error(e)

    def _get_arb_function_by_signature(
        self, contract_address: str, signature: str
    ) -> object:
        """Return function from arbitrum contract

        Args:
            contract_address (str): contract address from arbiscan
            signature (str): MethodID from transaction Input Data

        Returns:
            object: function from "get_function_by_selector(signature)"
        """
        try:
            checksum_address = self.optimism_core._web3.toChecksumAddress(
                contract_address
            )
            abi = self._get_arbitrum_abi(contract_address)
            contract = self.optimism_core._web3.eth.contract(
                address=checksum_address, abi=abi
            )
            function = contract.get_function_by_selector(signature)
            return function

        except Exception as e:
            logger.error(f"Wrong address or abi. Error: {e}")

    def _get_opt_function_by_signature(
        self, contract_address: str, signature: str
    ) -> str:
        """Return function from oprimism contract

        Args:
            contract_address (str): contract address from optimistic.etherscan
            signature (str): MethodID from transaction Input Data

        Returns:
            object: function from "get_function_by_selector(signature)"
        """
        try:
            checksum_address = self.optimism_core._web3.toChecksumAddress(
                contract_address
            )
            abi = self._get_optimism_abi(contract_address)
            contract = self.optimism_core._web3.eth.contract(
                address=checksum_address, abi=abi
            )
            function = contract.get_function_by_selector(signature)
            return function

        except Exception as e:
            logger.error(f"Wrong address or abi. Error: {e}")

    def _get_eth_price_arbitrum(self):
        """Return ETH price in USD from arbiscan

        Returns:
            float: ethusd_price
        """
        API_KEY = self._arbiscan_api_key
        try:
            arbiscan_contract_url = f"https://api.arbiscan.io/api?module=stats&action=ethprice&apikey={API_KEY}"
            request = requests.get(arbiscan_contract_url)
            data = request.json()

            if data["status"] == "1":
                response = data["result"]
                ethusd_price = response["ethusd"]
                return ethusd_price
            else:
                logger.error(f'Failed to get abi. Error: {data["result"]}')

        except Exception as e:
            logger.error(e)

    def _value_with_slippage(self, amount: float, slippage: float) -> int:
        """Return value with slippage

        Args:
            amount (float): input value
            slippage (float): slippage %

        Returns:
            int: value - (value with slippage)
        """
        try:
            slippage = slippage / 100
            min_amount = amount - (amount * slippage)
            return min_amount
        except Exception as e:
            logger.error(e)

    def _get_deadline(self):
        """Return +3 min deadline

        Returns:
            int: deadline
        """
        try:
            now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            deadline = int(
                time.mktime(
                    datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S").timetuple()
                )
                + 60 * 3
            )
            return deadline
        except Exception as e:
            logger.error(e)

    def _randomise_value(self, value: float):
        """Return random value in (value * 95%, value * 105%)

        Args:
            value (float): input value

        Returns:
            float: output random value
        """
        try:
            percent = 5
            min_value = value - (value * (percent / 100))
            max_value = value + (value * (percent / 100))
            random_value = random.uniform(min_value, max_value)
            return random_value
        except Exception as e:
            logger.error(e)

    def stargate_bridge_1(self, private_key: str, value: float):
        """
        @ Starkgate Bridge
        @ https://app.optimism.io/quests/stargate-bridge-optimism
        @ [Arbitrum] buy 100+ usdc
        """

        address = self.optimism_core._get_checksum_address(
            self.optimism_core._get_address(private_key)
        )
        nonce = self.optimism_core._get_nonce(private_key)

        swap_exact_eth_for_tokens = self._get_arb_function_by_signature(
            contract_address="0x1b02da8cb0d097eb8d57a175b88c7d8b47997506",
            signature="0x7ff36ab5",
        )

        # value_eth = 0.0001  # TODO add random
        value_eth = self._randomise_value(value)

        value_usd = float(self._get_eth_price_arbitrum()) * value_eth
        slippage = 1
        value_with_slippage = self.optimism_core._convert_to_mwei_format(
            self._value_with_slippage(value_usd, slippage)
        )

        path_weth = self.optimism_core._get_checksum_address(
            "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
        )
        path_usdc = self.optimism_core._get_checksum_address(
            "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
        )

        amountOutMin = value_with_slippage
        path = [path_weth, path_usdc]
        to = address
        deadline = self._get_deadline()

        try:
            transaction = swap_exact_eth_for_tokens(
                amountOutMin, path, to, deadline
            ).buildTransaction(
                {
                    "chainId": 42161,
                    "gasPrice": self.optimism_core._web3.eth.gas_price,
                    "from": address,
                    "value": self.optimism_core._convert_to_ether_format(value_eth),
                    "nonce": nonce,
                }
            )

            signed_txn = self.optimism_core._sign_transaction(
                transaction=transaction, private_key=private_key
            )

            raw_tx_hash = self.optimism_core._send_raw_transaction(sign_txn=signed_txn)
            tx_hash = self.optimism_core._get_tx_hash(raw_tx_hash)
            logger.success(f"Wallet {address[:9]}, transaction hash - {tx_hash}")

        except Exception as e:
            logger.error(e)
