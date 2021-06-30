from intuitlib.client import AuthClient

from Apps.qb_app.constants import REDIRECT_URL, QB_ENVIRONMENT
from quickbookIntegration.celery import app
from quickbookIntegration import settings


class QuickbooksConnection:
    auth_code = ''
    realm_id = ''
    client_id = ''
    client_secret = ''
    auth_client = object
    auth_header = {}
    __instance__ = None

    def __init__(self):
        # creating for checking single instance
        if QuickbooksConnection.__instance__ is None:
            QuickbooksConnection.__instance__ = self
        else:
            pass
        self.client_id = settings.QUICKBOOKS_CLIENT_ID
        self.client_secret = settings.QUICKBOOKS_CLIENT_KEY
        self.auth_client = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            environment=QB_ENVIRONMENT,
            redirect_uri=REDIRECT_URL,
        )

    @staticmethod
    def get_instance():
        if not QuickbooksConnection.__instance__:
            QuickbooksConnection()
        return QuickbooksConnection.__instance__


qbconn = QuickbooksConnection()
