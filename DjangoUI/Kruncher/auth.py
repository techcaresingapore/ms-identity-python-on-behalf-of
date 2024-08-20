import requests
import os
from urllib.parse import urlencode

class AzureAuth:
    def __init__(self, client_id, tenant_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authority = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0"
        self.scope = ["https://graph.microsoft.com/.default", "User.Read", "Mail.Read"]

    def get_authorization_url(self):
        auth_url = f"{self.authority}/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "response_mode": "query",
            "scope": " ".join(self.scope),
        }
        return f"{auth_url}?{urlencode(params)}"

    def get_token(self, code):
        token_url = f"{self.authority}/token"
        data = {
            "client_id": self.client_id,
            "scope": " ".join(self.scope),
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "client_secret": self.client_secret,
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
