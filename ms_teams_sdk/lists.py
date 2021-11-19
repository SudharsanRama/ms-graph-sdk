import requests
from .exception import TeamsApiException

list_team_channels_url = "https://graph.microsoft.com/v1.0/teams/{}/channels"
list_joined_teams_url = "https://graph.microsoft.com/v1.0/me/joinedTeams"


class List:
    def __init__(self, auth):
        self._auth = auth

    def list_joined_teams(self):
        headers = {'content-type': 'application/json',
                   'Authorization': 'Bearer ' + self._auth.access_token}
        response = requests.get(list_joined_teams_url, headers, verify=False)
        if not response.ok:
            return response.json()["value"]
        else:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])

    def list_team_channels(self, team_id):
        headers = {'content-type': 'application/json',
                   'Authorization': 'Bearer ' + self._auth.access_token}
        response = requests.get(list_team_channels_url.format(
            team_id), headers, verify=False)
        if not response.ok:
            return response.json()["value"]
        else:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])
