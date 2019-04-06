# must execute source ~/.certrc first
print("successfully opened document")
import httplib
from glue import gpstime
import sys
import pdb

try:
        from ligo.gracedb.rest import GraceDb
except ImportError:
        print >>sys.stderr, "warning: gracedb import failed, program will crash if gracedb uploads are attempted"

# set the gracedb server you want to download the events
# playground is for testing, containing replay events back to Nov. 20, 2018
# main database: https://gracedb.ligo.org/api/" includes real candidates
main_database = "gracedb" # either "gracedb" or "gracedb-playground"
print("  Searching in database: "+main_database)
gracedb_service_url = "https://"+main_database+".ligo.org/api/"
gracedb_client = GraceDb(gracedb_service_url)
#print "response status %s" % r.json()
#set the period/ condition of events, e.g. 1187008000 .. 1187009000 for the GW170817 event. Same format as input of the "Query" 
# 1 day either side of known GW events:
event_type = 'CBC 1126173062 .. 1126345862'#GW150914
#event_type = 'gstlal pycbc spiir MBTAOnline 1128592500 .. 1128765300'#GW151012
#event_type = 'CBC 1135049950 .. 1135222750'#GW151226
#event_type = 'CBC 1167473536 .. 1167646336'#GW170104
#event_type = 'CBC 1180836094 .. 1181008894'#GW170608
#event_type = 'CBC 1185303407 .. 1185476207'#GW170729
#event_type = 'gstlal MBTAOnline spiir 1186216119 .. 1186388919'#GW170809
#event_type = 'gstlal MBTAOnline spiir 1186655461 .. 1186828261'#GW170814
#event_type = 'gstlal MBTAOnline spiir 1186922482 .. 1187095282'#GW170817
#event_type = 'gstlal MBTAOnline spiir 1186971927 .. 1187144727'#GW170818
#event_type = 'CBC 1187442856 .. 1187615656'#GW170823
event_name = event_type.replace(' ', '_') # to get rid of those pesky white spaces
print('  for events satisfying: '+event_type)
events = gracedb_client.events(event_type) # number of events consistent with spiir Nov 20 - Nov 31
with open('graceid-pipeline_'+event_name,'w') as f:
        for event in events:
                gid = event['graceid']
                pipe = event['pipeline']
                f.write(gid+' '+pipe+'\n')
                fname = "%s.xml" % gid
                fout = open(fname, 'w+')
                content = gracedb_client.files(gid, filename="coinc.xml")
                fout.write(content.read())
                fout.close()

with open("name_log", "w") as f:
        f.write(main_database+"\n")
        f.write(event_name)
