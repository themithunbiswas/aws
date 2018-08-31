import boto3
import json
import readwrite

#DEFINE VARIABLES
VPC_ID = readwrite.getdata("vpc", "vpc_id")
SUBNET_ID = readwrite.getdata("subnet", "subnet_id")
ROUTE_TABLE_ASS_ID = readwrite.getdata("route_table_ass", "route_table_ass_id")
ROUTE_TABLE_ID = readwrite.getdata("route_table", "route_table_id")
IGW_ID = readwrite.getdata("igw", "igw_id")


client = boto3.client('ec2')
iam = boto3.resource('ec2')

#DELETE ROUTES -----------------------------------------------------------------------
try:
	if(ROUTE_TABLE_ID != None):
		response = client.delete_route(
			DestinationCidrBlock = '0.0.0.0/0',
			RouteTableId = ROUTE_TABLE_ID
		)
		print ("Routes has been deleted")
	else:
		print ("No Routes to delete")
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#DEASSOCIATE ROUTE TABLE -------------------------------------------------------------
try:
	if(ROUTE_TABLE_ID != None):
		client.disassociate_route_table(
			AssociationId = ROUTE_TABLE_ASS_ID
		)
		print ("RouteTable Desassociated from subnet '%s'" %SUBNET_ID)
		readwrite.delfile("route_table_ass")
	else:
		print ("No route table association found")
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#DELETE ROUTE TABLE ------------------------------------------------------------------
try:
	if(ROUTE_TABLE_ID != None):
		response = client.delete_route_table(
			RouteTableId = ROUTE_TABLE_ID
		)
		print ("RouteTable '%s' Deleted" %ROUTE_TABLE_ID)
		readwrite.delfile("route_table")
	else:
		print ('No route table to delete')
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#DELETE SUBNET -----------------------------------------------------------------------
try:
	if(SUBNET_ID != None):
		client.delete_subnet(
			SubnetId = SUBNET_ID
		)
		print ("Subnet '%s' Deleted" %SUBNET_ID)
		readwrite.delfile("subnet")
	else:
		print ("No subnet to delete")
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#DETACH INTERNET GATEWAY -------------------------------------------------------------
try:
	if(IGW_ID != None):
		client.detach_internet_gateway(
			InternetGatewayId = IGW_ID,
			VpcId = VPC_ID
		)
		print ("InternetGateway '%s' Detached from VPC '%s'" %(IGW_ID, VPC_ID))
	else:
		print ("No InternetGateway found to detach")
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#DELETE INTERNET GATEWAY -------------------------------------------------------------
try:
	if(IGW_ID != None):
		client.delete_internet_gateway(
			InternetGatewayId = IGW_ID
		)
		print ("InternetGateway '%s' Deleted" %IGW_ID)
		readwrite.delfile("igw")
	else:
		print ("No InternetGateway found to delete")
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#DELETE VPC --------------------------------------------------------------------------
try:
	if(VPC_ID != None):
		client.delete_vpc(
			VpcId = VPC_ID
		)
		print ("VPC with id '%s' deleted" %VPC_ID)
		readwrite.delfile("vpc")
	else:
		print ("No VPC found to delete")
	
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

