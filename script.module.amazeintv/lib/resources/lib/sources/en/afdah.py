# NEEDS FIXING

# -*- coding: utf-8 -*-

'''
    Genesis Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,json,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['afdah.to']
        self.base_link = 'http://afdah.to'
        self.search_link = '/wp-content/themes/afdah/ajax-search.php'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:

            query = urlparse.urljoin(self.base_link, self.search_link)
            post = 'apple=%s&banana=title' % cleantitle.getsearch(title)

            #c, h = self.__get_cookies(query)

            t = cleantitle.get(title)

            r = client.request(query, post=post)
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a',)) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = urlparse.urljoin(self.base_link, re.findall('(?://.+?|)(/.+)', r)[0])
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            print url
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = client.request(url, redirect=True)
            #data = client.parseDOM(r, 'div', attrs={'id': 'cont_\d+'})
            data2 = client.parseDOM(r, 'tr')
            #links = [client.parseDOM(i, 'div', ret='data-id') for i in data if not 'trailer' in i]
            links = [client.parseDOM(i, 'a', ret='href') for i in data2]
            links = [i[0] for i in links if i]
            for url in links:
                try:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if not valid: continue
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources

    def __get_cookies(self, url):
        h = {'User-Agent': client.randomagent()}

        c = client.request(url, headers=h, output='cookie')
        c = client.request(urlparse.urljoin(self.base_link, '/av'), cookie=c, output='cookie', headers=h, referer=url)
        c = client.request(url, cookie=c, headers=h, referer=url, output='cookie')

        return c, h

    def resolve(self, url):
        return directstream.googlepass(url)


