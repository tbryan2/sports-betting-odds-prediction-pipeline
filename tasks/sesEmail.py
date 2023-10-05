import emails
import pandas as pd

def send_email(body, subject, mail_from, mail_to, **kwargs):
    '''
    Send an email using SES
    '''
    # Pull secrets from XCom
    ti = kwargs['ti']
    secrets = ti.xcom_pull(task_ids='get_secrets')

    host = secrets.get("SES_HOST_ADDRESS")
    user = secrets.get("SES_USER_ID")
    password = secrets.get("SES_PASSWORD")

    # Pull the predictions JSON from XCom
    predictions_json = ti.xcom_pull(task_ids='predict_odds', key='predictions')

    # Convert the JSON string back to a DataFrame
    df_predictions = pd.read_json(predictions_json, orient='split')

    # Convert the DataFrame to an HTML table
    predictions_table = df_predictions.to_html(index=False)

    # Append the predictions table to the original HTML content
    full_html = f"{body}<br><br><strong>Predictions:</strong><br>{predictions_table}"

    # Prepare the email
    message = emails.html(
        html=full_html,
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
