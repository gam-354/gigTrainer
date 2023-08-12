
import setlistsfmRequests

API_URL = "https://api.setlist.fm/rest/1.0/"

API_COMMAND_SEARCH_ARTIST = "search/artists"
API_COMMAND_ARTIST = "artist/"
API_COMMAND_SETLISTS = "setlists/"

API_SETLISTS_PER_PAGE = 20


def search_artist(artistName):

    url = API_URL + API_COMMAND_SEARCH_ARTIST

    payload = {
        'artistName' : artistName,
        'sort' : 'relevance'
    }

    response = setlistsfmRequests.send_get_request(url, params=payload)

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

        response = setlistsfmRequests.send_get_request(url, params=payload)
        responseJson = response.json()

        if not response.ok:
            raise Exception(f"Could not retrieve setlists")

        numSetlistsAvailable = responseJson['total']
        print(f"Found {numSetlistsAvailable} setlists")

        # Read the chunk of setlists and append them to the global list
        setlists += read_setlists_from_setlists_response(responseJson)
    
    # Clip to the num of setlists requested, in case more
    # setlists were downloaded accidentally
    setlists = setlists[:numSetlistsRequested]

    #print(setlists)
    return setlists


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


def get_most_listened_songs(setlistsList, howMany=25):

    songsAndPlays = {}

    for setlist in setlistsList:
        for song in setlist:

            # Increase song play count, or add entry to the dict
            songName = song['name']

            if songName in songsAndPlays.keys():
                songsAndPlays[songName] += 1
            else:
                songsAndPlays[songName] = 1

    # Sorted will return a list of tuples, so convert it back to dictionary
    mostPlayed = dict(sorted(songsAndPlays.items(), key=lambda x:x[1], reverse=True))

    # Clip the list to the number of songs requested
    return dict(list(mostPlayed.items())[:howMany])


def demo(artistName):
    artist = search_artist(artistName)
    print(f"Found artist: {artist['name']}")
    kgSetlists = get_setlists(artist['mbid'], 60)
    most = get_most_listened_songs(kgSetlists)
    print(most)

# DEMO
if __name__ == '__main__':
    demo("Taylor Swift")
