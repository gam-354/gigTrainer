
import requests
import credentials
import time

API_KEY = credentials.get_credential("setlistsFmApiKey")
API_URL = "https://api.setlist.fm/rest/1.0/"

API_COMMAND_SEARCH_ARTIST = "search/artists"
API_COMMAND_ARTIST = "artist/"
API_COMMAND_SETLISTS = "setlists/"

API_MIN_SECONDS_BETWEEN_REQUESTS = 0.6
API_SETLISTS_PER_PAGE = 20


API_DEFAULT_HEADERS = {
    'Accept' : 'application/json',
    'x-api-key' : API_KEY
}

timeLastRequest = 0.0

def send_get_request(url, params={}, headers=API_DEFAULT_HEADERS):

    global timeLastRequest

    # Ensure it's been enough time  so that a new request can be executed
    timeFromLastRequest = time.time() - timeLastRequest

    if timeFromLastRequest < API_MIN_SECONDS_BETWEEN_REQUESTS:
        remainingTime = API_MIN_SECONDS_BETWEEN_REQUESTS - timeFromLastRequest
        print(f"Waiting {remainingTime} to send request.")
        time.sleep(remainingTime)

    # Build and execute the request
    response = requests.get(url, params=params, headers=headers)
    print(f"Sending GET request: {response.url}")

    # Update the timestamp
    timeLastRequest = time.time()

    responseJson = response.json()
    print(f"Response: {responseJson}")

    return response


def search_artist(artistName):

    url = API_URL + API_COMMAND_SEARCH_ARTIST

    payload = {
        'artistName' : artistName,
        'sort' : 'sortName'
    }

    response = send_get_request(url, params=payload)

    # Raise exception if status code is not OK
    if response.ok:
        return response.json()['artist'][0]
    else:
        raise Exception(f"Could not find artist '{artistName}'")


def get_setlists(artistMbId, numSetlistsRequested=30):

    setlists = []
    page = 0
    numSetlistsAvailable = 1000

    while (len(setlists) < numSetlistsRequested) and (len(setlists) < numSetlistsAvailable):
        page += 1

        url = API_URL + API_COMMAND_ARTIST + artistMbId + "/" + API_COMMAND_SETLISTS

        payload = { 'p' : page }

        response = send_get_request(url, params=payload)
        responseJson = response.json()

        if not response.ok:
            raise Exception(f"Could not retrieve setlists")

        numSetlistsAvailable = responseJson['total']
        print(f"Found {numSetlistsAvailable} setlists")

        # Read the chunk of setlists and append them to the global list
        setlists += read_setlists_from_setlists_response(responseJson)
    
    
    #print("########################")
    #print(f"Num setlists downloaded: {len(setlists)}")

    # Clip to the num of setlists requested, in case more
    # setlists were downloaded accidentally
    setlists = setlists[:numSetlistsRequested]
    #print(f"Num setlists to return: {len(setlists)}")

    print(setlists)


def read_setlists_from_setlists_response(responseJson):

    setlists = []

    # Add setlists from these results
    for setlist in responseJson['setlist']:
        
        # Try to retrieve the song list. If not available, skip this setlist
        try:
            songlist = setlist['sets']['set'][0]['song']
        except:
            continue    
        
        #print(songlist)
        setlists.append(songlist)

    return setlists


# DEMO
if __name__ == '__main__':
    artist = search_artist("King Gizzard")
    print(f"Found artist: {artist['name']}")
    get_setlists(artist['mbid'])




