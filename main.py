from __future__ import unicode_literals

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import requests
import pprint

from strex.parse import parse

sites = [{
    'name': 'Reuters home page',
    'url': 'http://www.reuters.com/',
    'options': {
        'parser': 'html',
        'list_type': 'xpath',
        'remove_whitespace': True,
    },
    'structure': {
        '_list': '//a[contains(@href,"/article/")]',
        '_item': {
            'title': 'text()',
            'date': 'substring(@href,10,10)',
            'url': '@href'
        }
    }
},
{
    'name': 'The Verge RSS feed', 
    'url': 'http://www.theverge.com/rss/frontpage', 
    'options': {
        'parser': 'xml',
        'list_type': 'xpath',
        'namespaces': {
            'a': 'http://www.w3.org/2005/Atom'
        },
    },
    'structure': {
        '_list': '//a:entry',
        '_item': {
            'title': 'a:title/text()',
            'date': 'a:published/text()',
            'url': 'a:link[@rel="alternate"]/@href'
        }
    } 
}]

def main():
    for site in sites:
        content = requests.get(site['url'])
        res = parse(content.text, site['structure'], site['options'])
        print(site['name'] + ' (' + site['url'] + ')')
        pprint.pprint(res)
        print('')

if __name__ == '__main__':
    main()
