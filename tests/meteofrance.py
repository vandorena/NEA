import json
import requests
import time

# Example of a Python implementation for a continuous authentication client.
# It's necessary to :
# - update APPLICATION_ID
# - update request_url at the end of the script

# unique application id : you can find this in the curl's command to generate jwt token 
APPLICATION_ID = 'xxxxx'

# url to obtain acces token
TOKEN_URL = "https://portail-api.meteofrance.fr/token"

class Client(object):

    def __init__(self):
        self.session = requests.Session()

    def request(self, method, url, **kwargs):
        # First request will always need to obtain a token first
        if 'Authorization' not in self.session.headers:
            self.obtain_token()

        # Optimistically attempt to dispatch reqest
        response = self.session.request(method, url, **kwargs)
        if self.token_has_expired(response):
            # We got an 'Access token expired' response => refresh token
            self.obtain_token()
            # Re-dispatch the request that previously failed
            response = self.session.request(method, url, **kwargs)

        return response

    def token_has_expired(self, response):
        status = response.status_code
        content_type = response.headers['Content-Type']
        if status == 401 and 'application/json' in content_type:
            repJson = response.text
            if 'Invalid JWT token' in repJson['description']:
                return True
        return False

    def obtain_token(self):
        # Obtain new token
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': 'Basic ' + APPLICATION_ID}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=False, headers=headers)
        token = access_token_response.json()['access_token']
        # Update session with fresh token
        self.session.headers.update({'Authorization': 'Bearer %s' % token})

def main():
    client = Client()
    # Issue a series of API requests an example.  For use this test, you must first subscribe to the arome api with your application
    client.session.headers.update({'Accept': 'application/json'})

    for i in range(100):
        response = client.request('GET', 'https://public-api.meteofrance.fr/
        public/arome/1.0/wms/MF-NWP-HIGHRES-AROME-001-FRANCE-WMS/GetCapabilities?service=WMS&version=1.3.0', verify=False)
        print(response.status_code)
        time.sleep(120)


if __name__ == '__main__':
    main()