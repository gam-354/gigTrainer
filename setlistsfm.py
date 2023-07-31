
import requests
import json

credentialsFile = open("credentials.json")

credentials = json.load(credentialsFile)

apiKey = credentials['setlistsFmApiKey']

apiUrl = "https://api.setlist.fm/rest/1.0/"


artistName = "King Gizzard"

headers = {
    'Accept' : 'application/json',
    'x-api-key' : apiKey
}

payload = {
    'artistName' : artistName,
    'sort' : 'sortName'
}

searchArtistCommand = "search/artists"

url = apiUrl + searchArtistCommand


response = requests.get(url, params=payload, headers=headers)

print(response.url)

print(response.json())



