#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'shay@inbar.co.il'

import datetime
from CleaningBot.Docs.SheetEditor import SheetEditor

# The ID and range of a sample spreadsheet.
DUTY_SPREADSHEET_ID = '1eP3P_90DzUbl8VVcNahi9ZJ2NMZ9FDvoP5ygcaqmpqE'

LIST_SPREADSHEET_ID = '1BfOz68K0v7al4uZ21rOBkiW2OseG4_dpyHjL4NjbwNA'

class DocsManager:

    # service - GOOGLE SHEETS API

    def __init__(self, week, sunday):
        self.__load_service()
        self.week = week
        self.sunday = sunday

    def __load_service(self):
        self.listEditor = SheetEditor(LIST_SPREADSHEET_ID)
        self.listEditor.use_sheet("~מ'")

        self.dutyEditor = SheetEditor(DUTY_SPREADSHEET_ID)

    def set_list(self, rows):
        # self.listEditor.set_column('A', 2, map(lambda x: x["name"], rows))
        self.listEditor.set_column('B', 2, list(map(lambda x: x["only_evening"], rows)))
        self.listEditor.set_column('C', 2, list(map(lambda x: x["cleans"], rows)))
        # self.listEditor.set_column('D', 2, map(lambda x: x["email"], rows))

    def get_swappers(self):
        """"
        return [(swappers_pair1 (tuple), mode), (swappers_pair2 (tuple), mode) ... ]
        """

    def get_scheule(self):
        """"
        return the same format I send to you marg
        """

    def clear_swappers(self):
        """
        void, just delete the swappers form
        """

    """
    Something that updates the how much everyone did
    """

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

            #  Empty the cells, if some day has no schedule
            morning = [''] * 4
            evening = [''] * 4

            self.dutyEditor.set_column(column, 4, morning)
            self.dutyEditor.set_column(column, 9, evening)

            #  Set the names according to manager
            morning = list(map(lambda x: x["name"], duty[0][i]))
            evening = list(map(lambda x: x["name"], duty[1][i]))

            self.dutyEditor.set_column(column, 4, morning)
            self.dutyEditor.set_column(column, 9, evening)

            #  Move to next day
            column = chr(ord(column)+1)
            day = day + datetime.timedelta(days=1)

        self.dutyEditor.rename_sheet(181407074, 'תורנויות שבוע '+ str(self.week))

    def __date_format(self, date):
        return datetime.datetime.strftime(date, '%d.%m.%Y')

"""
docs = DocsManager(2, datetime.date.today())

lista = docs.get_list()

new_schedule = [[], []]

i = 0

for sched in range(0, 2):
    for day in range(0, 5):
        one = []
        if day == 0 and sched == 0:
            new_schedule[sched].append(one)
            continue
        one.append(lista[i])
        i += 1
        one.append(lista[i])
        i += 1
        one.append(lista[i])
        i += 1
        one.append(lista[i])
        i += 1

        new_schedule[sched].append(one)

docs.set_schedule(new_schedule)
"""