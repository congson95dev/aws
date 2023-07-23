from flask import Blueprint, request, jsonify
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_bp = Blueprint('s3', __name__)

@s3_bp.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    """ 
    upload file by using s3_object.put()
    """

    # get file data
    file = request.files['file']
    file_content = file.read()

    # create a connection to the S3 service
    s3 = boto3.resource('s3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_DEFAULT_REGION'))

    # upload the file to S3
    try:
        s3_object = s3.Object(os.getenv('AWS_BUCKET_NAME'), file.filename)
        s3_object.put(Body=file_content)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # after upload, get presigned url
    # with this presigned url, when we open the link it provide, it gonna make us download the file instead of view directly on browser
    presigned_url = s3_object.meta.client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': os.getenv('AWS_BUCKET_NAME'),
            'Key': file.filename
        },
        ExpiresIn=3600  # URL expires in 1 hour
    )
    
    """ 
    upload file by using s3_client.upload_fileobj()
    """

    # get file data
    file = request.files['file']
    file_name = file.filename

    # create a connection to the S3 service
    s3_client = boto3.client('s3',
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.getenv('AWS_DEFAULT_REGION'))
    
    # upload the file to S3
    try:
        s3_client.upload_fileobj(file, os.getenv('AWS_BUCKET_NAME'), file_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # after upload, get presigned url
    # with this presigned url, when we open the link it provide, it gonna make us download the file instead of view directly on browser
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': os.getenv('AWS_BUCKET_NAME'), 'Key': file_name},
        ExpiresIn=3600  # URL expires in 1 hour
    )

    # return a success message
    return jsonify({'message': 'File successfully uploaded', 'data': {'presigned_url': presigned_url}}), 200
