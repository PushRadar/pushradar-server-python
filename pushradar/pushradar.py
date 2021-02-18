import json
import requests

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class PushRadar:
    __version = '3.0.2'
    __api_endpoint = 'https://api.pushradar.com/v3'
    __secret_key = None

    def __init__(self, secret_key):
        if not isinstance(secret_key, str):
            raise Exception("Secret key must be a string.")
        if (secret_key is None) or (not secret_key.startswith("sk_")):
            raise Exception("Please provide your PushRadar secret key. You can find it on the API page of your "
                            "dashboard.")
        self.__secret_key = secret_key

    def broadcast(self, channel_name, data):
        if not isinstance(channel_name, str):
            raise Exception("Channel name must be a string.")
        if (channel_name is None) or (channel_name.strip() == ''):
            raise Exception("Channel name empty. Please provide a channel name.")
        response = self._do_http_request('POST', self.__api_endpoint + '/broadcasts',
                                         {'channel': channel_name, 'data': json.dumps(data)})
        if response['status'] == 200:
            return True
        else:
            raise Exception('An error occurred while calling the API. Server returned: ' +
                            json.dumps(response['body']))

    def auth(self, channel_name, socket_id):
        if not isinstance(channel_name, str):
            raise Exception("Channel name must be a string.")
        if (channel_name is None) or (channel_name.strip() == ''):
            raise Exception("Channel name empty. Please provide a channel name.")
        if not channel_name.startswith('private-'):
            raise Exception("Channel authentication can only be used with private channels.")
        if not isinstance(socket_id, str):
            raise Exception("Socket ID must be a string.")
        if (socket_id is None) or (socket_id.strip() == ''):
            raise Exception("Socket ID empty. Please pass through a socket ID.")
        response = self._do_http_request('GET', self.__api_endpoint + '/channels/auth?channel=' +
                                         quote(channel_name.encode("utf-8")) + '&socketID=' +
                                         quote(socket_id.encode("utf-8")), {})
        if response['status'] == 200:
            return response['body']['token']
        else:
            raise Exception('There was a problem receiving a channel authentication token. Server returned: ' +
                            json.dumps(response['body']))

    def _do_http_request(self, method, url, data):
        headers = {'X-PushRadar-Library': 'pushradar-server-python ' + self.__version,
                   'Authorization': 'Bearer ' + self.__secret_key,
                   'Content-Type': 'application/json'}
        r = None
        if method.lower() == 'post':
            r = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            r = requests.get(url, data=None, headers=headers)
        return {'body': r.json(), 'status': r.status_code}
