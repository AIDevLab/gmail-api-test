import streamlit as st
from google.oauth2.credentials import Credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

# Set the scope and credentials file location
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
CLIENT_SECRET_FILE = "gmailAPI/creds.json"
APPLICATION_NAME = 'Gmail API Python Send Email'

# Define the credentials flow
def get_credentials():
    credential_path = os.path.join('./gmailAPI', 'gmail-python-send-email.json')
    credentials = None
    if os.path.exists(credential_path):
        with open(credential_path, 'r') as f:
            credentials = Credentials.from_authorized_user_info(info=json.load(f))
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(credential_path, 'w') as f:
            f.write(credentials.to_json())
    return credentials

def send_draft(content,recepient,subject):
    # Authenticate the user and authorize the credentials
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Get the authorized user's email address
    user_profile = service.users().getProfile(userId='me').execute()
    user_email = user_profile['emailAddress']

    print("---------")
    print(user_email)
    print("---------")

    # Define the email message
    message = MIMEMultipart()
    message['to'] = user_email
    message['subject'] = subject
    body = content
    message.attach(MIMEText(body, 'plain'))

    # Create the email draft
    message = {'message': {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}}
    draft = service.users().drafts().create(userId='me', body=message).execute()

st.title('Meet Recap Generator')

# Check if the user has authorized the Gmail API
if 'creds' not in st.session_state:
    st.write("Please authenticate with your Google account to continue")
    st.write("Click the button below to proceed")
    if st.button("Authenticate"):
        creds = st.experimental_get_credentials()
        if creds:
            st.session_state.creds = creds
            st.write("Authentication successful!")
        else:
            st.write("Authentication failed. Please try again.")
else:
    # Send the email draft
    content = "This is a test email."
    recipient = ""
    subject = "Test Email"
    send_draft(content, recipient, subject)
    st.write("Email sent!")
