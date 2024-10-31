import boto3
import csv
import json
from decimal import Decimal
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Replace with your table name
TABLE_NAME = 'your-dynamodb-table-name'
CSV_FILE_PATH = 'dynamodb_data.csv'
JSON_FILE_PATH = 'dynamodb_data.json'

def dynamodb_to_csv_and_json():
    # Initialize a DynamoDB client
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(TABLE_NAME)

        # Scan the table to get all items
        response = table.scan()
        data = response['Items']

        # Loop to handle pagination if the result is larger than 1MB
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        # Convert DynamoDB Decimal objects to float for JSON serialization
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        # Save data to JSON
        with open(JSON_FILE_PATH, 'w') as json_file:
            json.dump(data, json_file, default=decimal_default, indent=4)

        # Save data to CSV
        if data:
            with open(CSV_FILE_PATH, 'w', newline='') as csv_file:
                # Get the header from the first item keys
                headers = data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)

        print(f"Data successfully exported to {CSV_FILE_PATH} and {JSON_FILE_PATH}")

    except NoCredentialsError:
        print("No AWS credentials found. Please configure your AWS credentials.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials found. Please check your AWS configuration.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    dynamodb_to_csv_and_json()

