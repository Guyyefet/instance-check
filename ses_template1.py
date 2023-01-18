import boto3

def verify_email_identity():
    ses_client = boto3.client("ses", region_name="us-east-1")
    response = ses_client.verify_email_identity(
        EmailAddress="guy.yefet@gmail"
    )
    print(response)

def send_email(pls_check_instances):
    from taskworking1 import email_value 
    ses_client = boto3.client("ses", region_name="us-east-1")
    CHARSET = "UTF-8"

    # email address imported and got put into destination
    # developer is noted on instance status
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                               email_value
            ],
        },
        Message={
            "Body": {
                "Text": { 
                    "Charset": CHARSET,
                    "Data": 'Please check your instance status', pls_check_instances,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "instance notification",
            },
        },
        Source="guy.yefet@gmail.com",
    )

