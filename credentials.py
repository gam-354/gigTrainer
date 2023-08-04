import json

credentials_file_name = "credentials.json"
__credentials = {}

# Read the file and load the JSON data as dictionary
credentials_file = open(credentials_file_name)
__credentials = json.load(credentials_file)
credentials_file.close()       

# Get the value of a given credential
def get_credential(credentialName):

    if credentialName in __credentials.keys():
        return __credentials[credentialName]
    else:
        raise Exception(f"Could not find credential named '{credentialName}'")