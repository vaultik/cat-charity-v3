JWT_TOKEN_LIFETIME_SECONDS = 3600
MIN_LEN_PASSWORD = 3

GOOGLE_AUTH_URL = 'https://www.googleapis.com/auth/'

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY_TEMPLATE = {
    'properties': {
        'title': 'Отчёт на {now_date_time}',
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': 100,
                'columnCount': 11
            }
        }
    }]
}
