#!/usr/bin/python3
import os

from progress.bar import Bar
import pandas as pd

import api
import cli
import parser
import output


if __name__ == '__main__':
    GET_param = cli.select_grants_table_options()

    response = api.request(api.URL, GET_param)
    count_pages = parser.get_total_count_of_pages(response.text)

    Progress = Bar('Собираю ссылки на гранты с web-страниц', max=count_pages)

    links_to_grants = []
    for idpage in range(1, count_pages+1):
        page = api.request(api.URL, {**GET_param, **{'page': idpage}})

        page_links = parser.get_all_links_to_grant_from_page(page.text)
        links_to_grants.extend(page_links)

        Progress.next()
    Progress.finish()

    Progress = Bar('Обрабатываю каждый грант', max=len(links_to_grants))

    grants_table = []
    for link in links_to_grants:
        page = api.request(api.DOMAIN + link).text
        
        grants_table.extend([parser.get_grant_description_row(page)])
        Progress.next()
    grants_table = pd.DataFrame(grants_table)
    Progress.finish()

    writer = output.format_to_excel(grants_table, links_to_grants, 
                                    cli.args.out, cli.args.sheet)
    writer.save()

    print('Данные успешно собраны и сохранены в папке:')
    print(os.path.abspath(cli.args.out))
