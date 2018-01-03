#!/usr/bin/env python


import os
import time
import configparser
import pip


def pip_install(pkg_name):
    pip.main(['install', pkg_name])


def check_deps():

    print('Checking for dependencies:')

    try:
        import boto3

        print('boto3 library already installed - OK.\n')
    except ImportError:
        print('boto3 not found - going to install it now...\n')
        pip_install('boto3')
        print('\nDone - please, restart script nnow.\n')
        exit(0)


def get_config(config):

    """Create ConfigParcer object with configuration file.
       File can be passed with -c."""

    parser = configparser.ConfigParser()

    if len(parser.read(config)) == 0:
        raise Exception('ERROR: No config file {} found!'.format(config))

    return parser


def check_dirs(dirs):

    # check for backup directories, create if not
    print('Checking directories:\n')

    for d in dirs:
        if not os.path.isdir(d):
            print('{} - not found, creating...'.format(d))
            os.mkdir(d)
        else:
            print('{} - found, OK.'.format(d))


def bkps_cleanup(site, dirs, parser):

    now = time.time()

    try:
        keep_days = parser.get(site, 'bkps_keep_days')
    except configparser.NoOptionError as e:
        print('WARNING: {}.'.format(e))
        keep_days = parser.get('defaults', 'bkps_keep_days')
        print('Using default value: {}.\n'.format(keep_days))

    for d in dirs:
        for f in os.listdir(d):
            if os.stat(os.path.join(d, f)).st_mtime < now - int(keep_days) * 86400:
                print('Deleting file: {}'.format(os.path.join(d, f)))
                os.remove(os.path.join(d, f))
            else:
                print('Keeping local data: {}'.format(os.path.join(d, f)))
