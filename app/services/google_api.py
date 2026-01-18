from datetime import datetime as dt

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    now_date_time = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetId = response['spreadsheetId']
    return spreadsheetId


async def set_user_permissions(
        spreadsheetId: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetId,
            json=permissions_body,
            fields="id"
        ))


async def update_spreadsheets_value(
        spreadsheetId: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for pr in projects:
        new_row = [str(pr[0]), str(pr[1]), str(pr[2])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetId,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
    return response
