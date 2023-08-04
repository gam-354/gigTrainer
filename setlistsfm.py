
import requests
import credentials
import time

SETLISTSFM_API_KEY = credentials.get_credential("setlistsFmApiKey")
SETLISTSFM_API_URL = "https://api.setlist.fm/rest/1.0/"

SETLISTSFM_API_COMMAND_SEARCH_ARTIST = "search/artists"
SETLISTSFM_API_COMMAND_ARTIST = "artist/"
SETLISTSFM_API_COMMAND_SETLISTS = "setlists/"



SETLISTSFM_API_DEFAULT_HEADERS = {
    'Accept' : 'application/json',
    'x-api-key' : SETLISTSFM_API_KEY
}


def send_get_request(url, params={}, headers=SETLISTSFM_API_DEFAULT_HEADERS):

    response = requests.get(url, params=params, headers=headers)
    responseJson = response.json()

    print(f"Sending GET request: {response.url}")
    print(f"Response: {responseJson}")

    return response


def search_artist(artistName):

    url = SETLISTSFM_API_URL + SETLISTSFM_API_COMMAND_SEARCH_ARTIST

    payload = {
        'artistName' : artistName,
        'sort' : 'sortName'
    }

    response = send_get_request(url, params=payload)

    # response = requests.get(url, params=payload, headers=SETLISTSFM_API_DEFAULT_HEADERS)
    # responseJson = response.json()

    # print(f"Sending GET request: {response.url}")
    # print(f"Response: {responseJson}")

    # Raise exception if status code is not OK
    if response.ok:
        return response.json()['artist'][0]
    else:
        raise Exception(f"Could not find artist '{artistName}'")


def get_setlists(artistMbId):

    url = SETLISTSFM_API_URL + SETLISTSFM_API_COMMAND_ARTIST + artistMbId + "/" + SETLISTSFM_API_COMMAND_SETLISTS

    response = send_get_request(url)

#    response = requests.get(url, headers=SETLISTSFM_API_DEFAULT_HEADERS)
    responseJson = response.json()

    if not response.ok:
        raise Exception(f"Could not retrieve setlists")

    number_of_setlists = responseJson['total']
    print(f"Found {number_of_setlists} setlists")



# DEMO
if __name__ == '__main__':
    artist = search_artist("King Gizzard")
    print(f"Found artist: {artist['name']}")
    time.sleep(1)
    get_setlists(artist['mbid'])




