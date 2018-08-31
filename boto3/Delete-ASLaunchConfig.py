import boto3
import json
import readwrite

#DEFINE VAIRABLES
LC_NAME = 'CodeDeploy-Test-ASLC-mithun' 				#Name of the AutoScaling LaunchConfiguration


client = boto3.client('autoscaling')

#DELETING AUTO SCALING LAUNCH CONFIGURATION
try:
	client.delete_launch_configuration(
		LaunchConfigurationName = LC_NAME,
	)
	print ("AutoScaling LaunchConfiguration '%s' deleted" %LC_NAME)
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
