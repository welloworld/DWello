#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

DW_URL = 'https://www.digitalwhisper.co.il/'

def get_articles_from_page(page):
    soup = BeautifulSoup(page,'html.parser')
    articles_html = soup.find('table').tbody.find_all('tr')[1:]
    return map(lambda x: x.a.text, (filter(lambda y: True if y.a != None and y.a.text != None else False, articles_html)))

def print_articles():
    issue_num = 1
    
    # Delete not-up-to-date file
    data = ''

    while True:
        print(issue_num)
        response = requests.get(DW_URL + 'issue' + str(issue_num))
        if response.status_code != 200:
            break
        articles = get_articles_from_page(response.text)
        print('\n'.join(articles))
        data += str(issue_num) + ':\n' + '\n'.join(articles) + '\n'
        issue_num += 1

    print('No more issues')

    with open('issues.txt', 'w') as f:
        f.write(data.encode('utf-8'))

def main():
    print_articles()


if __name__ == '__main__':
    main()
