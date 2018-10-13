#!/usr/bin/python3
import api
import cli
import parser


if __name__ == '__main__':
    response = api.request(api.URL, cli.SETTING)
    print(parser.get_total_count_of_pages(response.text))