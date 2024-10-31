
# Exporting DynamoDB Data to CSV and JSON Using Python


This Python script exports data from an Amazon DynamoDB table into both CSV and JSON files. This can be useful for data analysis, backups, or sharing data with others without direct access to your DynamoDB table.

### Prerequisites

1. **AWS Account**: Ensure you have an AWS account with access to DynamoDB.
2. **Python and `boto3`**: Install Python and the `boto3` library (AWS SDK). You can install `boto3` by running:
   ```bash
   pip install boto3
   ```

### Configure your AWS credentials on your system
   ```bash
   aws configure
   ```

This command will prompt you to enter your AWS Access Key, Secret Key, region, and output format.

### Complete Python script
The following Python script exports data from DynamoDB to both CSV and JSON formats.

```python
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
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(TABLE_NAME)

        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        with open(JSON_FILE_PATH, 'w') as json_file:
            json.dump(data, json_file, default=decimal_default, indent=4)

        if data:
            with open(CSV_FILE_PATH, 'w', newline='') as csv_file:
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
```
### How to Use the Script
1) Replace `TABLE_NAME` with your DynamoDB table name.
2) Execute the script using Python:
    ```bash
    python export_dynamodb_data.py
    ```
3) On successful execution, check for dynamodb_data.csv and dynamodb_data.json in your script directory.

### Troubleshooting
* Ensure your AWS credentials are properly configured using `aws configure` if you encounter `NoCredentialsError` or `PartialCredentialsError`.
* Verify that the IAM role associated with your credentials has read access to the DynamoDB table.

With this setup, you can easily export your DynamoDB data to CSV and JSON formats for further analysis or backup.

