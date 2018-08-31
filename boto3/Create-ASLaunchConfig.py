import boto3
import json
import readwrite

#Define variables
AWS_REGION = 'us-east-1'
LC_NAME = 'CodeDeploy-Test-ASLC-mithun' 				#Name of the AutoScaling LaunchConfiguration
AMI_ID = 'ami-04169656fea786776'						#Ubuntu 16.04 LTS
KEY_NAME = 'mithun-RnD'									#Key-pair name
INST_TYPE = 't2.micro'									#Instance type
SG_IDS = [readwrite.getdata("sg", "sg_id")]				#SecurityGroups ids Array
I_PROF_ARN = readwrite.getdata("iprof", "iprof_arn")	#Instance profile ARN
USER_DATA = '''	
#!/bin/bash

# UPDATING SYSTEM ------------------------------
sudo apt-get -y update

# INSTALLING AWS CODE-DEPLOY AGENT -------------
sudo apt-get -y install awscli
sudo apt-get -y install ruby
sudo aws s3 cp s3://aws-codedeploy-us-east-1/latest/install . --region us-east-1  
sudo chmod +x ./install
sudo ./install auto 

# INSTALLING APACHE -----------------------------
sudo apt install -y apache2

# INSTALLING NODE-JS and ANGULAR-----------------------------
sudo apt install -y zip
sudo apt install -y nodejs-legacy
sudo apt install -y npm
sudo npm install -g forever
sudo npm install -g @angular/cli
'''


client = boto3.client('autoscaling')

#CREATE AUTOSCALLING LAUNCHCONFIGURATION
try:
	client.create_launch_configuration(
		LaunchConfigurationName = LC_NAME,
		ImageId = AMI_ID,
		KeyName = KEY_NAME,
		SecurityGroups = SG_IDS,
		UserData = USER_DATA,
		InstanceType = INST_TYPE,
		IamInstanceProfile = I_PROF_ARN
	)
	print ("AutoScaling LaunchConfiguration created with name '%s'" %LC_NAME)
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
