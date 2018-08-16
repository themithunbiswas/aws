import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g.; 'us-east-1'
region = 'ap-south-1'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
instances = ['i-050a0956fc4c748fd']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    res=ec2.start_instances(InstanceIds=instances)
    print 'started your instances: ' + str(instances)
    
    WAITER = ec2.get_waiter('instance_running')
    WAITER.wait(InstanceIds=instances)

    ec2_res = boto3.resource('ec2', region_name=region)
    ec2_pub_ip = ec2_res.Instance(instances[0]).public_ip_address
    print 'IP: '+ec2_pub_ip

	#Send Email Notification
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:465873658110:Testing',
        Message='Machine started with IP Address: '+ec2_pub_ip,
        Subject='Start Notification'
    )