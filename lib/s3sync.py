#!/usr/bin/env python

import boto3
import configparser


#def create_conn(site, ec2_region, parser):

def create_client(access_key, secret_key):

    #session = boto3.Session()
    #s3_client = session.client('s3')
    s3_client = boto3.client('s3',
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key,)

    return s3_client

if __name__ == '__main__':

    parser = configparser.ConfigParser()
    parser.read('../conf/simple-site-backup.ini')

    access_key = parser.get('defaults', 'aws_access_key')
    secret_key = parser.get('defaults', 'aws_secret_key')

    s3 = create_client(access_key, secret_key)
    print(type(s3))

    s3.upload_file('test.txt', 'setevoy-example-bucket', Key='test.txt')
    response = s3.list_objects(Bucket='setevoy-example-bucket')

    for file in response['Contents']:
        print(file['Key'])

    """
    try:
        aws_access_key = parser.get(site, 'aws_access_key')
        aws_secret_key = parser.get(site, 'aws_secret_key')
        aws_region  = parser.get(site, 'aws_region')
    except configparser.NoOptionError as e:
        aws_access_key = parser.get('defaults', 'aws_access_key')
        aws_secret_key = parser.get('defaults', 'aws_secret_key')
        aws_region = parser.get('defaults', 'aws_region')
        print('\nWARNING: {}.\nNo bucket name found for the {}, using default {}.\n'.format(e, site, bucket))


    conn = boto3.client('s3',
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key,
                        region_name=ec2_region)
    """


def upload(site, files, parser):

    try:
        bucket = parser.get(site, 's3_bucket')
    except configparser.NoOptionError as e:
        bucket = parser.get('defaults', 's3_bucket')

    for file in files:
        print('Upload {} to S3 bucket {}'.format(file, bucket))

    s3 = create_client(aws_access_key, aws_secret_key, aws_region)

    for object in s3.objects.all():
        print(object)

        #s3 = boto3.resource('s3')
        #s3.meta.client.upload_file(file, 'rtfmbackups', file)
