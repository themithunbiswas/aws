import boto3
import json
import readwrite

#DEFINE VARIABLES
SG_NAME = 'CodePipeline_SGroup'						#NAME OF THE SECURITY GROUP
VPC_ID = readwrite.getdata("vpc", "vpc_id")			#ID OF VPC

client = boto3.client('ec2')

#CREATE SECURITY GROUP
try:
	sg = client.create_security_group(
		GroupName = SG_NAME,
		Description = 'This Security Group has been create for testing of CodePipeline',
		VpcId = VPC_ID
	)
	readwrite.putdata("sg", "sg_id", sg["GroupId"])
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#DEFINE INBOUD AND OUTBOUND RULES FOR SECURITY GROUP	
try:
	ingress = client.authorize_security_group_ingress(
		GroupId = readwrite.getdata("sg", "sg_id"),
		IpPermissions=[
			{
				'FromPort': 80,
				'ToPort': 80,
				'IpProtocol': 'tcp',
				'IpRanges': [
					{
						'CidrIp': '0.0.0.0/0',
						'Description': 'HTTP port is Open to all'
					},
				]
			},
			{
				'FromPort': 4200,
				'ToPort': 4200,
				'IpProtocol': 'tcp',
				'IpRanges': [
					{
						'CidrIp': '0.0.0.0/0',
						'Description': 'HTTP port is Open to all'
					},
				]
			},
		]
	)
	print("Inbound Rule Security Group %s has beeen added" %SG_NAME)
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))