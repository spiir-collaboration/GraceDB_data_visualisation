# must execute source ~/.certrc firt
print("successfully opened document")
import httplib
from glue import gpstime
import sys
import pdb

try:
	from ligo.gracedb.rest import GraceDb
except ImportError:
	print >>sys.stderr, "Warning: gracedb import failed, program will crash if gracedb uploads are attempted"

# set the gracedb server you want to download the events
# playground is for testing, containing replay events back to Nov. 20, 2018
# main database: https://gracedb.ligo.org/api/" includes real candidates
main_database = "gracedb" # either "gracedb" or "gracedb-playground"
print("  Searching in database: "+main_database)
gracedb_service_url = "https://"+main_database+".ligo.org/api/"
gracedb_client = GraceDb(gracedb_service_url)
# 
# 
# 
# 
# ???
event_type = 'CBC 1186922482 .. 1187095282'
event_name = event_type.replace(' ', '_')
print('  for events satisfying: '+event_type)
events = gracedb_client.events(event_type) # number of events consistent with piir Nov 20 - Nov 31
with open('graceid-pipeline_'+event_name,'w') as f:
	for event in events:
		gid = event['graceid']
		pipe = event['pipeline']
		f.write(gid+' '+pipe+'\n')
		fname = "%s.xml" % gid
		fout = open(fname, 'w+')
		content = gracedb_client.files(gid, filename = 'coinc.xml')
		fout.write(content.read())
		fout.close()

with open("name_log", "w") as f:
	f.write(main_database+"\n")
	f.write(event_name)
