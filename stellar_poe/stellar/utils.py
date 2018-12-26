import logging

import requests
from stellar_base.builder import Builder
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


def create_transaction(sender_seed, recipient_key, hash_value):
    builder = Builder(secret=sender_seed)
    builder.append_payment_op(recipient_key, "1", "XLM")
    builder.add_hash_memo(hash_value.encode())
    builder.sign()
    # TODO: handle possible errors
    return builder.submit()
