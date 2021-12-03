import boto3

def s3_download_file(s3_path: str, file_name: str) -> str:
    local_path = f'files/{file_name}'
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("conversionaudiogrupo4")
    bucket.download_file(s3_path,
                         local_path)
    return local_path

def s3_upload_file(local_path: str, file_name: str, bucket: str) -> str:
    s3_path = f'files/{file_name}'
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    bucket.upload_file(local_path, s3_path)
    return s3_path