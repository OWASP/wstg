import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

if len(sys.argv) < 2:
    print('usage: upload-to-google-drive.py <drive-file-id> <version>')
    print('drive-file-id is the id of the file to update, version is optional')
    sys.exit(1)

XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

file_id = sys.argv[1]
version = '-' + sys.argv[2] if len(sys.argv) > 2 else ''
title = 'WSTG-Checklist{}.xlsx'.format(version)

# credentials.json holds the client id/secret and refresh token, the access
# token is refreshed automatically on the first request. No scopes are passed
# so the refresh uses whatever scopes the token was originally granted.
creds = Credentials.from_authorized_user_file('credentials.json')
drive = build('drive', 'v3', credentials=creds)

# Upload the new content and update the title
media = MediaFileUpload('checklists/checklist.xlsx', mimetype=XLSX_MIME)
drive.files().update(fileId=file_id, body={'name': title}, media_body=media).execute()

# Insert the permission
drive.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
