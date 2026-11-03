from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']

# To create the credentials file, client_secrets.json is the OAuth client
# downloaded from the Google Cloud console
flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('credentials.json', 'w') as f:
    f.write(creds.to_json())
