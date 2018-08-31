import boto3
import json
import readwrite

#DEFINE VARIABLES
POLICY_NAME = 'CodePipeline_IProf_Policy'						#NAME OF THE POLICY FOR ROLE
I_PROF_NAME = 'CodePipeline_Instance_Profile'					#NAME OF INSTANCE PROFILE
ROLE_NAME = 'CodePipeline_IProf_Role'							#ROLE NAME
POLICY_DOC = '''{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "*"
        }
    ]
}
'''
ASSUME_ROLE_PLC_DOC = '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
'''

resource = boto3.resource('iam')
client = boto3.client('iam')

#CREATE POLICY -----------------------------------------------------------
try:
	policy = client.create_policy(
		PolicyName = POLICY_NAME,
		PolicyDocument = POLICY_DOC,
		Description='This policy is for instance profile for testing of CodePipeline'
	)
	readwrite.putdata("iprof_policy","iprof_policy_arn", policy['Policy']['Arn'])
		
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#CREATE ROLE -------------------------------------------------------------
try:
	role = client.create_role(
		RoleName = ROLE_NAME,
		AssumeRolePolicyDocument = ASSUME_ROLE_PLC_DOC,
		Description = 'This role is for instance profile for testing of CodePipeline'
	)
	
	readwrite.putdata("iprof_role", "iprof_role_arn", role['Role']['Arn'])
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
		
#ATTACH POLICY TO ROLE ---------------------------------------------------	
	
try:
	role_policy_attch = client.attach_role_policy(
		PolicyArn = readwrite.getdata("iprof_policy",'iprof_policy_arn'),
		RoleName = ROLE_NAME,
	)
	print("Policy %s Attached to the Role %s" %(POLICY_NAME, ROLE_NAME) )
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#CREATE INSTANCE-PROFILE -------------------------------------------------
try:
	iprofile = resource.create_instance_profile(
		InstanceProfileName = I_PROF_NAME
	)
	
	#printing arn to output file
	readwrite.putdata("iprof", "iprof_arn", iprofile.arn)
		
except Exception as e:	
	print ("Exception: %s" %(e.response['Error']['Message']))

#ADD ROLE TO INSTANCE-PROFILE --------------------------------------------
try:
	instance_profile_attch = client.add_role_to_instance_profile(
		InstanceProfileName = I_PROF_NAME,
		RoleName = ROLE_NAME
	)
	print ("Role %s attached to the InstanceProfile %s" %(ROLE_NAME, I_PROF_NAME))
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))