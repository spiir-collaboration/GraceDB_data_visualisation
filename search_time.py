import httplib
from glue import gpstime
import sys
import pdb
import numpy as np

# Code written by: Teresa Slaven-Blair

# Purpose:
#  To take in a time value - currently only set up for O1
#  Convert time value to GPS
#  Search through GraceDB catalogue around given time, looking within multiple search windows
#  Output events within each search window to file
#  Save events within each search window to another folder

# Timeframes for searches:
#  1s before -> 5s after
#  10s before -> 2m after
#  1hr before -> 1hr after
#  1hr before -> 12hr after
#  12hr before -> 12hr after
#  24hr before -> 24hr after

### ########################### ###
### Variables to change by user ###
### ########################### ###
max_time_delta = 24*60*60 # convert max time delta to seconds
input_time = 1253923218 # GPS time at 2019-10-04T03:04:54, for testing - change later to take user input

time1 = input_time - max_time_delta
time2 = input_time + max_time_delta

# looking at CBC events that were not injected
event_search = 'CBC ~Inj '+str(time1)+' .. '+str(time2)

try:
        from ligo.gracedb.rest import GraceDb
except ImportError:
        print >>sys.stderr, "warning: gracedb import failed, program will crash if gracedb uploads are attempted"

# set the gracedb server you want to download the events
# playground is for testing, containing replay events back to Nov. 20, 2018
# main database: https://gracedb.ligo.org/api/" includes real candidates
main_database = "gracedb" # either "gracedb" or "gracedb-playground"

gracedb_service_url = "https://"+main_database+".ligo.org/api/"
gracedb_client = GraceDb(gracedb_service_url)

events = gracedb_client.events(event_search)

count = 0
for event in events:
        gid = event['graceid']
        with open('data/'+str(gid),'w') as f:
                count += 1
                print(count)
                if event['superevent'] == None:
                        superevent = u'none'
                else:
                        superevent = event['superevent']
                endtime = event['gpstime']
                chirpmass = event['extra_attributes']['CoincInspiral']['mchirp']
                farc = event['extra_attributes']['CoincInspiral']['combined_far']
                snrc = event['extra_attributes']['CoincInspiral']['snr']
                num_of_det = len(event['extra_attributes']['SingleInspiral'])
                ifos = np.chararray(num_of_det, itemsize = 8)# itemsize=8 for dtype=np.float64) equivalent. itemsize=16 for dtype=np.complex128 equivalent
                snri = np.chararray(num_of_det, itemsize = 8)
                chisqi = np.chararray(num_of_det, itemsize = 8)
                eff_dist = np.zeros(num_of_det)
                mass1 = np.zeros(num_of_det)
                mass2 = np.zeros(num_of_det)
                print(".")
                for idx in range(num_of_det):
                        ifos[idx] = event['extra_attributes']['SingleInspiral'][idx]['ifo']
                        try:
                                snri[idx] = event['extra_attributes']['SingleInspiral'][idx]['snr']
                        except KeyError:
                                snri[idx] = 0.0
                        mass1[idx] = event['extra_attributes']['SingleInspiral'][idx]['mass1']
                        mass2[idx] = event['extra_attributes']['SingleInspiral'][idx]['mass2']
                        try:
                                chisqi[idx] = event['extra_attributes']['SingleInspiral'][0]['chisq']
                        except KeyError:
                                chisqi[idx] = u'none'
                                #print("No chisq for that detector")
                        try:
                                eff_dist[idx] = event['extra_attributes']['SingleInspiral'][idx]['eff_distance']
                        except KeyError:
                                #print("No effective distance for that detector")
                                key_error = "No effective distance for that detector at index"+str(idx)
#                       print("check 4")
#               print(".")
                pipe = event['pipeline']
#               f.write(gid+' '+pipe+' '+superevent+'\n')
#               f.write(gid+' '+pipe+'\n')
                fname = "%s.xml" % gid
                fout = open(fname, 'w+')
#               print("check 5")
                try:
                        content = gracedb_client.files(gid, filename="coinc.xml")
                except:
                        print("didn't like that gid: "+str(gid))
                fout.write(content.read())
                fout.close()
                f.write(str(gid)+','+str(superevent)+','+str(endtime)+','+str(chirpmass)+','+str(farc)+','+str(snrc)+','+str(ifos)+','+str(snri)+','+str(chisqi)+','+str(pipe)+','+str(eff_dist)+','+str(mass1)+','+str(mass2))
