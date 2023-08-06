
import credentials
import requests

class SpotifyRequest: 
    authentication_token = ""
    def __init__(self):
        pass

    def request(self, type, url, authenticated=False, header={}, params={}):

        if authenticated:
            header['Authorization'] = f"Bearer {self.authentication_token}"

        if type == "GET":
            response = requests.get(url, params=params, headers=header)
        elif type == "POST":
            response = requests.post(url, data=params, headers=header)

        print(f"Request sent: {response.url}")
        print(f"Request response: {response.json()}")
        return response


    def authenticate(self, client_id, client_secret):
        url = "https://accounts.spotify.com/api/token"

        header = {
            'Content-Type' : "application/x-www-form-urlencoded"
        }
        data = {
            'grant_type' : "client_credentials",
            'client_id' : client_id,
            'client_secret' : client_secret
        }

        result = self.request("POST", url, False, header, data)

        self.authentication_token = result.json()["access_token"]
        print(f"Authenticated with token: {self.authentication_token}")
    

    def search(self,artistName):

        url = "https://api.spotify.com/v1/search"
        params = {
            'q' : artistName,
            'type' : 'artist'
        }

        result = self.request("GET", url, authenticated=True, params=params)
        resultJson = result.json()

        # Keep the first result from the list
        artist = resultJson['artists']['items'][0]['name']
        uid = resultJson['artists']['items'][0]['id']

        print(f"Found artist '{artist}' with id '{uid}'")
       


def main():
    client_id = credentials.get_credential("spotifyClientId")
    client_secret = credentials.get_credential("spotifyClientSecret")

    request = SpotifyRequest()
    request.authenticate(client_id, client_secret)
    request.search("Taylor Swift")



if __name__ == '__main__':
    main()
