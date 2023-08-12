
import requests
import credentials
import time

API_KEY = credentials.get_credential("setlistsFmApiKey")

API_MIN_SECONDS_BETWEEN_REQUESTS = 0.7

API_DEFAULT_HEADERS = {
    'Accept' : 'application/json',
    'x-api-key' : API_KEY
}

timeLastRequest = 0.0

def detect_too_many_requests_error(response):
    responseJson = response.json()

    if not response.ok and responseJson['message'] == "Too Many Requests":
        print("ERROR: too many requests! Retrying...")
        return True
    else:
        return False


def wait_until_available():
    global timeLastRequest

    # Ensure it's been enough time  so that a new request can be executed
    timeFromLastRequest = time.time() - timeLastRequest

    if timeFromLastRequest < API_MIN_SECONDS_BETWEEN_REQUESTS:
        remainingTime = API_MIN_SECONDS_BETWEEN_REQUESTS - timeFromLastRequest
        print(f"Waiting {remainingTime} to send request.")
        time.sleep(remainingTime)

    # Update the timestamp
    timeLastRequest = time.time()


def send_get_request(url, params={}, headers=API_DEFAULT_HEADERS):

    mustRetry = True

    while mustRetry:
        wait_until_available()

        # Build and execute the request
        response = requests.get(url, params=params, headers=headers)
        print(f"Sending GET request: {response.url}")

        mustRetry = detect_too_many_requests_error(response)

    responseJson = response.json()
    print(f"Response: {responseJson}")

    return response

