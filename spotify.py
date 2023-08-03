
import os
import json
import base64
import urllib.parse
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


def obtain_credentials(file_path):
    credentials = list()
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            credentials.append(line)
    return credentials
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Obtain artist from spotify.')
    parser.add_argument('file_path', type=str, help='Path to a file containing the keys to authenticate to Spotify')
    args = parser.parse_args()

    credentials = obtain_credentials(args.file_path)

    request = SpotifyRequest()
    request.authenticate(credentials[0], credentials[1])
    request.search("Taylor Swift")



if __name__ == '__main__':
    main()
