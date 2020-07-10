import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='jamesoneill997@gmail.com',
    to_emails='jamesoneill997@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('lu7yWzT4TMKrnYtMtODCZw.IWy7t8HfR_QBpZySUXrONtJ0ubwdtE5J0JPZnMAeDEg'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)