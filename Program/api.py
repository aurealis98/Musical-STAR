import requests
from time import sleep

API_KEY = ''        # To generate your own API Key, please go to README
URL = "http://ws.audioscrobbler.com/2.0/"


# Generic Error : -1
# No Artist Found : 6


def parameter(method: str, artist: str, api_key=API_KEY, return_format="json"):
    """Request format."""
    params = {
        "method": method,
        "artist": artist,
        "api_key": api_key,
        "format": return_format
    }
    return params


def handle_status_code(result: requests.Response):
    if result.status_code == 429:       # Rate limit reached.
        sleep(5)
        return 429
    elif result.status_code == 200:
        sleep(0.5)
        return 200


def search_artist(artist: str):
    params = parameter("artist.search", artist)
    result = requests.get(URL, params=params)
    status_code = handle_status_code(result)

    if status_code == 200:
        result = result.json()
        if len(result['results']['artistmatches']['artist']) == 0:
            return 6
        else:
            return result['results']['artistmatches']['artist']
    else:
        print("Error:", status_code)
        return -1


def get_similar_arists(artist: str, max_prizes: int, number_entered: int = 1):
    params = parameter("artist.getsimilar", artist)

    if number_entered == 1:
        pass
    elif number_entered == 2:
        if max_prizes%2 == 1:
            max_prizes = round(max_prizes/2) + 1
        else:
            max_prizes = round(max_prizes / 2)
    elif number_entered == 3:
        if max_prizes%2 == 1:
            max_prizes = round(max_prizes/2) + 1
        else:
            max_prizes = round(max_prizes/3)

    result = requests.get(URL, params=params)
    status_code = handle_status_code(result)

    if status_code == 200:
        result = result.json()
        if result.get('error') == 6:
            return 6

        if len(result['similarartists']['artist']) > max_prizes:
            return result['similarartists']['artist'][:max_prizes]
        else:
            return result['similarartists']['artist']
    else:
        print("Error:", status_code)
        return -1


def get_top_albums(artist: str):
    params = parameter("artist.getTopAlbums", artist)

    result = requests.get(URL, params=params)
    status_code = handle_status_code(result)
    if status_code == 200:
        result = result.json()
        if len(result) == 3:
            return "Could not be found"
        return result['topalbums']['album']
    else:
        print("Error:", status_code)
        return -1


def get_top_tracks(artist: str):
    params = parameter("artist.getTopTracks", artist)

    result = requests.get(URL, params=params)
    status_code = handle_status_code(result)
    if status_code == 200:
        result = result.json()
        if len(result) == 3:
            return "Could not be found"
        return result['toptracks']['track']
    else:
        print("Error:", status_code)
        return -1


def search_more_artists(artist_list: list, max_prizes: int):
    """Further search for more similar artists by going through a json file of artists and
    apply get_similar_artists() on each until a max number has been reached."""

    while len(artist_list) < max_prizes:

        for name in artist_list:
            more = get_similar_arists(name, max_prizes)

            if len(artist_list) + len(more) >= max_prizes:
                max_length = len(more)
                while len(artist_list) + max_length > max_prizes:
                    max_length -= 1

                artist_list = artist_list + more[:max_length]
                return artist_list
            else:
                artist_list = artist_list + more
        break

    return artist_list
