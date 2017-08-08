from apiclient.discovery import build


def create_service(service, version, key):
    """
    Create a keyed google api service.
    """
    return build(service, version, developerKey=key)


def subscriptions(channel_id, ytservice):
    """
    Generates the full subscription list for a channel. 
    """
    next_page_token = 'None'
    while next_page_token:
        if next_page_token == 'None': 
            next_page_token = None

        response = ytservice.subscriptions().list(
            part='snippet',
            channelId=channel_id,
            pageToken=next_page_token,
        ).execute()

        channels = response.get('items')
        next_page_token = response.get('nextPageToken')
        for item in channels:
            yield ChannelSnippetResponseWrapper(item)


def uploads(channel_id, ytservice):
    # Get channels uploads playlist id
    content_details_resp = ytservice.channels().list(
        id=channel_id,
        part='ContentDetails',
    ).execute()
    content_details = one_item_response(content_details_resp)
    uploads_playlist_id = playlists_from_content_details(content_details)['uploads']

    # Get video ids from playlistItems 
    next_page_token = 'None'
    while next_page_token:
        if next_page_token == 'None':
            next_page_token = None

        playlist_resp = ytservice.playlistItems().list(
            part='ContentDetails',
            playlistId=uploads_playlist_id,
            pageToken=next_page_token,
        ).execute()
        next_page_token = playlist_resp.get('nextPageToken')

        # Retreive video info   
        for item in playlist_resp['items']:
            video_id = item['contentDetails']['videoId']
            video_info = one_item_response(
                ytservice.videos().list(
                    id=video_id,
                    part='snippet',
                ).execute()
            )

            yield VideoSnippetResponseWrapper(video_info)


def channel_from_snippet(resp):
    """
    Convert a Youtube api snippet response into a dictionary of channel info.

    Contains: name, image, description, channel_id
    """
    return {
        'name': resp['snippet']['title'],
        'image': resp['snippet']['thumbnails']['high']['url'],
        'description': resp['snippet']['description'],
        'channel_id': resp['snippet']['resourceId']['channelId'],
    }


def video_from_snippet(resp):
    """ Convert a Youtube api snippet response into a dictionary of video info.

        Contains: name, image, description, channel_id, video_id
    """
    return {
        'name': resp['snippet']['title'],
        'image': resp['snippet']['thumbnails']['high']['url'],
        'description': resp['snippet']['description'],
        'channel_id': resp['snippet']['channelId'],
        'date': resp['snippet']['publishedAt'],
        'video_id': resp['id'],
    }


def playlists_from_content_details(resp):
    return resp['contentDetails']['relatedPlaylists']


def one_item_response(resp):
    return resp['items'][0]


class ChannelSnippetResponseWrapper(object):
    def __init__(self, resp):
        self._resp = resp

    @property
    def name(self):
        return self._resp['snippet']['title']

    @property
    def image(self):
        return self._resp['snippet']['thumbnails']['high']['url']

    @property
    def description(self):
        return self._resp['snippet']['description']

    @property
    def channel_id(self):
        return self._resp['snippet']['resourceId']['channelId']

    @property
    def data(self):
        return channel_from_snippet(self._resp)

    def __str__(self):
        return "<ChannelSnippet {}>".format(self.name)

    def __repr__(self):
        return str(self)


class VideoSnippetResponseWrapper(object):
    def __init__(self, resp):
        self._resp = resp

    @property
    def name(self):
        return self._resp['snippet']['title']

    @property
    def image(self):
        return self._resp['snippet']['thumbnails']['high']['url']

    @property
    def description(self):
        return self._resp['snippet']['description']

    @property
    def channel_id(self):
        return self._resp['snippet']['channelId']

    @property
    def video_id(self):
        return self._resp['id']

    @property
    def date(self):
        return self._resp['snippet']['publishedAt']

    @property
    def data(self):
        return video_from_snippet(self._resp)
    
    def __str__(self):
        return "<VideoSnippet {} {}>".format(self.name, self.channel_id)

    def __repr__(self):
        return str(self)
