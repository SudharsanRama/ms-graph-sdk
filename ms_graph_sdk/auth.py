import requests
from urllib.parse import urlencode
from .exception import TeamsApiException

authorize_url = "https://login.microsoftonline.com/{}/oauth2/v2.0/authorize?"
token_url = "https://login.microsoftonline.com/{}/oauth2/v2.0/token"


class Auth:

    def __init__(self, tenant_id, client_id, client_secret, scope, store_tokens=None):
        """
        Initialize the ms-teams-sdk auth object with the identifiers, scopes and redirect_uri
        configured while creating the Azure Active Directory App on Azure Portal

        :rtype: Auth
        :param tenant_id: The tenant id of your organization
        :type tenant_id: str
        :param client_id: The client id of your AD application
        :type client_id: str
        :param client_secret: The secret value in Certificates & Secrets
        :type client_secret: str
        :param scope: The list of scope required for your app
        :type scope: list

        """
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.data = {
            'client_id': client_id,
            'scope': ' '.join(scope)
        }
        self.store_tokens = store_tokens
        self.access_token = None

    def get_authorization_url(self, redirect_uri):
        """
        Returns authentication URL for granting permissions and
        get authorization code on behalf of a user
        https://docs.microsoft.com/en-us/graph/auth-v2-user

        :param redirect_uri: The redirect URI for your app
        :type redirect_uri: str
        :return: Authorization URL
        :rtype: str
        """
        url = authorize_url.format(self.tenant_id)
        data = dict(self.data)
        data.update({
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'response_mode': 'query',
            'state': '12345'
        })
        return url + urlencode(data)

    def authenticate(self, redirect_uri, **kwargs):
        """
        Get object with access and refresh token either using authorization code (code)
        or refresh token (refresh_token)

        :param redirect_uri: The redirect URI for your app
        :type redirect_uri: str
        :Keyword Arguments:
        * *code* (``str``) --
          Authorization code you get from granting permission to your application
        * *refresh_token* (``str``) --
          Previously generated refresh_token that is expired currently
        :return: Dictionary containing access & refresh tokens
        :rtype: dict
        """
        data = dict(self.data)
        key, value = kwargs.popitem()
        data.update({
            'redirect_uri': redirect_uri,
            'client_secret': self.client_secret,
            key: value,
            'grant_type': 'authorization_code' if key == 'code' else 'refresh_token'
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            token_url.format(self.tenant_id), data=data, headers=headers)
        if not response.ok:
            raise TeamsApiException(response.json()['error']['code'], response.json()['error']['message'])
        access_token, refresh_token = response.json()['access_token'], response.json()['refresh_token']
        if self.store_tokens:
            self.store_tokens(access_token, refresh_token)
        self.access_token = access_token
        return access_token, refresh_token
