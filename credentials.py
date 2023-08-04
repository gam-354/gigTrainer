import json

CREDENTIALS_FILE_NAME = "credentials.json"
__credentials = {}

# Read the file and load the JSON data as dictionary
print(f"CREDENTIALS: loading {CREDENTIALS_FILE_NAME}")
credentials_file = open(CREDENTIALS_FILE_NAME)
__credentials = json.load(credentials_file)
credentials_file.close()       

# Get the value of a given credential
def get_credential(credentialName):

    if credentialName in __credentials.keys():
        return __credentials[credentialName]
    else:
        raise Exception(f"Could not find credential named '{credentialName}'")