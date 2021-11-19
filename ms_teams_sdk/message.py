import json
import requests
from .exception import TeamsApiException

channel_message_url = "https://graph.microsoft.com/v1.0/teams/{}/channels/{}/messages"
chat_url = "https://graph.microsoft.com/v1.0/chats"
chat_message_url = "https://graph.microsoft.com/v1.0/chats/{}/messages"


class Message:

    def __init__(self, auth):
        self._auth = auth

    def create_chat(self, from_id, to_id):
        request_body = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": [
                        "owner"
                    ],
                    "user@odata.bind": "https://graph.microsoft.com/v1.0/users('{}')".format(from_id)
                },
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": [
                        "owner"
                    ],
                    "user@odata.bind": "https://graph.microsoft.com/v1.0/users('{}')".format(to_id)
                }
            ]
        }
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self._auth.access_token}
        response = requests.post(chat_url, data=json.dumps(request_body), headers=headers, verify=False)
        if not response.ok:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])
        return response.json()

    def send_channel_message(self, team_id, channel_id, content_type, content, hosted_content=None):
        headers = {'content-type': 'application/json',
                   'Authorization': 'Bearer ' + self._auth.access_token}
        message = {
            "body": {
                "contentType": content_type,
                "content": content
            }
        }
        if hosted_content:
            message.update({"hostedContents": hosted_content})
        response = requests.post(channel_message_url.format(
            team_id, channel_id), data=json.dumps(message), headers=headers, verify=False)
        if not response.ok:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])
        return

    def send_user_message(self, chat_id, content_type, content, hosted_content=None):
        headers = {'content-type': 'application/json',
                   'Authorization': 'Bearer ' + self._auth.access_token}
        message = {
            "body": {
                "contentType": content_type,
                "content": content
            }
        }
        if hosted_content:
            message.update({"hostedContents": hosted_content})
        response = requests.post(chat_message_url.format(
            chat_id), data=json.dumps(message), headers=headers, verify=False)
        if not response.ok:
            raise TeamsApiException(
                response.json()['error']['code'], response.json()['error']['message'])
        return
