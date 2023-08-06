import logging

import services_reviews.sending_message_service.messages.smsc.smsc_api as smsc_api
from services_reviews.common_configs import MessageSenderConf
from services_reviews.common_utils.read_conf import ReadConf

logging.basicConfig(level=logging.INFO)

_smsc = smsc_api.SMSC()


# todo: convert facade and service (and crud?) to classes
def init():
    config: MessageSenderConf = ReadConf.get_parsed('message_sender')
    smsc_api.SMSC_LOGIN = config.smsc.login
    smsc_api.SMSC_PASSWORD = config.smsc.api_password
    smsc_api.SMSC_DEBUG = config.smsc.debug

    global COST_THRESHOLD
    COST_THRESHOLD = config.message_sender.max_message_cost


def send_message(phone: str, message: str) -> bool:
    balance = float(_smsc.get_balance())
    cost, _ = _smsc.get_sms_cost(phone, message)
    cost = float(cost)
    if cost > balance:
        logging.error(f'Balance is {balance}, cost is {cost}. We need more money!')
        return False
    if cost > COST_THRESHOLD:
        logging.warning(f'Cost is {cost}, but threshold is {COST_THRESHOLD}. Too expensive message, skip it.')
        return False

    _, _, final_cost, _ = _smsc.send_sms(phone, message)
    final_cost = float(final_cost)
    if final_cost != cost:
        logging.warning(f'Something went wrong: preparing cost was {cost}, but final cost is {final_cost}. '
                        f'Need to check at smsc.ru.')
    return True
