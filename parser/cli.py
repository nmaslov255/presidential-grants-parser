#!/usr/bin/python3
import sys
import argparse

import parser
import api

argparser = argparse.ArgumentParser(
    description='Grants parser')

argparser.add_argument('out', type=str, default='Grants.xlsx',
    help='filename for save results (in xlsx)')

argparser.add_argument('-s', '--sheet', type=str, default='Grants',
    help='Sheet name in Exel')

args = argparser.parse_args()


def select_grants_table_options(only_winners=True):
    """CLI interface for choice competition waves
    
    Arguments:
        only_winners {bool} -- only grant winners?
    
    Returns:
        dict|bool -- return GET params for parser or False if you quit from program
    """
    GET_params = {'OnlyWinners': 'true'} if only_winners else {}
    response = api.request(api.URL, GET_params)

    # take select options from html web page
    competitions = parser.get_form_of_competition_waves(response.text)
    competitions = get_no_empty_competition_waves(competitions, GET_params)

    print('Выберите конкурс или напишите quit для выхода')
    for competition in competitions[::-1]:
        print('%s) %s' % (competition['id'], competition['text']))

    while True:
        competitionid = input('Введите №:')
        if competitionid_is_exist(competitionid, competitions):
            GET_params['CompetitionId'] = competitionid; break
        if competitionid == 'quit':
            sys.exit(0)
    return GET_params

def get_no_empty_competition_waves(competitions, GET_params):
    """Check html table in grants webpage

    Arguments:
        competitions {dict} -- list with competition select options
        GET_params {dict} -- Dict with GET params for grants html table
    
    Returns:
        list -- list with no empty competition select options
    """
    for idx, competition in enumerate(competitions):
        GET_params['CompetitionId'] = competition['id']

        page = api.request(api.URL, GET_params).text
        if parser.is_empty_competition_page(page):
            del competitions[idx]
    return competitions

def competitionid_is_exist(choice, competitions):
    options = {option['id']:True for option in competitions}
    return options.get(choice, False)
