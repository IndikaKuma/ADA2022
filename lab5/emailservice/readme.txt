First, you have to do a few configurations at GCP and SendGrid – see below

https://stackoverflow.com/questions/62282170/whats-the-best-way-to-send-an-e-mail-via-python-google-cloud-function/62285013#62285013Links to an external site.

To deploy the function,

gcloud functions deploy send_email --runtime python38 --trigger-http --allow-unauthenticated --set-env-vars SENDGRID_API_KEY=YourSendGridKey

To execute the function,

Send a POST (to the HTTP function URL) with a json body of

{

  "from": "the email address given for sendgrid sender",

  "to": "any",

  "subject": "any",

  "message":"any"

}

If you have not completed setting configurations correctly, you may get an error  

https://stackoverflow.com/questions/59739152/getting-a-strange-error-403-forbidden-for-accessing-an-api-through-pythonLinks to an external site.

An article on combining send email with Pub/sub 

https://dvelp.co.uk/articles/automating-emails-with-google-cloudLinks to an external site.