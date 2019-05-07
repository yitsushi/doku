from datetime import datetime
from doku.context import Context
from pathlib import Path
from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import Mock, patch, call

import os
import re


class TestContext(TestCase):
    context = None

    @patch('xmlrpc.client.ServerProxy')
    def setUp(self, mock):
        self.setUpPyfakefs()

        # Prepare config file
        self.fs.create_file(
            os.path.join(Path.home(), '.doku.ini'),
            contents='''[connection]\n'''
                     '''domain = something.to.call\n'''
                     '''username = username\n'''
                     '''password = password\n'''
                     '''[settings]\n'''
                     '''indexpage = root\n'''
                     '''diaryroot = mydiary\n'''
        )

        self.context = Context()

    def test_index_page(self):
        expected = 'root'
        value = self.context.indexpage()
        self.assertEqual(expected, value)

    def test_diary_paths(self):
        self.assertEqual(
            self.context.day_path(2019, 1, 1),
            ':mydiary:2019:01:01'
        )

        self.assertEqual(
            self.context.month_path(2019, 1),
            ':mydiary:2019:01:root'
        )

        self.assertEqual(
            self.context.year_path(2019),
            ':mydiary:2019:root'
        )

        now = datetime.now()
        self.assertEqual(
            self.context.today(),
            ':mydiary:{:04d}:{:02d}:{:02d}'.format(now.year, now.month, now.day)
        )

        self.assertEqual(
            self.context.this_month(),
            ':mydiary:{:04d}:{:02d}:root'.format(now.year, now.month)
        )

        self.assertEqual(
            self.context.this_year(),
            ':mydiary:{:04d}:root'.format(now.year)
        )

    # TODO: refactor fill_month_view to be more testable
    def test_fill_month_view_nothing_to_do(self):
        with patch('doku.client.Client.call') as mockCall:
            mockCall.return_value = 'non-empty body'
            self.context.fill_month_view()

            args = mockCall.call_args[0]
            self.assertEqual(2, len(args))
            self.assertEqual('wiki.getPage', args[0])
            self.assertEqual(self.context.this_month(), args[1])

    def test_fill_month_view_update_required(self):
        with patch('doku.client.Client.call') as mockCall:
            mockCall.return_value = ''
            self.context.fill_month_view()

            args = mockCall.call_args[0]
            self.assertEqual('wiki.putPage', args[0])
            self.assertEqual(self.context.this_month(), args[1])

            body = args[2]
            self.assertRegex(
                body,
                r'====== \w+ ======',
                'h1 title not found in the request')
            self.assertRegex(
                body,
                r'\[\[:mydiary:\d{4}:\d{2}:\d{2}\|\d+\]\]'
            )

    # TODO: refactor fill_year_view to be more testable
    def test_fill_year_view_nothing_to_do(self):
        with patch('doku.client.Client.call') as mockCall:
            mockCall.return_value = 'non-empty body'
            self.context.fill_year_view()

            args = mockCall.call_args[0]
            self.assertEqual(2, len(args))
            self.assertEqual('wiki.getPage', args[0])
            self.assertEqual(self.context.this_year(), args[1])

    def test_fill_year_view_update_required(self):
        with patch('doku.client.Client.call') as mockCall:
            mockCall.return_value = ''
            self.context.fill_year_view()

            args = mockCall.call_args[0]
            self.assertEqual('wiki.putPage', args[0])
            self.assertEqual(self.context.this_year(), args[1])

            body = args[2]
            self.assertRegex(
                body,
                r'====== \d{4} ======',
                'h1 title not found in the request')
            self.assertRegex(
                body,
                r'\* \[\[:mydiary:\d{4}:\d{2}:root\|\w+\]\]'
            )

    # TODO: refactor update_diary_root to be more testable
    def test_update_diary_root_nothing_to_do(self):
        with patch('doku.client.Client.call') as mockCall:
            mockCall.return_value = self.context.year_path(datetime.now().year)
            self.context.update_diary_root()

            args = mockCall.call_args[0]
            self.assertEqual(2, len(args))
            self.assertEqual('wiki.getPage', args[0])
            self.assertEqual(self.context.diary_path(), args[1])

    def test_update_diary_root_nothing_to_do(self):
        with patch(
            'doku.client.Client.call',
            side_effect=['', [{'id': 'mydiary:2001:root'}], '']
        ) as mockCall:
            self.context.update_diary_root()

            mockCall.assert_has_calls(
                [
                    call('wiki.getPage', self.context.diary_path()),
                    call('dokuwiki.getPagelist', ':mydiary', [])
                ],
                any_order=True
            )

            args = mockCall.call_args[0]
            self.assertEqual('wiki.putPage', args[0])
            self.assertEqual(self.context.diary_path(), args[1])

            body = args[2]
            self.assertRegex(
                body,
                r'====== Diary ======',
                'h1 title not found in the request')
            self.assertRegex(
                body,
                r'\* \[\[:mydiary:2001:root\]\]'
            )
