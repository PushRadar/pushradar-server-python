<p align="center"><a href="https://pushradar.com" target="_blank"><img src="https://pushradar.com/images/logo/pushradar-logo-dark.svg" width="300"></a></p>

<p align="center">
    <a href="https://pypi.org/project/pushradar"><img src="https://img.shields.io/pypi/v/pushradar?cacheSeconds=60&color=5b86e5"></a>
    <a href="https://pypi.org/project/pushradar"><img src="https://img.shields.io/pypi/dm/pushradar?cacheSeconds=60&color=5b86e5"></a>
    <a href="https://pypi.org/project/pushradar"><img src="https://img.shields.io/pypi/l/pushradar?cacheSeconds=60&color=5b86e5"></a>
</p>
<br />

## PushRadar Python Server Library

[PushRadar](https://pushradar.com) is a realtime API service for the web. The service uses a simple publish-subscribe model, allowing you to broadcast "messages" on "channels" that are subscribed to by one or more clients. Messages are pushed in realtime to those clients.

This is PushRadar's official Python server library.

## Prerequisites

In order to use this library, please ensure that you have the following:

- Python 3.3+
- A PushRadar account - you can sign up at [pushradar.com](https://pushradar.com)

## Installation

The easiest way to get up and running is to install the library using Pip or Pipenv. Run the following command in your console:

```bash
$ pip install pushradar
```

or

```bash
$ pipenv install pushradar
```

## Broadcasting Messages

```python
import pushradar

radar = pushradar.PushRadar('your-secret-key')
radar.broadcast('channel-1', {'message': 'Hello world!'})
```

## Receiving Messages

```html
<script src="https://pushradar.com/js/v3/pushradar.min.js"></script>
<script>
    var radar = new PushRadar('your-public-key');
    radar.subscribe.to('channel-1', function (data) {
        console.log(data.message);
    });
</script>
```

## Private Channels

Private channels require authentication and start with the prefix **private-**. We recommend that you use private channels by default to prevent unauthorised access to channels.

You will need to set up an authentication endpoint that returns a token using the `auth(...)` method if the user is allowed to subscribe to the channel. For example:

```python
radar = pushradar.PushRadar('your-secret-key')
if request.method == 'GET':
    channel_name = request.GET.get('channelName')
    socket_id = request.GET.get('socketID')
    # is user allowed to access channel?
    if True:
        return json.dumps({"token": radar.auth(channel_name, socket_id)})
```

Then register your authentication endpoint by calling the `auth(...)` method client-side:

```javascript
radar.auth('/auth');
```

## Presence Channels

Presence channels require authentication and start with the prefix **presence-**. Presence channels are eligible for 'presence messages' containing information about channel subscribers.

You will need to set up an authentication endpoint as with private channels (see above). You should then register a `onPresence(...)` callback which will be called periodically. Your callback should accept two parameters: subscriber count and subscriber data. For example:

```javascript
radar.auth('/auth');
radar.call.on.connection('/connected');

radar.subscribe.to('presence-channel-1', function (data) {
    console.log(data.message);
}).onPresence(function (count, clientData) {
    console.log(count);
});
```

If you wish to pass through subscriber (client) data, you can set up an endpoint and pass its URL to the `call.on.connection(...)` method. Your endpoint will be called when a user first connects to the service. From your endpoint you can register client data as follows:

```python
radar = pushradar.PushRadar('your-secret-key')
if request.method == 'POST':
    socket_id = request.POST.get('socketID')
    radar.register_client_data(socket_id, {'##uniqueID': 1, 'name': 'James Smith'})
```

## Complete Documentation

Complete documentation for PushRadar's Python server library can be found at: <https://pushradar.com/docs/3.x/python>

## License

Copyright © 2021, PushRadar. PushRadar's Python server library is licensed under the MIT license:
<https://opensource.org/licenses/mit-license.php>