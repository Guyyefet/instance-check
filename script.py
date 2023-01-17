import boto3
from datetime import datetime, timezone, timedelta

EC2_SESSION = boto3.Session(region_name="us-east-1")
EC2_RESOURCE = boto3.resource('ec2', 'us-east-1')
EC2_CLIENT = boto3.client('ec2')

# tag = ''
instance_email = ''
protected_instances = []


def instance_tags_check():
  instances = EC2_RESOURCE.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
  for instance in instances:
    for tag in instance.tags:
      if tag['Key': 'dev_status' ] != "Protected" or instance.tags == None:
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
      for tag in instance.tags:
        if tag['Key'] == 'Email':
          instance_email = tag['Value']
          print('instance is running more then a week', instance.id,  instance_email)
        elif instance_uptime >= 14:
          instance.stop()
          print('instance is running more then 2 weeks, instance is stopped', instance.id, instance_email)
        else: 
          print('instance is running less then a week', instance.id)

def send_email(instance_email):
  



instance_tags_check()
check_instance_runtime(instance_email)