import logging

from services_reviews.common_configs import DB_CONFIG_DIR, MESSAGE_SENDER_CONFIG_DIR
from services_reviews.common_utils.db_connect import dbConnector as dbc
from services_reviews.common_utils.read_conf import ReadConf
from services_reviews.sending_message_service.message_service import prepare_and_send_messages

logging.basicConfig(level=logging.INFO)


def sending_message_service() -> None:
    """ скрипт для отправки запросов на отзвывы """

    # todo: unit test
    ReadConf.read('message_sender', MESSAGE_SENDER_CONFIG_DIR)
    ReadConf.read('db', DB_CONFIG_DIR)

    try:
        logging.info('Connecting to database')
        dbc.start_connect_db()

        logging.info('Preparing and sending messages')
        prepare_and_send_messages()

        logging.info('Saving changes')
        dbc.session.commit()

        logging.info('Completed successfully')
    finally:
        dbc.disconnect()
