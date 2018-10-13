#!/usr/bin/python3
from bs4 import BeautifulSoup


COLUMNS = ['Номер заявки', 'Наименование организации', 'Грантовое направление',
           'Название проекта', 'ИНН', 'ОГРН']


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

def get_total_count_of_pages(text):
    """
    Arguments:
        text {str} -- Raw html string
    
    Returns:
        int -- total count of pages
    """
    html = BeautifulSoup(text, 'html.parser')

    count_pages = html.find('ul', class_='pagination')\
                      .find_all('li')[-1].a.string

    return int(count_pages)

def get_all_links_to_grant_from_page(text):
    """
    Arguments:
        text {str} -- Raw html string
    
    Returns:
        list -- list with links to full grant description
    """
    html = BeautifulSoup(text, 'html.parser')

    html_table_rows = html.find('section', class_='project-present')\
               .find_all('div', class_='table__row')[1:]

    links = []
    for row in html_table_rows:
        link = row.find_all('div', class_='table__cell')[0].a['href']
        links.append(link)
    return links
    