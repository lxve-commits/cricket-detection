import boto3
import botocore
import sys, getopt
def download_from_bucket(argv):
    bucket_name = ''
    key = ''
    try:
        opts, args = getopt.getopt(argv, "hn:k:")
    except getopt.GetoptError:
        print('upload_to_bucket.py -n <nameOfBucket> -k <KeyOfBucket>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('upload_to_bucket.py -n <nameOfBucket> -k <KeyOfBucket>')
            sys.exit()
        elif opt in ("-n"):
            bucket_name = arg
        elif opt in ("-k"):
            key = arg
    return bucket_name, key

BUCKET_NAME, KEY = download_from_bucket(sys.argv[1:])
s3 = boto3.resource('s3')
print("Bucket:" +BUCKET_NAME + "KEy:" + KEY)
try:
    file = s3.Bucket(BUCKET_NAME).download_file(KEY, KEY)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise