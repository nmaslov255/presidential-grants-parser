#!/usr/bin/python3
from bs4 import BeautifulSoup

def get_waves_of_competition(text):
    """
    Arguments:
        text {str} -- Row html string
    
    Returns:
        list -- list with competitionId and description
    """
    html = BeautifulSoup(text, 'html.parser')
    competition = html.find(id='CompetitionId')
    
    options = []
    for option in competition.find_all('option'):
        val, desc = option['value'], option.string

        if isinstance(desc, str):
            options.append({'id': val, 'text': desc})
    return options
