import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

from library.settings import CONSUMER_KEY, CONSUMER_SECRET


def get_access_token():

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            settings.CONSUMER_KEY,
            settings.CONSUMER_SECRET
        )
    )

    return response.json()['access_token']