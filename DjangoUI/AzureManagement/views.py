from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Helpers.msal_helper import AuthenticationHelper
from Helpers.requests_helper import RequestsHelper
import os, json
import requests

def sendEmail(userId,toUserEmail,subject,body,access_token):
    endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/sendMail'
    fromUserEmail = 'info@techcare.info'
    email_msg = {'Message': {'Subject': subject,
                            'Body': {'ContentType': 'Text', 'Content': body},
                            'ToRecipients': [{'EmailAddress': {'Address': toUserEmail}}],
                            'sender': {'EmailAddress': {'address': fromUserEmail, 'name':'TechCare Team'}},
                            },
                'SaveToSentItems': 'true'}
    
    r = requests.post(endpoint,headers={'Authorization': 'Bearer ' + access_token},json=email_msg)
    if r.ok:
        print(f'Sent email successfully to {toUserEmail}')
    else:
        print(r.json())

class SubscriptionsView(View):

    def get(self, request):

        if request.session.get("user_name", None) is None:
            return HttpResponseRedirect(reverse("login"))

        accounts = AuthenticationHelper.get_confidential_client().get_accounts(username=request.session["user_name"])

        if len(accounts) == 0:
            return HttpResponseRedirect(reverse("login"))

        token_response = AuthenticationHelper.get_confidential_client().acquire_token_silent(
            scopes=[os.environ.get("API_SCOPE")],
            account=accounts[0],
            authority=os.environ.get("AUTHORITY")
        )

        if "error" in token_response:
            return HttpResponse("An Error Occurred:" + token_response.get("error") + " " +  token_response.get("error_description"), status=404)

        #rg_response = RequestsHelper.get_backend_api_session(token_response).get(os.environ.get("FLASK_BACKEND_URL")).json()
        #rg_response_converted = json.dumps(rg_response)
        userId = accounts[0]["local_account_id"]

        sendEmail(userId,"dorigoandrea98@gmail.com","Test 1","Python fa schifo",token_response['access_token'])

        return HttpResponse(f"Toekn {token_response}")
    
    
            