import json
import requests
import tempfile

from upload import upload


url = "https://football-data.co.uk/mmz4281/2627/E0.csv"


def lambda_handler(event, context):
    status_code = None
    body_text = str

    # Fetch the CSV data from the URL
    response = requests.get(url)

    if response.status_code == 200:
        status_code = response.status_code

        # Save the CSV data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        # upload the CSV data to S3
        upload(temp_file_path)
        body_text = "Data uploaded successfully."

    else:
        status_code = response.status_code
        body_text = "Failed to fetch data."

    return {
        'statusCode': status_code,
        'body': json.dumps(body_text)
    }
        