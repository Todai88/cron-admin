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

        valid_current = self.validate_datetime(current_time)

        # If we have been passed a valid current time
        if valid_current[u'minute'] and valid_current[u'hour']:

            if cron_file_path and not cron_string:
                cron_data = (
                    CronParser(self.logger).parse_cron_file(cron_file_path)
                )
            else:
                cron_data = (
                    CronParser(self.logger).parse_cron_string(cron_string)
                )

            for cron in cron_data:
                next_run = self.find_next_run_time(
                    cron[u'hour'], cron[u'minute'],
                    valid_current[u'hour'], valid_current[u'minute']
                )

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

        hour, minute = current_date.split(u':')

        try:
            if (0 <= int(hour) <= 23) and (0 <= int(minute) <= 59):
                valid_minute = int(minute)
                valid_hour = int(hour)
        except ValueError as e:
            logging.error(u'Given current time is invalid %s', e)

        valid_datetime = {u'hour': valid_hour, u'minute': valid_minute}

        return valid_datetime

    def find_next_run_time(
            self, cron_hour, cron_minute, current_hour, current_minute):
        """
        Find the next time / day to run the cron given the current time
        :param cron_minute:
        :param cron_hour:
        :param current_time:
        :return: the next time and next day
        """
        hour_delta = self.find_time_delta(cron_hour, current_hour)
        minute_delta = self.find_time_delta(cron_minute, current_minute)

        if cron_minute == u'*' and cron_hour == u'*':
            # Should run every minute of every hour in a day
            next_run_minute = current_minute
            next_run_hour = current_hour
            next_run_day = u'today'
        elif cron_hour == u'*':
            # Minute is set but should run every hour of a day
            # Cron run time has passed
            if minute_delta < 0:
                # Check for time going into next day (after 23:00)
                if current_hour != 23:
                    next_run_hour = current_hour + 1
                    next_run_day = u'today'
                else:
                    next_run_hour = 0
                    next_run_day = u'tomorrow'
            else:
                next_run_hour = current_hour
                next_run_day = u'today'

            next_run_minute = cron_minute
        elif cron_minute == u'*':
            # Hour is set but should run every minute of that hour
            # Cron run time has passed
            if hour_delta < 0:
                next_run_minute = 0
                next_run_day = u'tomorrow'
            elif hour_delta == 0:
                next_run_minute = current_minute
                next_run_day = u'today'
            else:
                next_run_minute = 0
                next_run_day = u'today'

            next_run_hour = cron_hour
        else:
            # Both Hour and minute are specified and should only run then
            # Cron run time has passed
            if hour_delta < 0:
                next_run_day = u'tomorrow'
            elif hour_delta == 0:
                if minute_delta < 0:
                    next_run_day = u'tomorrow'
                else:
                    next_run_day = u'today'
            else:
                next_run_day = u'today'

            next_run_minute = cron_minute
            next_run_hour = cron_hour

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

        if not cron == u'*' and not current == u'*':
            delta = cron - current

        return delta

    def format_date(self, hour, minute):
        """
        Create a formatted date string
        :param hour:
        :param minute:
        :return:
        """
        hour = unicode(hour)
        minute = unicode(minute) if minute > 9 else u'0' + unicode(minute)

        date = u':'.join([hour, minute])

        return date
