
from __future__ import print_function

import logging
import json
import urllib
import boto3
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
print('Loading function')

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

ddb = boto3.resource('dynamodb')

tableName = 'IoTLog2'

table = ddb.Table(tableName)

def handler(event, context):
    logger.info('got event{}'.format(event))
    t0 = time.time()
    event['epoch_time'] = t0
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = 'lambdatest911'
    filename = 'IoT.txt'
    logger.info('bucket: %s' %bucket)
    logger.info('filename: %s' %filename)
    print('bucket: %s' %bucket)
    print('filename: %s' %filename)

    # write to temporary location
#    with open('/tmp/%s' %filename, 'wb') as fid:
#        fid.write('{}'.format(event))
    with open('/tmp/%s' %filename, 'wb') as fid:
        json.dump(event, fid)

    # write to the S3 bucket
    with open('/tmp/%s' %filename, 'rb') as fid:
        s3_resource.Bucket(bucket).put_object(Key='%s' %filename, Body=fid)

    # write entry to dynamodb
    table.put_item(Item={"epoch_time":str(t0), "serialNumber":event['serialNumber'], "batteryVoltage":event['batteryVoltage']})
    # log number of entries
    logger.info('table entry count: %d' %table.item_count)
    return(filename)