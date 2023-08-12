
import requests
import spotifyLoginResponse
import time

API_ACCOUNTS_URL = "https://accounts.spotify.com/api"
ACCOUNTS_URL = "https://accounts.spotify.com"

authentication_token = ""

def request(type, url, authenticated=False, header={}, params={}):

    if authenticated:
        header['Authorization'] = f"Bearer {authentication_token}"

    if type == "GET":
        response = requests.get(url, params=params, headers=header)
    elif type == "POST":
        response = requests.post(url, data=params, headers=header)

    print(f"Request sent: {response.url}")
    print(f"Request response: {response.json()}")
    print(f"Response OK? = {response.ok}")
    return response


def authenticate_basic(client_id, client_secret):
    
    global authentication_token
    url = API_ACCOUNTS_URL + "/token"

    header = {
        'Content-Type' : "application/x-www-form-urlencoded"
    }
    data = {
        'grant_type' : "client_credentials",
        'client_id' : client_id,
        'client_secret' : client_secret
    }

    result = request("POST", url, False, header, data)

    authentication_token = result.json()["access_token"]
    print(f"Authenticated with token: {authentication_token}")

def authenticate_user(appClientId, scopes):

    print("Starting Spotify Login Response server...")
    spotifyLoginResponse.start()
    time.sleep(2)

    url = ACCOUNTS_URL + "/authorize"

    data = {
        'client_id' : appClientId,
        'response_type' : "code",
        'redirect_uri' : spotifyLoginResponse.LOCAL_CALLBACK
    }

    if scopes != "":
        data['scope'] = scopes

    result = request("GET", url, False, params=data)

