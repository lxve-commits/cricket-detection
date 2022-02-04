import boto3
import botocore
import sys, getopt
import os

def upload_to_bucket(argv):
    bucket_name = ''
    body = ''
    try:
        opts, args = getopt.getopt(argv, 'hn:k:b:')
    except getopt.GetoptError:
        print('upload_to_bucket.py -n <nameOfBucket> -b <FolderName>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('upload_to_bucket.py -n <nameOfBucket> -b <FolderName>')
            sys.exit()
        elif opt in ('-n'):
            bucket_name = arg
        elif opt in ('-b'):
            body = arg
    return bucket_name, body
BUCKET_NAME, BODY = upload_to_bucket(sys.argv[1:])
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
#s3.Bucket(BUCKET_NAME).put_object(Key=KEY, Body=BODY)

if os.path.isfile(BODY):
    s3_client.upload_file(BODY, BUCKET_NAME, BODY)
else:
    s3_client.put_object(Bucket=BUCKET_NAME, Key= BODY + '/')
    for item in os.listdir(BODY):
        response = s3_client.upload_file(BODY + '/' + item, BUCKET_NAME, item)
        print(response)
#print(s3_client)
#s3 = boto3.resource('s3')
#print(s3.download_file('grillenrepository', '/', ''))
