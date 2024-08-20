import msal

# Authority and scope
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

# Create a confidential client application
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# Acquire a token
result = None
result = app.acquire_token_silent(SCOPE, account=None)

if not result:
    result = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" in result:
    access_token = result["access_token"]
else:
    raise Exception("Could not acquire token")

import requests

# Endpoint for sending an email
SEND_MAIL_URL = 'https://graph.microsoft.com/v1.0/me/sendMail'

# Email content
email_message = {
    "message": {
        "subject": "Test Email from Microsoft Graph API",
        "body": {
            "contentType": "Text",
            "content": "This is a test email sent using Microsoft Graph API in Python."
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": "recipient@example.com"
                }
            }
        ]
    }
}

# Send the request
response = requests.post(
    SEND_MAIL_URL,
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    },
    json=email_message
)

if response.status_code == 202:
    print("Email sent successfully!")
else:
    print(f"Failed to send email: {response.status_code}, {response.text}")
