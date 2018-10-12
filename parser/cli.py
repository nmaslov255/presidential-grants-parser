#!/usr/bin/python3
import parser
import api

SETTING = {
    'OnlyWinners': 'true',
    'CompetitionId': 3,
}

response = api.request(api.URL, SETTING)
options = parser.get_waves_of_competition(response.text)

print('Доступные конкурсы:')
for option in options[::-1]:
    print('%s) %s' % (option['id'], option['text']))
SETTING['CompetitionId'] = input('Введите №:')
