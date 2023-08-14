
import credentials
import spotifyRequests

API_URL = "https://api.spotify.com/v1"
SEARCH_COMMAND = "/search"

def search_artist(artistName):

    url = API_URL + "/search"
    params = {
        'q' : artistName,
        'type' : 'artist'
    }

    result = spotifyRequests.request("GET", url, authenticated=True, params=params)
    resultJson = result.json()

    # Keep the first result from the list
    artist = resultJson['artists']['items'][0]['name']
    uid = resultJson['artists']['items'][0]['id']

    print(f"Found artist '{artist}' with id '{uid}'")
    
def create_playlist(userId, name):

    data = {
        "name": name,
        "description": "New playlist description",
        "public": "false"
    }

    header = {
        'Content-Type' : "application/x-www-form-urlencoded"
    }

    url = API_URL + f"/users/{userId}/playlists"

    # Se necesita estar autenticado con unos scopes concretos. Leer:
    # https://developer.spotify.com/documentation/web-api/tutorials/code-flow

    result = spotifyRequests.request("POST", url, authenticated=True, params=data, header=header)

    print(result.json())



def main():
    client_id = credentials.get_credential("spotifyClientId")
    client_secret = credentials.get_credential("spotifyClientSecret")

    userId = credentials.get_credential("spotifyUserIdGuille")
    scopes = "playlist-modify-public playlist-modify-private"

    #spotifyRequests.authenticate_basic(client_id, client_secret)
    #search_artist("Taylor Swift")
    #create_playlist(userId,"wisi wisi")

    spotifyRequests.authenticate_user(client_id, scopes)

if __name__ == '__main__':

    main()
