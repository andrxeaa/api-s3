import json
import boto3

def _parse_body(event):
    body = event.get('body', {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except:
            body = {}
    return body

def lambda_handler(event, context):
    body = _parse_body(event)
    bucket = body.get('bucket')
    if not bucket:
        return {'statusCode': 400, 'error': 'Falta campo "bucket" en body'}

    s3 = boto3.client('s3')
    session = boto3.session.Session()
    region = session.region_name or 'us-east-1'

    try:
        # create_bucket requiere LocationConstraint salvo que sea us-east-1
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

    return {'statusCode': 200, 'bucket': bucket, 'message': 'Bucket creado'}
