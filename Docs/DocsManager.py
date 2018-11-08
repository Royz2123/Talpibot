#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'shay@inbar.co.il'

import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from Docs.SheetEditor import SheetEditor

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
DUTY_SPREADSHEET_ID = '1eP3P_90DzUbl8VVcNahi9ZJ2NMZ9FDvoP5ygcaqmpqE'
DUTY_RANGE_NAME = 'תורנויות שבוע 1' + '!A1:G'

LIST_SPREADSHEET_ID = '1BfOz68K0v7al4uZ21rOBkiW2OseG4_dpyHjL4NjbwNA'
LIST_RANGE_NAME = "~מ'" +'!A1:G46'

class DocsManager:

    # service - GOOGLE SHEETS API

    def __init__(self, week, sunday):
        self.__load_service()
        self.week = week
        self.sunday = sunday

    def __load_service(self):
        store = file.Storage('Docs\\token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('Docs\\credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)

        self.service = build('sheets', 'v4', http=creds.authorize(Http()))

        self.listEditor = SheetEditor(self.service, LIST_SPREADSHEET_ID)
        self.listEditor.use_sheet("~מ'")

        self.dutyEditor = SheetEditor(self.service, DUTY_SPREADSHEET_ID)

    def set_list(self, rows):
        # self.listEditor.set_column('A', 2, map(lambda x: x["name"], rows))
        self.listEditor.set_column('B', 2, list(map(lambda x: x["only_evening"], rows)))
        self.listEditor.set_column('C', 2, list(map(lambda x: x["cleans"], rows)))
        # self.listEditor.set_column('D', 2, map(lambda x: x["email"], rows))

    def get_list(self):
        rows = self.listEditor.get_rows('A2', 'J53')
        result = []

        for row in rows:
            name = row[0]
            only_evening = row[1]
            cleans = row[2]
            email = row[3]

            result.append({
                "name": name,
                "email": email,
                "cleans": cleans,
                "only_evening": only_evening
            })

        return result

    def set_schedule(self, duty):
        # update dates
        day = self.sunday
        column = 'B'
        for i in range(0, 5):
            self.dutyEditor.set_cell(column + '2', self.__date_format(day))

            morning = list(map(lambda x: x["name"], duty[0][i]))
            evening = list(map(lambda x: x["name"], duty[1][i]))

            self.dutyEditor.set_column(column, 4, morning)
            self.dutyEditor.set_column(column, 9, evening)

            column = chr(ord(column)+1)
            day = day + datetime.timedelta(days=1)

        self.dutyEditor.rename_sheet(181407074, 'תורנויות שבוע '+ str(self.week))

    def __date_format(self, date):
        return datetime.datetime.strftime(date, '%d.%m.%Y')

docs = DocsManager(2, datetime.date.today())

lista = docs.get_list()

docs.set_list(lista)