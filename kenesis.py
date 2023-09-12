from flask import Blueprint, jsonify
import boto3
import datetime
from dotenv import load_dotenv

load_dotenv()

kenesis_bp = Blueprint('kenesis', __name__)


@kenesis_bp.route('/', methods=['POST'])
def put_data():
    # http://localhost:4566 is url of localstack
    client = boto3.client('kinesis', region_name='us-east-1', endpoint_url='http://localhost:4566')
    put_data = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
    response = client.put_record(StreamName='test-stream', Data=put_data, PartitionKey='123')

    return jsonify({'message': 'File successfully uploaded', 'data': response}), 200


@kenesis_bp.route('/', methods=['GET'])
def get_data():
    # http://localhost:4566 is url of localstack
    client = boto3.client('kinesis', region_name='us-east-1', endpoint_url='http://localhost:4566')
    shard_response = client.get_shard_iterator(
        StreamName='test-stream', ShardId='shardId-000000000000', ShardIteratorType='TRIM_HORIZON'
    )
    response = {"shard_response": shard_response}

    record_count = 0
    shard_iterator = shard_response["ShardIterator"]
    while record_count < 20:
        get_record_response = client.get_records(ShardIterator=shard_iterator)
        records = get_record_response["Records"]
        shard_iterator = get_record_response["NextShardIterator"]
        if len(records) == 0:
            break
        record_count += len(records)

        for record in records:
            response["record_data"] = {"record_data_" + record["SequenceNumber"]: record["Data"].decode("utf-8")}

    return jsonify({'message': 'File successfully uploaded', 'data': response}), 200
