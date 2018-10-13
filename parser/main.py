#!/usr/bin/python3
import api
import cli
import parser


if __name__ == '__main__':
    response = api.request(api.URL, cli.SETTING)
    count_pages = parser.get_total_count_of_pages(response.text)

    links_to_grants = []
    for n in range(1, count_pages):
        html_page = api.request(api.URL, {**cli.SETTING, **{'page': n}}).text

        page_links = parser.get_all_links_to_grant_from_page(html_page)
        links_to_grants.extend(page_links)

    grants_table = []
    for link in links_to_grants:
        page = api.request(api.DOMAIN + link).text
        
        grants_table.extend([parser.get_grant_description_row(page)])
    import ipdb; ipdb.set_trace()