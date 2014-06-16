# -*- coding: utf-8 -*-

from unittest import TestCase
from nextrun.next_run import NextRun


class TestNextRun(TestCase):

    def test_find_next_run_times(self):
        expected = [
            [u'1:30', u'tomorrow', u'/bin/run_me_daily'],
            [u'16:45', u'today', u'/bin/run_me_hourly'],
            [u'16:10', u'today', u'/bin/run_me_every_minute'],
            [u'19:00', u'today', u'/bin/run_me_sixty_times']
        ]
        response = NextRun().find_next_run_times(u'16:10', u'crontab.txt')
        self.assertEqual(expected, response, response)

    def test_validate_datetime(self):
        # Normal case
        current_time = u'12:20'
        expected = {u'hour': 12, u'minute': 20}

        response = NextRun().validate_datetime(current_time)
        self.assertEqual(expected, response, response)

        # Fail on invalid hour
        current_time = u'24:20'
        expected = {u'hour': None, u'minute': None}

        response = NextRun().validate_datetime(current_time)
        self.assertEqual(expected, response, response)

        # Fail on invalid minute
        current_time = u'23:60'
        expected = {u'hour': None, u'minute': None}

        response = NextRun().validate_datetime(current_time)
        self.assertEqual(expected, response, response)

    def test_find_next_run_time(self):
        # Case 1: 30 1 /bin/run_me_daily -> 1:30 tomorrow
        response = NextRun().find_next_run_time(1, 30, 16, 10)
        self.assertEqual(1, response[u'hour'], response[u'hour'])
        self.assertEqual(30, response[u'minute'], response[u'minute'])
        self.assertEqual(u'tomorrow', response[u'day'], response[u'day'])

        # Case 2: 45 * /bin/run_me_hourly -> 16:45 today
        response = NextRun().find_next_run_time(u'*', 45, 16, 10)
        self.assertEqual(16, response[u'hour'], response[u'hour'])
        self.assertEqual(45, response[u'minute'], response[u'minute'])
        self.assertEqual(u'today', response[u'day'], response[u'day'])

        # Case 3: * * /bin/run_me_every_minute -> 16:10 today
        response = NextRun().find_next_run_time(u'*', u'*', 16, 10)
        self.assertEqual(16, response[u'hour'], response[u'hour'])
        self.assertEqual(10, response[u'minute'], response[u'minute'])
        self.assertEqual(u'today', response[u'day'], response[u'day'])

        # Case 4: * 19 /bin/run_me_sixty_times -> 19:00 today
        response = NextRun().find_next_run_time(19, u'*', 16, 10)
        self.assertEqual(19, response[u'hour'], response[u'hour'])
        self.assertEqual(0, response[u'minute'], response[u'minute'])
        self.assertEqual(u'today', response[u'day'], response[u'day'])

    def test_find_time_delta(self):
        pass

    def test_format_date(self):
        pass
