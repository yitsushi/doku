import calendar
import os
import re
from datetime import datetime
from functools import partial

from doku.client import Client
from doku.config_manager import ConfigManager


class Context:
    client: Client
    config: ConfigManager
    editor: str
    today: str
    diary_prefix = 'diary:'
    __today = None

    def __init__(self):
        self.editor = os.environ.get('EDITOR', 'vim')
        self.config = ConfigManager()
        self.__new_client()
        self.__today = datetime.now()

    def __new_client(self):
        info = self.config['connection']
        self.client = Client(
            info['domain'],
            info['username'],
            info['password'],
            ssl=info.get('ssl', True),
            basepath=info.get('path', '/')
        )

    def indexpage(self):
        return self.config.get('settings', 'indexpage', 'index')

    def day_path(self, year, month, day):
        return ':{}:{:04d}:{:02d}:{:02d}'.format(
            self.diary_prefix, year, month, day)

    def month_path(self, year, month):
        return ':{}:{:04d}:{:02d}:{}'.format(
            self.diary_prefix, year, month, self.indexpage())

    def year_path(self, year):
        return ':{}:{:04d}:{}'.format(
            self.diary_prefix, year, self.indexpage())

    def diary_path(self):
        return ':{}:{}'.format(self.diary_prefix, self.indexpage())

    def today(self):
        _t = self.__today
        return self.day_path(_t.year, _t.month, _t.day)

    def this_month(self):
        _t = self.__today
        return self.month_path(_t.year, _t.month)

    def this_year(self):
        _t = self.__today
        return self.year_path(_t.year)

    def fill_month_view(self):
        content = self.client.call('wiki.getPage', self.this_month())
        if content != '':
            return

        print('Generate month view...')
        _t = self.__today
        days = calendar.monthrange(_t.year, _t.month + 1)[1]
        lines = []
        for d in range(1, days + 1, 7):
            link = partial(self.day_path, year=_t.year, month=_t.month)
            current = ['[[{}|{}]]'.format(link(day=d+i), d+i)
                       for i in range(0, 7) if d + i <= days]
            lines.append('|{}|'.format('|'.join(current)))

        lines.insert(0, _t.strftime('====== %B ======%n'))

        self.client.call(
            'wiki.putPage',
            self.this_month(),
            '\n'.join(lines),
            {'sum': 'Auto-generated with doku command line tool'}
        )

    def fill_year_view(self):
        content = self.client.call('wiki.getPage', self.this_year())
        if content != '':
            return

        print('Generate year view...')
        link = lambda x: '  * [[{}|{}]]'.format(
                    self.month_path(self.__today.year, x),
                    calendar.month_name[x]
               )
        lines = [link(m+1) for m in range(0, 12)]

        lines.insert(0, self.__today.strftime('====== %Y ======%n'))

        self.client.call(
            'wiki.putPage',
            self.this_year(),
            '\n'.join(lines),
            {'sum': 'Auto-generated with doku command line tool'}
        )

    def update_diary_root(self):
        content = self.client.call('wiki.getPage', self.diary_path())
        if self.year_path(self.__today.year) in content:
            return

        print('Regenerate diary root...')
        pages = self.client.call('dokuwiki.getPagelist', ':diary', [])
        lines = []
        for page in [p for p in pages
                     if re.match(
                         r'^diary:\d{4}:%s$' %
                         (self.indexpage()),
                         p['id'])
                     ]:
        lines.append('  * [[:{}]]'.format(page['id']))

        lines.insert(0, '====== Diary ======\n')

        self.client.call(
            'wiki.putPage',
            self.diary_path(),
            '\n'.join(lines),
            {'sum': 'Auto-generated with doku command line tool'}
        )

