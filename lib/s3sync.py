#!/usr/bin/env python

import os
import boto3
import configparser


def create_client(access_key, secret_key):

    s3_client = boto3.client('s3',
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,)

    return s3_client


def upload(site, files, parser):

    try:
        aws_access_key = parser.get(site, 'aws_access_key')
        aws_secret_key = parser.get(site, 'aws_secret_key')
        aws_s3_bucket = parser.get(site, 'aws_s3_bucket')
        s3 = create_client(aws_access_key, aws_secret_key)
    except configparser.NoOptionError as e:
        print('ERROR: no "aws_access_key" and "aws_secret_key" options found'
              'in the configuration file for the {} site: {}.'.format(site, e))
        exit(1)

    for file in files:

        print('Uploading {} to S3 bucket {} as {}'.format(file, aws_s3_bucket, os.path.basename(file)))
        s3.upload_file(file, aws_s3_bucket, Key=os.path.basename(file))

    response = s3.list_objects(Bucket=aws_s3_bucket)
    print('\nExisting data in the {} bucket:\n'.format(aws_s3_bucket))
    for file in response['Contents']:
        print(file['Key'])
