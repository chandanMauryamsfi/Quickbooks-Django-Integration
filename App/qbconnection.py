from intuitlib.client import AuthClient
import requests
from quickbookIntegration.celery import app

#singleton class to connect with quickbooks
class QuickbooksConnection:
    auth_code = ''
    realm_id = ''
    client_id = ''
    client_secret = ''
    auth_client = object
    auth_header = {}
    __instance__ = None  
      
    def __init__(self):
        #creating for checking single instance
        if QuickbooksConnection.__instance__ is None:
            QuickbooksConnection.__instance__ = self  
        else:
            pass
        self.client_id = 'ABUU64LRq5F5qUk8bVw2YzSqTO2tGKvCF3FZl9MteGB3BZdaSI'
        self.client_secret = '6muTSNyKR8G6pW10dYnyUAZraB7pK9ryN6HBJE3J'
        self.auth_client = AuthClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            environment='sandbox',
            redirect_uri='http://localhost:8000/callback',
        )
        self.base_url = 'https://sandbox-quickbooks.api.intuit.com'
    
    @staticmethod  
    def get_instance():  
       # We define the static method to fetch instance  
        if not QuickbooksConnection.__instance__:  
            QuickbooksConnection()  
        return QuickbooksConnection.__instance__  

    def header(self):
        headers = {
            'Authorization': self.auth_header,
            'Accept': 'application/json'
        }
        return headers

qbconn = QuickbooksConnection()