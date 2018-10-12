#!/usr/bin/python3
import api

if __name__ == '__main__':
    table_settings = {
        'OnlyWinners': 'true',
        'CompetitionId': 3,
    }

    response = api.request(api.URL, table_settings)
    html = response.text
    print(html)
