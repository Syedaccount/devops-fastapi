import boto3
import os
import base64
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY")
secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("AWS_BUCKET")
region_name = os.getenv("AWS_BUCKET_REGION")


s3 = boto3.client('s3', 
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key,
                  region_name=region_name)


def upload_base64_image_to_s3(base64_string):
    
    try:
        current_datetime = datetime.now()
        object_name=current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        object_name=object_name+".jpeg"
        image_data = base64.b64decode(base64_string)
        image = BytesIO(image_data)
        s3.upload_fileobj(image, bucket_name, object_name)
        presigned_url = s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name,
                                                          'Key': object_name},
                                                  ExpiresIn=604800)  # 1 hour expiry
        return object_name,presigned_url
    except:
        print("Credentials not available")
        return None


