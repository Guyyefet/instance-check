import boto3
from datetime import datetime, timezone, timedelta

EC2_SESSION = boto3.Session(region_name="us-east-1")
EC2_RESOURCE = boto3.resource('ec2', 'us-east-1')
# EC2_CLIENT = boto3.client('ec2')

# tag = EC2_RESOURCE.Tag('resource_id','key','value')
instance_email = {}
tag = {}
protected_instances = []
pls_check_instances = []
issent = False

class Email_Data:
  def __init__(self, email: str, issent: bool, timestamp: datetime):
    self.email = email
    self.issent = issent
    self.timestamp = timestamp


def instance_tags_check():
  instances = EC2_RESOURCE.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
  for instance in instances:
    if {'Key': 'Status', 'Value': 'Protected'} in instance.tags:
      protected_instances.append(instance)
      print("protected instances:", instance.id, instance.tags)
    else:
      instance.stop()
      print("stopped instances:", protected_instances)
      
def check_instance_runtime(instance_email, tag):
  for instance in protected_instances:
    instance_uptime = datetime.now(timezone.utc) - instance.launch_time
    instance_uptime = instance_uptime.seconds
    if instance_uptime in range(30, 300):
      pls_check_instances.append(instance)
      check_issent()
      print('instance is running more then a week', pls_check_instances, instance_uptime, instance_email)
    elif instance_uptime >= 300:
      instance.stop()
      print('instance is running more then 2 weeks, instance is stopped', pls_check_instances, instance_uptime, instance_email)
    else: 
      print('instance is running less then a week', instance.id)

def get_email_data(instance_email):
  for instance in pls_check_instances:
    for tag in instance.tags:
      if tag['Key'] == 'Email':
        instance_email = tag['Value']
      else:
        pass
      email_data = Email_Data(instance_email, issent, datetime.now(timezone.utc))
      # email_data1 = email_data(instance_email, issent, timestamp)

def send_email(instance_email, issent):
  pass

def check_issent(issent):
  if issent == False:
    send_email()
  else:
    print("issent is True")



  

instance_tags_check()
check_instance_runtime(tag, instance_email)
get_email_data(instance_email, issent)