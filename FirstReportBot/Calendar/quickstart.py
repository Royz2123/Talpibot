from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
DUTY_TITLE = 'תורנות דו"ח 1'
DUTY_LOCATION = 'קומות מחזור מ'
DESCRIPTION = 'תורנות דו"ח 1 מרגשת במיוחד - לך תוודא את המחזור! באהבה - תואר וצוות סייברלוז'
TIME_ZONE = 'Asia/Jerusalem'

class CalManager:

    def __init__(self):
        store = file.Storage('Calendar\\token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('Calendar\\credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))

    def __new_calendar(self):
        calendar = {'summary': 'CyberLooz'}
        created_calendar = self.service.calendars().insert(body = calendar).execute()
        print(created_calendar)
        return created_calendar["id"]

    def __new_event(self, calender, attendee, date): #timeBool = morning(0) or evening(1)
        final_attendees = []
        date = '20' + date
        time = 'T07:00:00'
        time2 = 'T07:30:00'
        
        formatted_attendee = {
            "displayName" : attendee["name"], 
            "email" : attendee["email"]
        }
        
        print(date, ":\t", formatted_attendee["displayName"])
       
        event = {
            'summary': DUTY_TITLE,
            'location': DUTY_LOCATION,
            'description': DESCRIPTION,
            'start': {
                'dateTime': date + time, #'2015-05-28T09:00:00-07:00',
                'timeZone': TIME_ZONE,
            },
            'end': {
                'dateTime': date + time2,
                'timeZone': TIME_ZONE,
            },
            'attendees' : [formatted_attendee],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        event = self.service.events().insert(calendarId=calender, body=event).execute()

    def __search_calendar(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if(calendar_list_entry['summary'] == 'סייבר לוז בדיקה'):
                    return calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return "0"

    def send_events(self, duty_list):
        cal_id = self.__search_calendar()
        if(cal_id == "0"):
            cal_id = self.__new_calendar()
            
        for index, duty in enumerate(duty_list):
            date = self.create_date(duty["date"]).strftime('%y-%m-%d')
            self.__new_event(cal_id, duty, date)
            
    def create_date(self, str_date):
        return datetime.datetime.strptime(str_date, "%d/%m/%Y").date()


