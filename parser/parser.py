#!/usr/bin/python3
import pandas as pd
from bs4 import BeautifulSoup


COLUMNS = ['Номер заявки', 'Наименование организации', 'Грантовое направление',
           'Название проекта', 'ИНН', 'ОГРН']

def get_form_of_competition_waves(text):
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
        val, desc = option['value'], option.get_text('', strip=True)

        if desc != '':
            options.append({'id': val, 'text': desc})
    return options

def is_empty_competition_page(text):
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
                      .find_all('li')[-1].a.get_text('', strip=True)

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

def get_grant_description_row(text):
    """    
    Arguments:
        text {str} -- Raw html string
    
    Returns:
        object -- pandas.Series like table row with grant info
    """
    html = BeautifulSoup(text, 'html.parser')

    cols = html.find('section', class_='winner-info')\
               .find_all('li', class_='winner-info__list-item')

    col_cls = 'winner-info__list-item-text'
    number = cols[3].find('span', class_=col_cls).get_text('', strip=True)
    organization = cols[6].find('span', class_=col_cls).get_text('', strip=True)
    grant_way = cols[1].find('span', class_=col_cls).get_text('', strip=True)
    INN = cols[7].find('span', class_=col_cls).get_text('', strip=True)
    OGRN = cols[8].find('span', class_=col_cls).get_text('', strip=True)

    progect = html.find('h2', class_='winner-info__title')\
                  .get_text('', strip=True)

    grant_row = [number, organization, grant_way, progect, INN, OGRN]
    return pd.Series(grant_row, COLUMNS)
