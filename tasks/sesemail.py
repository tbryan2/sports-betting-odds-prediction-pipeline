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

if __name__ == "__main__":
    send_email(
        html="<p>Testing email</p>",
        subject="Odds update",
        mail_from="timsfootballs@gmail.com",
        mail_to="timbryan0315@gmail.com",
        host="email-smtp.us-east-1.amazonaws.com",
        user="AKIAQ7KPVUQJ6U6HHWP3",
        password="BMY4iqWSjunC7oFaXkydayDwsTDGf0G0SR5xF7Viv5S6"
    )