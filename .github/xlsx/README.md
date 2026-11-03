# xlsx

This directory contains github action dependencies for creation of the WSTG XLSX Checklist.

Required pip modules (pinned in `/.github/requirements.txt`, kept current by Dependabot with a 7 day cooldown):

- openpyxl
- google-api-python-client and google-auth (used by `upload-to-google-drive.py` to publish the XLSX checklist to Google Drive)
- google-auth-oauthlib (only needed to run `create-google-drive-cred.py` locally to generate `credentials.json`)
