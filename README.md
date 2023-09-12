# aws

# put and get data from kinesis through localstack

## Prequisite

`python3 -m pip install --upgrade localstack`

`localstack start -d`

## Install the package

`pip install Flask`

`pip install boto3`

`pip install awscli`

`sudo pip3 install awscli-local`

or 

`pip install -r requirements.txt`

## Run `python app.py`

## After that, we can go to `/`

## Alternatives:

## Command Line Version

### List stream

`awslocal kinesis list-streams`

### Create stream

`awslocal kinesis create-stream --stream-name test-stream --shard-count 1`

### Put data to stream

`awslocal kinesis put-record --stream-name test-stream --partition-key 123 --data sample-text`

### Get ShardIterator on specific stream

`awslocal kinesis get-shard-iterator --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON --stream-name test-stream`

### Get data of specific stream based on ShardIterator (replace ShardIterator with previous ShardIterator we have got from previous step)
### At this step, Records.Data will be Encrypted

`awslocal kinesis get-records --shard-iterator AAAAAAAAAAFMPnS3oxyJPoqnOVA7ReIJkOMnX9psnQ0UMUh4WP/XYBmVcFe7/WQIQboO6rr02kVTaupfLo2KvIahUKGNG6S1T94SRPxC+blVTIGTIPHXrT+1z71hkjG07vno65VxqKn74l3TxM1OAPbbxhkvZFrLg7Rzcv7g9knjJCl3MgAZbOz7nkX+d+E6Mcj5KWe93mE=`

### Decrypt Records.Data to get actual content (Replace c2FtcGxlLXRleHQ= with Records.Data)

`echo 'c2FtcGxlLXRleHQ=' | base64 -d`