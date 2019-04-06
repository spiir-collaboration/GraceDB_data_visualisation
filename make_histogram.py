import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time

def get_pipes(title):
        filename = "graceid-pipeline_"+title[8:]
        data = []
        pipes = []
        ids = []
        with open(filename, 'r') as f:
                for line in f:
                        line = line[1:-1]
                        split_line = line.split(' ')
                        data.append(split_line)
        for idx in range(len(data)):
                data[idx][0] = int(data[idx][0])
        data.sort()
        for idx in range(len(data)):
                pipes.append(data[idx][1])
                ids.append('G'+str(data[idx][0]))
        return pipes, ids

def get_bins(all_data, num_obs, num_events, input_idx, with_outliers):
        # function works out the min and max of the whole data for a histogram and sets
        # the bins based on variable nbin
        data = []
        nbin = 20
        for ev_idx in range(num_events):
                for ob_idx in range(1, len(all_data[ev_idx])):
                        data.append(float(all_data[ev_idx][ob_idx][input_idx]))
        if with_outliers == False:
                temp_min = np.percentile(data, 25) - (np.percentile(data, 75) - np.percentile(data, 25))*3
                temp_data = [i for i in data if i >= temp_min]
                min_range = max(min(temp_data), temp_min)

                temp_max = np.percentile(data, 75) + (np.percentile(data, 75) - np.percentile(data, 25))*3
                temp_data = [i for i in data if i <= temp_max]
                max_range = min(max(temp_data), temp_max)
        else:
                min_range = min(data)
                max_range = max(data)
        binwidth = (max_range - min_range)/nbin
        bins = np.arange(min_range, max_range + binwidth, binwidth)
        return bins

filename = "log_events"

def plot_indiv(all_data, colours, input_idx, input_bins, num_obs, num_events, data_name):
        sngl_H1 = []
        sngl_L1 = []
        sngl_V1 = []
        for ev_idx in range(len(all_data)-1):
                for ob_idx in range(1,len(all_data[ev_idx][1:])+1):
                        if all_data[ev_idx][ob_idx][1] == 'H1':
                                sngl_H1.append(float(all_data[ev_idx][ob_idx][input_idx]))
                        elif all_data[ev_idx][ob_idx][1] == 'L1':
                                sngl_L1.append(float(all_data[ev_idx][ob_idx][input_idx]))
                        elif all_data[ev_idx][ob_idx][1] == 'V1':
                                sngl_V1.append(float(all_data[ev_idx][ob_idx][input_idx]))
        data_sets = [sngl_H1, sngl_L1, sngl_V1]
        data_names = ['H1', 'L1', 'V1']
        for idx in range(3):
                if data_sets[idx] != []:
                        plt.hist(data_sets[idx], bins = input_bins, label = data_names[idx], alpha = 0.5)
        plt.title(data_name+' for single detectors')
        plt.legend()
        plt.savefig(title+'-'+data_name+'-Individual.png')
        plt.clf()
        return data_sets

def plot_comb(all_data, num_events, input_idx, data_name):
        spiir_data = []
        spiir_times = []
        gstlal_data = []
        gstlal_times = []
        pycbc_data = []
        pycbc_times = []
        other_data = []
        other_times = []
        for ev_idx in range(num_events):
                num_det = 0
                for det_idx in range(1,4):
                        if all_data[ev_idx][0][det_idx] == 'H1':
                                num_det += 1
                        if all_data[ev_idx][0][det_idx] == 'L1':
                                num_det += 1
                        if all_data[ev_idx][0][det_idx] == 'V1':
                                num_det += 1
                        if all_data[ev_idx][0][det_idx] == 'L1H1':
                                num_det += 1
                        else:
                                num_det += 0
                if data_name == 'FAR':
                        data = np.log10(float(all_data[ev_idx][0][num_det + input_idx]))
                else:
                        data = float(all_data[ev_idx][0][num_det + input_idx])
                if ordered_pipes[ev_idx] == 'spiir':
                        spiir_data.append(data)
                        spiir_times.append(int(all_data[ev_idx][0][0]))
                elif ordered_pipes[ev_idx] == 'gstlal':
                        gstlal_data.append(data)
                        gstlal_times.append(int(all_data[ev_idx][0][0]))
                elif ordered_pipes[ev_idx] == 'pycbc':
                        pycbc_data.append(data)
                        pycbc_times.append(int(all_data[ev_idx][0][0]))
                else:
                        other_data.append(data)
                        other_times.append(int(all_data[ev_idx][0][0]))
        # plot with parameters determined by pipeline
        plt.plot(spiir_times, spiir_data, color = 'b', marker = 'o', linestyle = 'None', label='spiir')
        plt.plot(gstlal_times, gstlal_data, color = 'g', marker = '^', linestyle = 'None', label='gstlal')
        plt.plot(pycbc_times, pycbc_data, color = 'y', marker = 's', linestyle = 'None', label='pycbc')
        plt.plot(other_times, other_data, color = 'r', marker = 'x', linestyle = 'None', label='other')
        plt.title(data_name+' for combined detectors')
        plt.xlabel("Time")
        plt.ylabel(data_name)
        plt.legend(loc='best')
        plt.savefig(title+'-'+data_name+'-Combined.png')
        plt.clf()

# reads out the name for the data used
# name log will have the database (gracedb or gracedb-playground) and the search terms
labels = []
with open("name_log", "r") as f:
        for line in f:
                labels.append(line)

title = labels[0][:-1]+"-"+labels[1]
print(title)

ordered_pipes, ordered_ids = get_pipes(title)

# read out all the data from the file of name filename, spliting it appropriately and removing \n
indiv_data = []
all_data = []
with open(filename) as f:
        for line in f:
                if line != '\n':
                        line = line[:-1]
                        split_line = line.split(',')
                        indiv_data.append(split_line)
                        #print("indiv_data: "+str(indiv_data))
                elif line == '\n':
                        all_data.append(indiv_data)
                        indiv_data = []

num_events = len(all_data) - 1
num_obs = len(all_data[0])

indiv_snrs = []
indiv_chisqs = []
labels = []

# get GPS time: find numbers that are larger than the gps time for year 2000
gps = [s for s in title.split("_") if s.replace(".","", 1).isdigit() and s > 630720013]

if gps != []:
        for t in gps:
                utc = Time(int(t), format='gps')
                utc = Time(utc,format = 'iso')
                utc = Time(utc, out_subfmt='date').iso
                title = title.replace(t, utc)

# scatter plot combined data

plot_comb(all_data, num_events, 1, "FAR")
plot_comb(all_data, num_events, 2, "SNR")
plot_comb(all_data, num_events, 3, "Chirp Mass")
#plot_comb(all_data, num_events, 0, "Signal End Time")

colours = ['b', 'g', 'y']
bins_snr = get_bins(all_data, num_obs, num_events, 2, True)
bins_chisq = get_bins(all_data, num_obs, num_events, 3, True)
snr_data_sets = plot_indiv(all_data, colours, 2, bins_snr, num_obs, num_events, "SNR")
chisq_data_sets = plot_indiv(all_data, colours, 3, bins_chisq, num_obs, num_events, "Chisq")


bins_snr = get_bins(all_data, num_obs, num_events, 2, False)
bins_chisq = get_bins(all_data, num_obs, num_events, 3, False)
snr_data_sets = plot_indiv(all_data, colours, 2, bins_snr, num_obs, num_events, "SNR-no-outliers")
chisq_data_sets = plot_indiv(all_data, colours, 3, bins_chisq, num_obs, num_events, "Chisq-no-outliers")
