#!/usr/bin/python
# -*- coding: utf-8 -*-

class SheetEditor:

    sheet = ""

    def __init__(self, service, spreadsheet):
        # init the sheet classes using Google SDK or other libraries
        self.service = service
        self.spreadsheet = spreadsheet

    def use_sheet(self, sheet):
        self.sheet = sheet + "!"
        pass

    def __batch(self, requests):
        body = {
            'requests': requests
        }

        return self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet, body=body).execute()

    def rename_sheet(self, sheetId, newName):
        return self.__batch({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheetId,
                    "title": newName,
                },
                "fields": "title",
            }
        })

    def set_row(self, row, start_i, values):
        body = {
            "values": [values]
        }

        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet,
            range=self.sheet + start_i + str(row) + ":" + chr(ord(start_i)+len(values)) + str(row),
            valueInputOption="RAW",
            body=body
        ).execute()

    def set_column(self, column, start_i, values):
        body = {
            "values": list(map(lambda x: [x], values))
        }

        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet,
            range=self.sheet + column + str(start_i) + ":" + column + str(start_i+len(values)),
            valueInputOption="RAW",
            body=body
        ).execute()

    def set_cell(self, cell, value):
        body = {
            "values": [[value]]
        }

        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet,
            range=self.sheet + cell,
            valueInputOption="RAW",
            body=body
        ).execute()

    def get_row(self, row, start_i, count):
        pass

    def get_column(self, row, start_i, count):
        pass

    def get_cell(self, row, column):
        pass

    def get_rows(self, start, end):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet,
                                                range=self.sheet + start + ":" + end).execute()

        values = result.get('values', [])
        return values