import requests
from .exception import TeamsApiException

my_profile_url = "https://graph.microsoft.com/v1.0/me"
user_by_email_url = "https://graph.microsoft.com/v1.0/users/{})"


class Users:

    def __init__(self, auth):
        self._auth = auth

    def get_my_profile(self):
        headers = {'Authorization': 'Bearer ' + self._auth.access_token}
        response = requests.get(my_profile_url, headers=headers)
        if not response.ok:
            response.json()
        else:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])

    def get_user_by_email(self, email):
        headers = {'Authorization': 'Bearer ' + self._auth.access_token}
        response = requests.get(
            user_by_email_url.format(email), headers=headers)
        if not response.ok:
            response.json()
        else:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])
