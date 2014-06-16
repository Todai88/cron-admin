# -*- coding: utf-8 -*-

import os


class CronParser(object):

    def __init__(self, logger=None):
        self.logger = logger

    def parse_cron_string(self, cron_string):
        """
        Parse a cron data string
        :param cron_string:
        :return:
        """
        formatted_cron_data = []

        if cron_string:
            cron_data = cron_string.split(u'\\n')
            parsed_cron_data = self.parse_cron_data(cron_data)
            formatted_cron_data = self.format_cron_data(parsed_cron_data)

        return formatted_cron_data

    def parse_cron_file(self, cron_file_path):
        """
        Given a cron file return its contents in a list of dict
        :param cron_file_path:
        :return: formatted_cron_data dict
        """
        formatted_cron_data = []

        if self.is_valid_file_path(cron_file_path):

            cron_data = self.get_cron_data(cron_file_path)
            parsed_cron_data = self.parse_cron_data(cron_data)
            formatted_cron_data = self.format_cron_data(parsed_cron_data)

        return formatted_cron_data

    def is_valid_file_path(self, cron_file_path):
        """
        Check if the cron file exists / path is valid
        :param cron_file_path:
        :return:
        """
        is_valid = False

        if os.path.isfile(cron_file_path):
            is_valid = True

        return is_valid

    def get_cron_data(self, cron_file_path):
        """
        Read in a cron file
        :param cron_file_path:
        :return: list of cron config strings
        """
        cron_data = []

        try:
            with open(cron_file_path, u'r') as cron_file:
                for cron_config in cron_file:
                    if cron_config and len(cron_config) > 5:
                        cron_data.append(cron_config.strip(u'\n'))
        except IOError as e:
            if self.logger:
                self.logger.error(u'Could not read cron file %s', e)

        return cron_data

    def parse_cron_data(self, cron_data):
        """
        Parse and separate config string into constituent parts
        :param cron_data:
        :return list of lists of cron data
        """
        parsed_cron_data = []

        for cron_config in cron_data:
            try:
                cron_parts = cron_config.strip().split()
                parsed_cron_data.append(cron_parts)
            except ValueError as e:
                if self.logger:
                    self.logger.warning(u'Malformed cron config %s', e)

        return parsed_cron_data

    def format_cron_data(self, cron_data):
        """
        Put data into a desired list of dicts format
        :param cron_data:
        :return: structured list of dicts
        """
        formatted_cron_data = []

        for data in cron_data:
            try:
                format_data = {
                    u'minute': self.validate_in_range(data[0], 0, 59),
                    u'hour': self.validate_in_range(data[1], 0, 23),
                    u'path': data[2]
                }
                formatted_cron_data.append(format_data)
            except IndexError as e:
                if self.logger:
                    self.logger.error(u'Malformed cron entry %s', e)

        return formatted_cron_data

    def validate_in_range(self, value, low, high):
        """
        Check a value is in range or return None
        :param number:
        :param low:
        :param high:
        :return:
        """
        validated = None

        try:
            if low <= int(value) <= high:
                validated = int(value)
        except ValueError:
            # Is usually '*'
            if value == u'*':
                validated = u'*'

        return validated