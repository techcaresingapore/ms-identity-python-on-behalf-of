import requests
from auth import AzureAuth
from dotenv import load_dotenv
import os
load_dotenv('productions.env')

def get_emails(access_token):
    get_messages_url = 'https://graph.microsoft.com/v1.0/me/messages'

    response = requests.get(
        get_messages_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    if response.status_code == 200:
        emails = response.json().get('value', [])
        for email in emails:
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']['emailAddress']['address']}")
            print(f"Body Preview: {email['bodyPreview']}\n")
    else:
        print(f"Failed to fetch emails: {response.status_code}, {response.text}")

# Example usage
if __name__ == "__main__":
    CLIENT_ID = os.environ.get('CLIENT_ID')
    TENANT_ID = os.environ.get('TENANT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    REDIRECT_URI = os.environ.get('REDIRECT_URI')

    auth = AzureAuth(CLIENT_ID, TENANT_ID, CLIENT_SECRET, REDIRECT_URI)
    
    # Get authorization URL to redirect the user
    auth_url = auth.get_authorization_url()
    print(f"Please go to this URL and authorize access: {auth_url}")
    
    # The user needs to paste the authorization code from the redirect URL
    authorization_code = input("Enter the authorization code: ")
    
    token = auth.get_token(authorization_code)
    get_emails(token)
