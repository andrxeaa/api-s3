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
    directory = body.get('directory')  # p.ej. "mi-carpeta" o "carpeta/subcarpeta"

    if not bucket or not directory:
        return {'statusCode': 400, 'error': 'Faltan campos "bucket" o "directory" en body'}

    # asegurar que termine en slash
    key = directory.rstrip('/') + '/'

    s3 = boto3.client('s3')
    try:
        # Crear objeto cero-bytes que representa la "carpeta"
        s3.put_object(Bucket=bucket, Key=key, Body=b'')
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

    return {'statusCode': 200, 'bucket': bucket, 'directory': key, 'message': 'Directorio creado (objeto 0 bytes)'}
