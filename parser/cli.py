#!/usr/bin/python3
import parser
import api

SETTING = {
    'OnlyWinners': 'true',
}

def competition_is_exist(choice, options):
    options = {option['id']:True for option in options}
    return options.get(choice, False)

def get_options_with_content(options):
    for n, option in enumerate(options):
        setting = SETTING.copy()
        setting['CompetitionId'] = option['id']

        response = api.request(api.URL, setting)
        if parser.is_empty_page(response.text):
            del options[n]
    return options

response = api.request(api.URL, SETTING)
options = parser.get_waves_of_competition(response.text)
options = get_options_with_content(options)

print('Выберите конкурс или напишите quit для выхода')
for option in options[::-1]:
    print('%s) %s' % (option['id'], option['text']))

while True:
    choice = input('Введите №:')
    if competition_is_exist(choice, options):
        SETTING['CompetitionId'] = choice
        break
    if choice == 'quit':
        break

