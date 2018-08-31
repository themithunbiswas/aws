import json
import os

infra_data = {}
DIR = './output'

def getdata(file, key):
	FILE="%s/%s.json" %(DIR, file)
	print("Reading '%s' value of '%s' file" %(key, FILE))
	
	try:
		with open(FILE) as f:
			infra = json.load(f)
			
		try:
			return infra[key]
		except Exception as e:
			print ("'%s' key not found !" %key)
			return None
	except Exception as e:
		print ("'%s' file not found !" %file)
		return None
		
	
def putdata(file, key, value):
	FILE="%s/%s.json" %(DIR, file)
	print("Writing '%s' as '%s' to '%s' file" %(key, value, FILE))
	infra_data[key] = value
	
	with open(FILE, mode='w') as f:
		json.dump(infra_data, f)		
		
def delfile(file):
	FILE="%s/%s.json" %(DIR, file)
	if os.path.exists(FILE):
		os.remove(FILE)
		print ("The file '%s' deleted" %FILE)
	else:
		print ("The file '%s' does not exist" %FILE)

		
#delfile("route_table_ass")