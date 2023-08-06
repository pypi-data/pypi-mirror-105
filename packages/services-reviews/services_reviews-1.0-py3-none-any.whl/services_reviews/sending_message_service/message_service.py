import logging
import secrets
import string

from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from services_reviews.common_configs import MessageSenderConf
from services_reviews.common_utils.read_conf import ReadConf
from services_reviews.models.tables.review_requests_tables import RequestStatus, ReviewRequests
from services_reviews.sending_message_service.exceptions import SendingMessageException, \
    UnknownTemplateVariableException
from services_reviews.sending_message_service.message_crud import get_new_requests, get_template, get_branch_name, \
    is_link_unique
from services_reviews.sending_message_service.messages.messages_facade import send_message, init


class ConstClass:
    LINK_ALPHABET: str = string.ascii_letters + string.digits

    @staticmethod
    def get_config() -> MessageSenderConf:
        return ReadConf.get_parsed('message_sender')

    def __init__(self):
        self._link_size = None
        self._url_template = None

    @property
    def LINK_SIZE(self) -> int:
        if self._link_size is None:
            self._link_size = self.get_config().message_sender.link_size
        return self._link_size

    @property
    def URL_TEMPLATE(self) -> str:
        if self._url_template is None:
            self._url_template = self.get_config().message_sender.short_url_template
        return self._url_template


Const = ConstClass()

logging.basicConfig(level=logging.INFO)


def prepare_and_send_messages() -> None:
    """ Get new requests, prepare messages and send them. """
    init()
    for request in get_new_requests():
        logging.info(f'Processing phone number {request.phone}...')
        generate_link(request)
        logging.debug(f'Generated or retrieved link is {request.short_url}')
        try:
            message = get_message(request)
            logging.debug(f'Generated message is:\n{message}')
        except (SendingMessageException, NoResultFound, MultipleResultsFound) as e:
            logging.warning(f'An error occurred: {e}. Skip phone number {request.phone}')
            request.request_status = RequestStatus.ERROR_SENDING
        else:
            send_and_handle_status(request, message)
        logging.debug(f'Request status is {request.request_status}')


def generate_link(request: ReviewRequests) -> None:
    """ Generate unique link and save it to review request if there's no link yet. """
    if request.short_url is not None:
        return
    while True:
        link = ''.join(secrets.choice(Const.LINK_ALPHABET) for _ in range(Const.LINK_SIZE))
        if is_link_unique(link):
            break
    request.short_url = link


def get_message(request: ReviewRequests) -> str:
    """ Construct message with review request. """
    branch_name = get_branch_name(request.branch_id)
    template = get_template(request.branch_id)
    try:
        message = template.format(branch_name=branch_name, fio=request.fio, link=link_to_url(request.short_url))
    except KeyError as e:
        raise UnknownTemplateVariableException(f"Unknown template variable: {repr(e.args[0])}") from None
    return message


def link_to_url(link: str) -> str:
    """ Create https url from link postfix """
    return Const.URL_TEMPLATE.format(link)


def send_and_handle_status(request: ReviewRequests, message: str) -> None:
    """ Send message and save status in DB. """
    status = send_message(request.phone, message)
    if status:
        request.request_status = RequestStatus.SENT
    else:
        request.request_status = RequestStatus.ERROR_SENDING
