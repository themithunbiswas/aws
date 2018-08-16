import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'ap-south-1'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
instances = ['i-050a0956fc4c748fd']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print 'stopped your instances: ' + str(instances)
    
    WAITER = ec2.get_waiter('instance_stopped')
    WAITER.wait(InstanceIds=instances)

	#Send Email Notification
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:465873658110:Testing',
        Message='Machine stopped',
        Subject='Stop Notification'
    )