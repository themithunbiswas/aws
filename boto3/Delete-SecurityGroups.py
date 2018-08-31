import boto3
import json
import readwrite

#DEFINE VARIABLES
SG_NAME = 'CodePipeline_SGroup'						#NAME OF THE SECURITY GROUP

client = boto3.client('ec2')

#DELETE SECURITY GROUP
try:
	client.delete_security_group(
		GroupId = readwrite.getdata("sg", "sg_id")
	)
	print ("Sercurity Group '%s' has been deleted" %SG_NAME)
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

