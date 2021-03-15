import os
from twilio.rest import Client
import config

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure


def send_sms(message_body):
    account_sid = config.ACCOUNT_SID
    auth_token = config.AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=message_body,
                         from_='+12562897127',
                         to='+16087997367'
                     )
    print('Sucessfully sent SMS alert')
    return
