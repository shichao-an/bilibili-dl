# -*- coding: utf-8 -*-
import requests
import sys


class Video(object):
    URL = 'http://www.bilibili.com/m/html5'

    def __init__(self, aid, page=1):
        self.aid = aid
        self.page = page
        self._attrs = None

    def _load(self):
        params = {'aid': self.aid, 'page': self.page}
        r = requests.get(self.URL, params=params)
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
    aid = sys.argv[1]
    page = 1
    if len(sys.argv) > 2:
        page = int(sys.argv[2])
    v = Video(aid, page)
    print v.attrs['src']
    #v.download()


if __name__ == '__main__':
    main()
