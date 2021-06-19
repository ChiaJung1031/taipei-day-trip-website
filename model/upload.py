import boto3
from botocore.exceptions import NoCredentialsError
from flask import jsonify 

ACCESS_KEY = 'AKIAZLKIILV66CXYMDMY'
SECRET_KEY = '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'


def upload_to_aws(local_file, bucket):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        #upload_fileobj(Fileobj, Bucket, Key, ExtraArgs=None, Callback=None, Config=None)
        s3.upload_fileobj(Fileobj=local_file, Bucket=bucket, Key=local_file.filename)
        print("Upload Successful")
        return "uploadOK"
    except FileNotFoundError:
        print("The file was not found")
        return "uploadFailure"
    except NoCredentialsError:
        print("Credentials not available")
        return "uploadFailure"