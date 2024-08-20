import msal
import requests
from flask import Flask, redirect, request, url_for, session
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Read environment variables
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
AUTHORITY = os.environ.get("AUTHORITY")  # Use the common endpoint
SCOPE = os.environ.get("SCOPE")

# Initialize the MSAL confidential client application
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

# Initialize Flask application
flask_app = Flask(__name__)
flask_app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")

@flask_app.route('/')
def index():
    # Build the authorization URL to get the authorization code
    auth_url = app.get_authorization_request_url(
        scopes=SCOPE.split(),
        redirect_uri=REDIRECT_URI,
    )
    return redirect(auth_url)

@flask_app.route('/account/callback')
def callback():
    authorization_code = request.args.get('code')
    if not authorization_code:
        return "Authorization code not found in the redirect URL"

    # Exchange the authorization code for an access token
    token_response = app.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=SCOPE.split(),
        redirect_uri=REDIRECT_URI,
    )

    print("token_response")
    print(token_response)
    print("\n")

    access_token = token_response.get("access_token")
    if not access_token:
        return f"Could not obtain access token: {token_response.get('error_description')}"

    # Extract ID token claims
    id_token_claims = token_response.get("id_token_claims", {})
    tenant_id = id_token_claims.get("tid")
    if not tenant_id:
        return "Tenant ID not found in the ID token"

    

    # Send an email using Microsoft Graph API
    email_data = {
        "message": {
            "subject": "Test Email",
            "body": {
                "contentType": "Text",
                "content": "Hello, this is a test email sent using Microsoft Graph API."
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": "dorigoandrea98@gmail.com"
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    print("id_token_claims")
    print(id_token_claims)
    print("\n")

    send_mail_response = requests.post(
        'https://graph.microsoft.com/v1.0/me/sendMail',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=email_data
    )

    if send_mail_response.status_code == 202:
        return "Email sent successfully."
    else:
        return f"Failed to send email: {send_mail_response.status_code}, {send_mail_response.text}"

if __name__ == '__main__':
    flask_app.run(debug=True, port=8000)