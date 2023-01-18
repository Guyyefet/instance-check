import boto3
from datetime import datetime, timezone, timedelta

EC2_SESSION = boto3.Session(region_name="us-east-1")
EC2_RESOURCE = boto3.resource('ec2', 'us-east-1')
# EC2_CLIENT = boto3.client('ec2')

# tag = EC2_RESOURCE.Tag('resource_id','key','value')
# instance_email = ''
tag = ''
protected_instances = []
pls_check_instances = []


def instance_tags_check():
  instances = EC2_RESOURCE.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
  for instance in instances:
    for tag in instance.tags:
      if tag['Value'] != "Protected":
        instance.stop()
        print("stopped instances:", instance.id, instance.name)
      else: 
        protected_instances.append(instance)
        print("protected instances:", protected_instances, tag)

          # if instance.tags == None: 
          #      instance.stop()
          #      print("stopped instances:", instance.id)
          # else: 
          #   for tag in instance.tags: 
          #     if tag["Key"] == "Protected":
          #          protected_instances.append(instance)
          #          print("protected instances:", protected_instances, tag)

def check_instance_runtime(instance_email):
  for instance in protected_instances:
    instance_uptime = datetime.now(timezone.utc) - instance.launch_time
    instance_uptime = instance_uptime.days
    if instance_uptime >= 7:
      pls_check_instances.append(instance)
      for tag in instance.tags:
        if tag['Key'] == 'Email':
          instance_email = tag['Value']
          print('instance is running more then a week', pls_check_instances,  instance.id,  instance_email)
    elif instance_uptime >= 14:
      instance.stop()
      print('instance is running more then 2 weeks, instance is stopped', pls_check_instances, instance.id, instance_email)
    else: 
      print('instance is running less then a week', instance.id)

def send_email(instance_email):

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
  



instance_tags_check()
check_instance_runtime(instance_email)