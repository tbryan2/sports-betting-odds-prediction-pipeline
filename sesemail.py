import emails
from keys import SES_HOST_ADDRESS, SES_USER_ID, SES_PASSWORD, port


# Prepare the email
message = emails.html(
    html="<h1>Testing Something</h1><strong>Love you!</strong>",
    subject="Hi Sydney",
    mail_from="timsfootballs@gmail.com",
)

# Send the email
r = message.send(
    to="sydney.fortin2@gmail.com",
    smtp={
        "host": SES_HOST_ADDRESS,
        "port": 587,
        "timeout": 5,
        "user": SES_USER_ID,
        "password": SES_PASSWORD,
        "tls": True,
    },
)

# Check if the email was properly sent
assert r.status_code == 250
