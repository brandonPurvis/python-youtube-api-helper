# Python-Youtube Api

A collection of helper functions which I use to simplify interfacing
with the youtube api via google's python api client. 

- [Google APIs Client for Python](https://developers.google.com/api-client-library/python/)
- [Youtube Data API Docs](https://developers.google.com/youtube/v3/)


## To Use 
The google-api-python-client is the only requirement.

- `pip install google-api-python-client`


## Examples

### Get a channels subscriptions:

```python
import ytapi
from secrets import YOUTUBE_DATA_API_KEY

CHANNEL_ID = ...

service = ytapi.create_service('youtube', 'v3', YOUTUBE_DATA_API_KEY)

for channel in ytapi.subscriptions(CHANNEL_ID, service):
    print(channel.name, channel.channel_id)
```
