import boto3
import json
import readwrite

#DEFINE VARIABLES
POLICY_NAME = 'CodePipeline_IProf_Policy'						#NAME OF THE POLICY FOR ROLE
I_PROF_NAME = 'CodePipeline_Instance_Profile'					#NAME OF INSTANCE PROFILE
ROLE_NAME = 'CodePipeline_IProf_Role'							#ROLE NAME

resource = boto3.resource('iam')
client = boto3.client('iam')

#REMOVE ROLE FROM INSTANCE-PROFILE --------------------------------------------
try:
	client.remove_role_from_instance_profile(
		InstanceProfileName = I_PROF_NAME,
		RoleName = ROLE_NAME
	)
	print ("Role '%s' has been removed from InstanceProfile '%s'" %(ROLE_NAME, I_PROF_NAME))
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))


#DELETE INSTANCE-PROFILE -------------------------------------------------
try:
	client.delete_instance_profile(
		InstanceProfileName = I_PROF_NAME
	)
	
	print ("InstanceProfile '%s' has been deleted" %I_PROF_NAME)
		
except Exception as e:	
	print ("Exception: %s" %(e.response['Error']['Message']))

#DETTACH POLICY TO ROLE ---------------------------------------------------		
try:
	client.detach_role_policy(
		PolicyArn = readwrite.getdata("iprof_policy",'iprof_policy_arn'),
		RoleName = ROLE_NAME
	)
	print("Policy %s Dettached from the Role %s" %(POLICY_NAME, ROLE_NAME))
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#DELETE ROLE -------------------------------------------------------------
try:
	client.delete_role(
		RoleName = ROLE_NAME
	)
	print ("Role '%s' has been deleted" %ROLE_NAME)
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
		
#DELETE POLICY -----------------------------------------------------------
try:
	client.delete_policy(
		PolicyArn = readwrite.getdata("iprof_policy",'iprof_policy_arn')
	)
	print ("Policy '%s' has been deleted" %POLICY_NAME)
		
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))


		


