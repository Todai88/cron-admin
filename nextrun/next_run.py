# -*- coding: utf-8 -*-

import logging
import sys
from cron_parser import CronParser


class NextRun(object):

    def __init__(self):
        self.logger = logging.Logger(u'cron-admin')
        self.logger.setLevel(logging.WARNING)

        # create console handler
        console_log = logging.StreamHandler(sys.stdout)
        console_log.setLevel(logging.WARNING)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            u'[%(asctime)s %(name)s %(filename)s:%'
            u'(lineno)d - %(levelname)s]: %(message)s',
            u'%d-%m-%Y %H:%M:%S'
        )
        console_log.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(console_log)

    def find_next_run_times(
            self, current_time, cron_file_path=None, cron_string=None):
        """
        Given cron path / data and current time find next times each cron runs
        :param cron_string:
        :param cron_file_path:
        :param current_time:
        :return:
        """
        next_run_times = []

        # Check that a valid date and time have been passed
        valid_current = self.validate_datetime(current_time)

        # If we have been passed a valid current time
        if valid_current[u'minute'] and valid_current[u'hour']:

            if cron_file_path and not cron_string:
                # Parse data from a given file
                cron_data = (
                    CronParser(self.logger).parse_cron_file(cron_file_path)
                )
            else:
                # Parse data from a given string
                cron_data = (
                    CronParser(self.logger).parse_cron_string(cron_string)
                )

            for cron in cron_data:
                # Find how many hours until the next run time
                hour_delta = self.find_time_delta(
                    cron[u'hour'], valid_current[u'hour']
                )

                # Find how many minutes past the hour until the next run time
                minute_delta = self.find_time_delta(
                    cron[u'minute'], valid_current[u'minute']
                )

                # Calculate the next run time from the deltas
                next_run = self.find_next_run_time(
                    cron[u'hour'], cron[u'minute'],
                    valid_current[u'hour'], valid_current[u'minute'],
                    hour_delta, minute_delta
                )

                # Create a results list entry for each cron
                next_run_times.append([
                    self.format_date(next_run[u'hour'], next_run[u'minute']),
                    next_run[u'day'],
                    cron[u'path']
                ])

        return next_run_times

    def validate_datetime(self, current_date):
        """
        Check the given hour and minute figures are valid
        :param current_date:
        :return:
        """
        valid_minute = None
        valid_hour = None
        MIN_HOUR = 0
        MAX_HOUR = 23
        MIN_MINUTE = 0
        MAX_MINUTE = 59
        TIME_SEPARATOR = u':'

        hour, minute = current_date.split(TIME_SEPARATOR)

        try:
            if ((MIN_HOUR <= int(hour) <= MAX_HOUR) and
                    (MIN_MINUTE <= int(minute) <= MAX_MINUTE)):
                valid_minute = int(minute)
                valid_hour = int(hour)
        except ValueError as e:
            logging.error(u'Given current time is invalid %s', e)

        valid_datetime = {u'hour': valid_hour, u'minute': valid_minute}

        return valid_datetime

    def find_next_run_time(self, cron_hour, cron_minute, current_hour,
                           current_minute, hour_delta, minute_delta):
        """
        Find the next time / day to run the cron given the current time
        :param current_hour:
        :param current_minute:
        :param hour_delta:
        :param minute_delta:
        :param cron_minute:
        :param cron_hour:
        :return: the next time and next day
        """
        NOW = 0
        LAST_HOUR_OF_DAY = 23
        EVERY_MINUTE = u'*'
        EVERY_HOUR = u'*'
        CURRENT_DAY = u'today'
        NEXT_DAY = u'tomorrow'

        if cron_minute == EVERY_MINUTE and cron_hour == EVERY_HOUR:
            # Should run every minute of every hour in a day
            next_run_minute = current_minute
            next_run_hour = current_hour
            next_run_day = CURRENT_DAY

        elif cron_hour == EVERY_HOUR:
            # Minute is set but should run every hour of a day
            # Cron run time has passed
            if minute_delta < NOW:
                # Check for time going into next day (after 23:00)
                if current_hour != LAST_HOUR_OF_DAY:
                    next_run_hour = current_hour + 1
                    next_run_day = CURRENT_DAY
                else:
                    next_run_hour = NOW
                    next_run_day = NEXT_DAY
            else:
                next_run_hour = current_hour
                next_run_day = CURRENT_DAY

            next_run_minute = cron_minute

        elif cron_minute == EVERY_MINUTE:
            # Hour is set but should run every minute of that hour
            # Cron run time has passed
            if hour_delta < NOW:
                next_run_minute = NOW
                next_run_day = NEXT_DAY
            elif hour_delta == NOW:
                next_run_minute = current_minute
                next_run_day = CURRENT_DAY
            else:
                next_run_minute = NOW
                next_run_day = CURRENT_DAY

            next_run_hour = cron_hour

        else:
            # Both Hour and minute are specified and should only run then
            # Cron run time has passed
            if hour_delta < NOW:
                next_run_day = NEXT_DAY
            elif hour_delta == NOW:
                if minute_delta < NOW:
                    next_run_day = NEXT_DAY
                else:
                    next_run_day = CURRENT_DAY
            else:
                next_run_day = CURRENT_DAY

            next_run_minute = cron_minute
            next_run_hour = cron_hour

        # Convenient structure
        next_run_time = {
            u'day': next_run_day,
            u'hour': next_run_hour,
            u'minute': next_run_minute
        }

        return next_run_time

    def find_time_delta(self, cron, current):
        """
        Find difference (time to/from next/previous cron)
        :param cron:
        :param current:
        :return:
        """
        delta = 0
        EVERY_TIME = u'*'

        if not cron == EVERY_TIME and not current == EVERY_TIME:
            delta = cron - current

        return delta

    def format_date(self, hour, minute):
        """
        Create a formatted date string
        :param hour:
        :param minute:
        :return:
        """
        SINGLE_DIGIT = 9
        PADDING_DIGIT = u'0'
        TIME_SEPARATOR = u':'

        hour = unicode(hour)
        minute = (unicode(minute)
                  if minute > SINGLE_DIGIT
                  else PADDING_DIGIT + unicode(minute))

        date = TIME_SEPARATOR.join([hour, minute])

        return date
