#!/usr/bin/python3
import api
import cli
import parser


if __name__ == '__main__':
    response = api.request(api.URL, cli.SETTING)
    count_pages = parser.get_total_count_of_pages(response.text)

    grant_links = []
    for n in range(1, count_pages):
        html_page = api.request(api.URL, {**cli.SETTING, **{'page': n}}).text

        page_links = parser.get_all_links_to_grant_from_page(html_page)
        grant_links.extend(page_links)