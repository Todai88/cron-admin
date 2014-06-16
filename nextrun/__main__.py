# -*- coding: utf-8 -*-

import argparse
from next_run import NextRun


if __name__ == u'__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description=u'Cron Admin tool.'
    )

    parser.add_argument(
        u'-t',
        dest=u'current_time',
        default=u'16:10',
        help=u'The time from which to check'
    )

    parser.add_argument(
        u'-p',
        dest=u'cron_path',
        default=None,
        help=u'Full path to the cron file to check'
    )

    parser.add_argument(
        u'-s',
        dest=u'cron_string',
        default=None,
        help=u'A newline separated string of cron data'
    )

    args = parser.parse_args()

    # Call the class controller to run the script
    next_run_times = NextRun().find_next_run_times(
        args.current_time, args.cron_path, args.cron_string
    )

    # Output results to console
    for cron_data in next_run_times:
        print u' '.join(cron_data)