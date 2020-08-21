import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SpreadSheet:

    def __init__(self, doc_name, google_sheets_credentials_json):

        self.doc_name = doc_name
        self.google_sheets_credentials_json = google_sheets_credentials_json

        self.sheet_list = self.get_sheet_list()

    def get_sheet_list(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.google_sheets_credentials_json, scope)
        client = gspread.authorize(credentials)
        return client.open(self.doc_name)

    def get_sheet(self, sheet_title):
        for sheet in self.sheet_list:
            if sheet.title == sheet_title:
                return sheet
        raise UserWarning("{} sheet does not exist in {} doc.".format(sheet_title, self.doc_name))

    def sheet_to_list_list(self, sheet_name):
        data_list_list = []
        for data_list in self.get_sheet(sheet_name).get_all_values():
            data_list_list.append([data if data != "" else None for data in data_list])
        return data_list_list

    def update(self):
        self.sheet_list = self.get_sheet_list()
