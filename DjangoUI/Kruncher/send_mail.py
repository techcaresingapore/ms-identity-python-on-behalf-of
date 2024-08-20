# send_mail.py
import requests
from auth import AzureAuth
from dotenv import load_dotenv
load_dotenv('production.env')
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
TENANT_ID = os.environ.get('TENANT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def send_mail(access_token, recipient_email, subject, content):
    send_mail_url = 'https://graph.microsoft.com/v1.0/me/sendMail'
    
    email_message = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": content
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_email
                    }
                }
            ]
        }
    }

    response = requests.post(
        send_mail_url,
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

# Example usage
if __name__ == "__main__":

    auth = AzureAuth(CLIENT_ID, TENANT_ID, CLIENT_SECRET)
    token = auth.get_token()

    recipient = "dorigoandrea98@gmail.com"
    subject = "Test Email"
    content = "This is a test email sent using Microsoft Graph API in Python."

    send_mail(token, recipient, subject, content)
