import json
import requests
import urllib


class PushRadar:
    __version = '3.0.0-alpha.1'
    __api_endpoint = 'https://api.pushradar.com/v3'
    __secret_key = None

    def __init__(self, secret_key):
        if (secret_key is None) or (not secret_key.startswith("sk_")):
            raise Exception("Please provide your PushRadar secret key. You can find it on the API page of your "
                            "dashboard.")
        self.__secret_key = secret_key.strip()

    def broadcast(self, channel_name, data):
        if (channel_name is None) or (channel_name.strip() == ''):
            raise Exception("Channel name empty. Please provide a channel name.")
        response = self._do_http_request('POST', self.__api_endpoint + '/broadcasts',
                                         {'channel': channel_name.strip(), 'data': data})
        if response['status'] == 200:
            return True
        else:
            raise Exception('An error occurred while calling the API. Server returned: ' +
                            response['body'])

    def auth(self, channel_name):
        if (channel_name is None) or (channel_name.strip() == ''):
            raise Exception("Channel name empty. Please provide a channel name.")
        if not channel_name.startswith('private-'):
            raise Exception("Channel authentication can only be used with private channels.")
        response = self._do_http_request('GET', self.__api_endpoint + '/channels/auth?channel=' +
                                         urllib.quote(channel_name.encode("utf-8")), {})
        if response['status'] == 200:
            return json.loads(response['body']).token
        else:
            raise Exception('There was a problem receiving a channel authentication token. Server returned: ' +
                            response['body'])

    def _do_http_request(self, method, url, data):
        headers = {'X-PushRadar-Library': 'pushradar-server-python ' + self.__version,
                   'Authorization': 'Bearer ' + self.__secret_key}
        r = None
        if method == 'post':
            r = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            r = requests.get(url, data=None, headers=headers)
        return {'body': r.json(), 'status': r.status_code}
