import boto3
import json
import readwrite

#DEFINE VARIABLES
VPC_CIDR = '10.0.0.0/16'
SUBNET_AVL_ZONE = 'us-east-1a'
SUBNET_CIDR = '10.0.0.0/24'
VPC_ID = readwrite.getdata("vpc", "vpc_id")
IGW_ID = readwrite.getdata("igw", "igw_id")
SUBNET_ID = readwrite.getdata("subnet", "subnet_id")
ROUTE_TABLE_ID = readwrite.getdata("route_table", "route_table_id")
ROUTE_TABLE_ASS_ID = readwrite.getdata("route_table_ass", "route_table_ass_id")

client = boto3.client('ec2')
iam = boto3.resource('ec2')
	
#CREATE INTERNET GATEWAY --------------------------------------------------------------
try:
	if (IGW_ID == None):
		igw = client.create_internet_gateway()
		readwrite.putdata("igw", "igw_id", igw['InternetGateway']['InternetGatewayId'])
		IGW_ID = igw['InternetGateway']['InternetGatewayId']
	else:
		print ("InternetGateway with id '%s' already exists" %IGW_ID)

except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#CREATE VPC --------------------------------------------------------------------------
try:
	if (VPC_ID == None):
		vpc = client.create_vpc(
			CidrBlock = VPC_CIDR
		)
		readwrite.putdata("vpc", "vpc_id", vpc['Vpc']['VpcId'])
		VPC_ID = vpc['Vpc']['VpcId']
	else:
		print ("VPC with id '%s' already exists" %VPC_ID)
		
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#Attach internet gateway ----------------------------------------------------------------------------
try:
	client.attach_internet_gateway(
		InternetGatewayId = IGW_ID,
		VpcId = VPC_ID
	)	
	print ("InternetGateway '%s' has been attached to VPC %s" %(IGW_ID, VPC_ID))
except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#CREATE SUBNET -------------------------------------------------------------------------
try:
	subnet = client.create_subnet(
		AvailabilityZone = SUBNET_AVL_ZONE,
		CidrBlock = SUBNET_CIDR,
		VpcId = VPC_ID
	)
	readwrite.putdata("subnet", "subnet_id", subnet['Subnet']['SubnetId'])
	SUBNET_ID = subnet['Subnet']['SubnetId']

except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#CREATE ROUTE TABLE --------------------------------------------------------------------
try:
	if (ROUTE_TABLE_ID == None):
		routeTable = client.create_route_table(
			VpcId = VPC_ID
		)
		readwrite.putdata("route_table", "route_table_id", routeTable['RouteTable']['RouteTableId'])
		ROUTE_TABLE_ID = routeTable['RouteTable']['RouteTableId']
	else:
		print ("RouteTable with id '%s' already exists" %ROUTE_TABLE_ID)

except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
	
#CREATE ROUTES FOR ROUTE TABLE -----------------------------------------------------------
try:
	client.create_route(
		DestinationCidrBlock = '0.0.0.0/0',
		GatewayId = IGW_ID,
		RouteTableId = ROUTE_TABLE_ID,
	)
	print ("Routes added to RouteTable '%s'" %ROUTE_TABLE_ID)

except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))

#ASSOCIATE ROUTE TABLE TO SUBNET ----------------------------------------------------------
try:
	route_table_ass = client.associate_route_table(
		RouteTableId = ROUTE_TABLE_ID,
		SubnetId = SUBNET_ID
	)
	readwrite.putdata("route_table_ass", "route_table_ass_id", route_table_ass['AssociationId'])
	ROUTE_TABLE_ASS_ID = route_table_ass['AssociationId']
	print ("RouteTable '%s' associated with subnet '%s' with id '%s'" %(ROUTE_TABLE_ID, SUBNET_ID, ROUTE_TABLE_ASS_ID))

except Exception as e:
	print ("Exception: %s" %(e.response['Error']['Message']))
