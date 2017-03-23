from __future__ import print_function

import zipfile
import os
from datetime import datetime
from urllib2 import urlopen

SITE = 'http://www.penn.museum/collections/assets/data/all-json-latest.zip'


def validate(res):
    zip_ref = zipfile.ZipFile(res, 'r')
    s3 = boto3.resource('s3')
    zip_ref.extractall(s3.Bucket("archaeology-lookup"))
    zip_ref.close()


def lambda_handler(event, context):
    print('Checking {} at {}...'.format(SITE, event['time']))
    try:
        if not validate(urlopen(SITE).read()):
            raise Exception('Validation failed')
    except:
        print('Check failed!')
        raise
    else:
        print('Check passed!')
        return event['time']
    finally:
        print('Check complete at {}'.format(str(datetime.now())))
