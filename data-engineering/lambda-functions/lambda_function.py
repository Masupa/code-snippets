import json
import requests
import tempfile

from extract_load import extract_load, create_aws_client


def lambda_handler(event, context):
    status_code = None
    body_text = str

    try:
        # Create an AWS s3 client
        s3_client = create_aws_client()

        # Call the extract_load function
        response = extract_load(
            s3_client=s3_client
        )

        status_code = response['status_code']
        body_text = response['message']

    except Exception as e:
        status_code = 500
        body_text = str(e)

    finally:
        return {
            'statusCode': status_code,
            'body': json.dumps(body_text)
        }
       