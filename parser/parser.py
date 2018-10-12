#!/usr/bin/python3
from bs4 import BeautifulSoup

def get_waves_of_competition(text):
    """
    Arguments:
        text {str} -- Raw html string
    
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

def is_empty_page(text):
    """
    Arguments:
        text {str} -- Raw html string
    
    Returns:
        bool
    """
    html = BeautifulSoup(text, 'html.parser')
    
    if html.find('h2', class_='application-not-found') is None:
        return False
    return True