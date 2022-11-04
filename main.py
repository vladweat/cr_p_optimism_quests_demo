import config

from quests_engine import QuestsEngine
from optimism_core import OptimismClient


def main():
    client = OptimismClient(run=config.RUN_SCRIPT, network="arbitrum")
    engine = QuestsEngine(client)

    keys_list = client._get_private_keys()
    for key in keys_list:
        engine.stargate_bridge_1(private_key=key, value=0.0001)

    # # ЗАПУСК ЧЕГО ЛИБО ОТДЕЛЬНО ПО КЛЮЧАМ
    # keys_list = client._get_private_keys()
    # for key in client._get_private_keys():
    #     print(client._get_balance(key))


if __name__ == "__main__":
    main()
