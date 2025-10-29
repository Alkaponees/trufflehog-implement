# example_boto3_fake_creds.py
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError

# set fake credentials (for demo/testing only)
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAFAKEEXAMPLEKEY00000"
os.environ["AWS_SECRET_ACCESS_KEY"] = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYFAKEEXAMPLEKEY12"
# Optionally set region
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

def get_s3_object(bucket_name: str, key: str) -> bytes | None:
    s3 = boto3.client("s3")  # boto3 reads creds from env
    try:
        resp = s3.get_object(Bucket=bucket_name, Key=key)
        data = resp["Body"].read()
        print(f"[OK] Retrieved {len(data)} bytes from s3://{bucket_name}/{key}")
        return data
    except NoCredentialsError:
        print("[ERROR] No AWS credentials provided")
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        print(f"[ERROR] AWS ClientError: {code} - {e}")
    except EndpointConnectionError as e:
        print(f"[ERROR] Can't connect to endpoint: {e}")
    return None

if __name__ == "__main__":
    # intentionally fake - will most likely return an error from AWS (AccessDenied / InvalidAccessKeyId / SignatureDoesNotMatch)
    get_s3_object("my-demo-bucket", "path/to/object.txt")
