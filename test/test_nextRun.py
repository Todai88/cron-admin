# -*- coding: utf-8 -*-

from unittest import TestCase
from nextrun.next_run import NextRun


class TestNextRun(TestCase):

    def test_find_next_run_times(self):

        expected = (
            ()
        )

        self.fail()

    def test_is_valid_datetime(self):
        # Normal case
        current_time = u'12:20'
        expected = True

        response = NextRun().is_valid_datetime(current_time)

        self.assertEqual(expected, response, response)

        # Fail on invalid hour
        current_time = u'24:20'
        expected = False

        response = NextRun().is_valid_datetime(current_time)

        self.assertEqual(expected, response, response)

        # Fail on invalid minute
        current_time = u'23:60'
        expected = False

        response = NextRun().is_valid_datetime(current_time)

        self.assertEqual(expected, response, response)
