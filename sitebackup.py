#!/usr/bin/env python

"""Personal backup script"""

import argparse

from lib import backup

__author__ = "Arseny Zinchenko"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Arseny Zinchenko"
__status__ = "Development"


def getopts():

    """Use '-c' to specify non-default configuration file."""

    parser = argparse.ArgumentParser()

    parser.add_argument('-c',
                              '--config',
                              action='store',
                              default='conf/simple-site-backup.ini'
                        )

    return parser.parse_args()


if __name__ == '__main__':

    # get options set from argparse() and pass them to backup()
    options = vars(getopts())

    # start here - run backup() with path to config file passed
    backup.backup(options['config'])
