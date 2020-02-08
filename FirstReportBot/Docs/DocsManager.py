#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'shay@inbar.co.il'

import datetime
from Docs.SheetEditor import SheetEditor

# The ID and range of a sample spreadsheet.
EMAIL_LIST_SPREADSHEET_ID = '1BfOz68K0v7al4uZ21rOBkiW2OseG4_dpyHjL4NjbwNA'
DOCH_LIST_SPREADSHEET_ID = '1MR3L4mfhosWrPu0vm1FtnNDpTHxKXqWFl80xUWq3cRs'

class DocsManager:

    # service - GOOGLE SHEETS API

    def __init__(self):
        self.__load_service()

    def __load_service(self):
        self.emailEditor = SheetEditor(EMAIL_LIST_SPREADSHEET_ID)
        self.emailEditor.use_sheet("~מ'")
        self.dochEditor = SheetEditor(DOCH_LIST_SPREADSHEET_ID)

    """
    Something that updates the how much everyone did
    """

    def get_doch_list(self):
        rows = self.dochEditor.get_rows('A9', 'D56')
        email_dict = self.get_email_dict()
                
        result = []

        for col_index in range(2):
            for row in rows:
                try:
                    name = row[2 * col_index]
                    date = row[2 * col_index + 1]

                    result.append({
                        "name": name,
                        "email": email_dict[name],
                        "date": date
                    })
                except:
                    pass

        return result
        
    def get_email_dict(self):
        rows = self.emailEditor.get_rows('A2', 'J53')
        result = {}

        # get all emails
        for row in rows:
            name = row[0]
            email = row[3]
            result[name] = email

        return result

    
    def __date_format(self, date):
        return datetime.datetime.strftime(date, '%d.%m.%Y')

