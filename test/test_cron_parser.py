# -*- coding: utf-8 -*-

from unittest import TestCase
import os
from nextrun.cron_parser import CronParser


class TestCronParser(TestCase):

    def test_parse_cron_string(self):
        pass

    def test_parse_cron_file(self):
        pass

    def test_is_valid_path(self):
        cron_file_path = os.path.abspath(u'crontab.txt')
        expected = True
        response = CronParser(None).is_valid_file_path(cron_file_path)

        self.assertEqual(expected, response, response)

        cron_file_path = os.path.abspath(u'fail_file.txt')
        expected = False
        response = CronParser(None).is_valid_file_path(cron_file_path)

        self.assertEqual(expected, response, response)

    def test_get_cron_data(self):
        cron_file_path = os.path.abspath(u'crontab.txt')
        expected = [
            u'30 1 /bin/run_me_daily',
            u'45 * /bin/run_me_hourly',
            u'* * /bin/run_me_every_minute',
            u'* 19 /bin/run_me_sixty_times'
        ]
        response = CronParser(None).get_cron_data(cron_file_path)

        self.assertEqual(expected, response, response)

    def test_parse_cron_data(self):
        cron_data = [
            u'30 1 /bin/run_me_daily',
            u'45 * /bin/run_me_hourly',
            u'* * /bin/run_me_every_minute',
            u'* 19 /bin/run_me_sixty_times'
        ]
        expected = [
            [u'30', u'1', u'/bin/run_me_daily'],
            [u'45', u'*', u'/bin/run_me_hourly'],
            [u'*', u'*', u'/bin/run_me_every_minute'],
            [u'*', u'19', u'/bin/run_me_sixty_times']
        ]
        response = CronParser(None).parse_cron_data(cron_data)

        self.assertEqual(expected, response, response)

    def test_format_cron_data(self):
        pass

    def test_validate_in_range(self):
        pass