import boto3
import json
import readwrite

client = boto3.client('ec2')

try:
	vpc = client.create_vpc(
		CidrBlock='10.0.0.0/16'
	)
	
	print (vpc['Vpc']['VpcId'])
		
except Exception as e:	
	print ("Exception: %s" %e)
		
