import boto3

client = boto3.client('iam')
'''
client.delete_role(
    RoleName='CodePipeline_IProf_Role'
)
'''
response = client.delete_instance_profile(
    InstanceProfileName='CodePipeline_Instance_Profile'
)