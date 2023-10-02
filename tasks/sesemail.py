import emails

def send_email(html, subject, mail_from, mail_to, host, user, password):
    '''
    Send an email using SES
    '''
    # Prepare the email
    message = emails.html(
        html=html,
        subject=subject,
        mail_from=mail_from,
    )

    # Send the email
    r = message.send(
        to=mail_to,
        smtp={
            "host": host,
            "port": 587,
            "timeout": 5,
            "user": user,
            "password": password,
            "tls": True,
        },
    )

    # Check if the email was properly sent
    assert r.status_code == 250