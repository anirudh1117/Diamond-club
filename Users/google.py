from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
           
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request(),
            '461998924717-nlhg007hcr65ukd4ldsol52okh9uc18h.apps.googleusercontent.com')

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return "The token is either invalid or has expired"
