
import os
import json
import urllib.parse
import credentials

class SpotifyRequest: 
    authentication_token = ""
    def __init__(self):
        pass

    def request(self,type, url, header,body):
        command = f'curl -X {type} "{url}" -H "{header}" -d "{body}"'
        if body=="":
            command = f'curl -X {type} "{url}" -H "{header}"'
        print(command)
        return self.execute_command(command)


    def execute_command(self, command):
        result = os.popen(command).read()
        return result 

    def authenticate(self,client_id, client_secret):

        header = ""
        body = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        result = self.request("POST", "https://accounts.spotify.com/api/token", header + "Content-Type: application/x-www-form-urlencoded", body)
        print(result)
        self.authentication_token = json.loads(result)["access_token"]
        print(self.authentication_token)

    def authenticated_request(self,type, url, header,body):
        authenticated_header=header+f"Authorization: Bearer {self.authentication_token}"
        return self.request(type, url, authenticated_header, body)
    def search(self,artist):
        artist_encoded=urllib.parse.quote(artist)
        query=urllib.parse.quote(f"{artist}")
        type="artist"
        url=f"https://api.spotify.com/v1/search?q={query}&type={type}"
        result = self.authenticated_request("GET",url,"","")

        print(result)
        uid = json.loads(result)["artists"]["href"]
        print(uid)


def main():
    client_id = credentials.get_credential("spotifyClientId")
    client_secret = credentials.get_credential("spotifyClientSecret")

    request = SpotifyRequest()
    request.authenticate(client_id, client_secret)
    request.search("Taylor Swift")



if __name__ == '__main__':
    main()
