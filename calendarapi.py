from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarAPI():
    def __init__(self, scope):
        self.scope = scope
        self.service = self.createCalendarService()

    def createCalendarService(self):
        print('Creating Google calendar API service')
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        return service

    def batchInsertEvents(self, args):

        def printCreatedEvent(request_id, response, exception):
            if exception is not none:
                print('Created Event: ' + createdEvent)
                pass
            else: 
                print('Event not created')
                pass

        print('Inserting all events')

        batch = self.service.new_batch_http_request()

        for event in args:
            batch.add(self.service.events().insert(calendarId='primary', body=event), callback=printCreatedEvent)

        batch.execute()