import logging

import requests
from stellar_base.keypair import Keypair


logger = logging.getLogger(__name__)


def create_new_address():
    kp = Keypair.random()
    public_key = kp.address().decode()
    seed = kp.seed().decode()
    return seed, public_key


def ask_for_coins(public_key):
    url = f"https://horizon-testnet.stellar.org/friendbot?addr={public_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return True, None
    else:
        data = response.json()
        logger.warning(data["detail"], extra={"response_data": data})
        return False, data["detail"]
