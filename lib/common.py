#!/usr/bin/env python


import os
import time
import configparser
import pip


def pip_install(pkg_name):
    pip.main(['install', pkg_name])


def check_deps():

    print('\nChecking for dependencies:')

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


def set_params(parser, section):

    """
    Depending on a passed $section will return dictionary with values:

        for the [backup-settings] section:

    'backup_root_path': '/backups',
    'backup_files_path': 'files',
    'backup_db_path': 'databases'

        for the [test] section:

    'www_data_path': '/tmp/testbak/',
    'mysql_db': 'bkp_test',
    'mysql_host': 'localhost',
    'mysql_user': 'bkp_test',
    'mysql_pass': 'bkp_test'

    """

    # set own settings if "backup-settings" passed
    if section == 'backup-settings':
        params = dict.fromkeys([
            'backup_root_path',
            'backup_files_path',
            'backup_db_path'])
    # otherwise set site's settings
    else:
        params = dict.fromkeys([
            'www_data_path',
            'mysql_db',
            'mysql_host',
            'mysql_user',
            'mysql_pass'])

    for param in params:
        params[param] = parser.get(section, param)

    return params


def check_dirs(dirs):

    # check for backup directories, create if not
    print('Checking directories:\n')

    for dir in dirs:
        if not os.path.isdir(dir):
            print('{} - not found, creating...'.format(dir))
            os.mkdir(dir)
        else:
            print('{} - found, OK.'.format(dir))


def bkps_cleanup(site, dirs, parser):

    now = time.time()

    try:
        keep_days = parser.get(site, 'bkps_keep_days')
    except configparser.NoOptionError as e:
        print('WARNING: {}.'.format(e))
        keep_days = parser.get('defaults', 'bkps_keep_days')
        print('Using default value: {}.\n'.format(keep_days))

    for dir in dirs:
        for f in os.listdir(dir):
            if os.stat(os.path.join(dir, f)).st_mtime < now - int(keep_days) * 86400:
                print('Deleting file: {}'.format(os.path.join(dir, f)))
                #os.remove(os.path.join(dir, f))
                print('To del: {}'.format(os.path.join(dir, f)))
            else:
                print('Saving files: {}'.format(os.path.join(dir, f)))