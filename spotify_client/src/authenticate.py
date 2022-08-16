import base64
import requests


class CreateAuthorization:
    def __new__(cls, client_id=None, client_secret=None):
        """
        Create authorization token from base64 encoding the client ID
        and the client secret when registering your app in the Spotify
        developers site.
        """
        encoded_token = f"{client_id}:{client_secret}".encode("utf-8")
        authorization_token = base64.standard_b64encode(encoded_token)
        return authorization_token.decode('utf-8')


class GetToken:
    def __new__(cls, encoded_token=None):
        header = {
            "Authorization": f"Basic {encoded_token}"
        }
        data = {
            "grant_type": "client_credentials"
        }
        url = "https://accounts.spotify.com/api/token"
        req = requests.post(url=url, data=data, headers=header)

        return req.json().get('access_token')


