# -*- coding: utf-8 -*-
import re
import requests
import sys


class Extractor(object):
    _VALID_URL = r'http://www\.bilibili\.(?:tv|com)/video/av(?P<id>[0-9]+)/'
    _INDEX = r'(index_(?P<page>[0-9]+).html)?'
    VALID_URL = _VALID_URL + _INDEX

    def __init__(self, url):
        self.url = url
        self.aid = None
        self.page = 1

    def _extract(self):
        m = re.match(self.VALID_URL, self.url)
        self.aid = m.group('id')
        page = m.group('page')
        if page is not None:
            self.page = page

    @property
    def video(self):
        if self.aid is None:
            self._extract()
        return {'aid': self.aid, 'page': self.page}


class Video(object):
    HTML5_URL = 'http://www.bilibili.com/m/html5'

    def __init__(self, aid, page=1):
        self.aid = aid
        self.page = page
        self._attrs = None

    def _load(self):
        params = {'aid': self.aid, 'page': self.page}
        r = requests.get(self.HTML5_URL, params=params)
        if r.ok:
            self._attrs = r.json()
        else:
            r.raise_for_status()

    @property
    def attrs(self):
        if self._attrs is None:
            self._load()
        return self._attrs

    def download(self):
        if self._attrs is None:
            self._load()
        path = self.aid + '.mp4'
        if self._attrs:
            download(path, self._attrs['src'])


def download(path, url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)


def main():
    url = sys.argv[1]
    e = Extractor(url)
    v = Video(e.video['aid'], e.video['page'])
    print v.attrs['src']
    #v.download()


if __name__ == '__main__':
    main()
