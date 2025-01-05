"""
Lambda Function 1: Serialize Image Data
 
"""

import json
import boto3
import base64


s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input (You may also check lambda test)
    key = event['s3_key']                              
    bucket = event['s3_bucket']                         
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }



    """
Lambda Function 2: Image-Classification

It takes the image output from the lambda 1 function, decodes it, and then pass inferences back to the the Step Function
"""

import json
import sagemaker
import base64
import boto3
from botocore.config import Config


# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2024-07-17-12-09-56-017" ## TODO: fill in (Trained IC Model Name)


def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])     ## TODO: fill in (Decoding the encoded 'Base64' image-data and class remains'bytes')

    # Configure the timeout settings and retry attempts for the Boto3 client
    config = Config(
        read_timeout=300,  # Increase the read timeout to 300 seconds (5 minutes)
        connect_timeout=60,  # Increase the connect timeout to 60 seconds
        retries={'max_attempts': 5}  # Increase the maximum number of retry attempts to 5
    )

    sagemaker_client = boto3.client('sagemaker')
    runtime_client = boto3.client('runtime.sagemaker', config=config)
    response = runtime_client.invoke_endpoint(
                                        EndpointName=ENDPOINT,    # Endpoint Name
                                        Body=image,               # Decoded Image Data as Input (class:'Bytes') Image Data
                                        ContentType='image/png'   # Type of inference input data - Content type (Eliminates the need of serializer)
                                    )
                                    
    
    
    inferences = json.loads(response['Body'].read().decode('utf-8'))     # list
  
    
    # We return the data back to the Step Function    
    event['inferences'] = inferences            ## List of predictions               
    return {
        'statusCode': 200,
        "body": {
            "image_data": event["body"]['image_data'],
            "s3_bucket": event["body"]['s3_bucket'],
            "s3_key": event["body"]['s3_key'],
            "inferences": event['inferences'],
       }
    }


"""
Lambda Function 3: Filter-Low-Confidence-Inferences

takes the inferences from the Lambda 2 function output and filters low-confidence inferences
"""

import json

THRESHOLD = 0.75


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['body']['inferences'] ## TODO: fill in
    
    # Check if any values in our inferences are above threshold
    meets_threshold = max(list(inferences))>THRESHOLD    
    
    # If our threshold is met, pass our data back out of the
    if meets_threshold:
        pass
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

