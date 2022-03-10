from python_http_client import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(request):
    request_json = request.get_json(silent=True)
    message = Mail(
        to_emails=request_json['to'],
        from_email=request_json['from'],
        subject=request_json['subject'],
        html_content=request_json['message']
    )

    sg = SendGridAPIClient()
    try:
        response = sg.send(message)
        return f"An email was sent to {request_json['to']}"

    except HTTPError as e:
        return e.reason
