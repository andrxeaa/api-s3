import json
import boto3
import base64

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
    directory = body.get('directory', '')  # opcional, p.ej. "carpeta/sub/"
    filename = body.get('filename')
    content = body.get('content')  # texto plano o base64
    is_base64 = body.get('base64', False)  # booleano opcional

    if not bucket or not filename or content is None:
        return {'statusCode': 400, 'error': 'Faltan campos "bucket", "filename" o "content" en body'}

    # normalizar directory
    if directory and not directory.endswith('/'):
        directory = directory + '/'
    key = f"{directory}{filename}"

    # preparar body
    try:
        if is_base64:
            body_bytes = base64.b64decode(content)
        else:
            # tratar content como string UTF-8
            if isinstance(content, str):
                body_bytes = content.encode('utf-8')
            else:
                # ya es bytes-like
                body_bytes = content
    except Exception as e:
        return {'statusCode': 400, 'error': f'Error al procesar "content": {str(e)}'}

    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body_bytes)
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

    return {'statusCode': 200, 'bucket': bucket, 'key': key, 'message': 'Archivo subido'}
