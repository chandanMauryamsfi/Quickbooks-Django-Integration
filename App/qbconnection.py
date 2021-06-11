from intuitlib.client import AuthClient
import requests


class QuickbooksConnection:

    auth_code = ''
    realm_id = ''
    client_id = ''
    client_secret = ''
    auth_client = object
    auth_header = {}

    def __init__(self):
        super().__init__()
        self.client_id = 'ABUU64LRq5F5qUk8bVw2YzSqTO2tGKvCF3FZl9MteGB3BZdaSI'
        self.client_secret = '6muTSNyKR8G6pW10dYnyUAZraB7pK9ryN6HBJE3J'
        self.base_url = 'https://sandbox-quickbooks.api.intuit.com'
        self.auth_client = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            environment='sandbox',
            redirect_uri='http://localhost:8000/callback',
        )

    def header(self):
        headers = {
            'Authorization': self.auth_header,
            'Accept': 'application/json'
        }
        return headers

    def getData(self, object):
        if object == 'employee':
            query = 'select * from Employee'
        elif object == 'item':
            query = 'select * from Item'
        elif object == 'time_activity':
            query = 'select * from TimeActivity'
        url = '{0}/v3/company/{1}/query?query={2}'.format(
            self.base_url, self.realm_id, query)

        headers = self.header()
        return requests.get(url, headers=headers)
