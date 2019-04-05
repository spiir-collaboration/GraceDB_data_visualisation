import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

filename = "log_events"

title = "_Playground_2019-03-19_gstlal_MBTAOnline_1135697336-1135765736"
xlabel = "_sngl_inspiral_ifo_snr"

if xlabel == "_coinc_inspiral_snr":
        data_list = []
        with open(filename,"r") as f:
                for line in f:
                        if line!='\n':
                                data_list.append(float(line[:-1]))

        data_array = np.array(data_list)
        print(type(data_array))


        plt.hist(data_array)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.savefig("histogram"+str(title)+str(xlabel)+".png")

if xlabel == "_sngl_inspiral_ifo_snr":
        data_list = []
	det_list = []
        with open(filename,"r") as f:
                for line in f:
                        if line!='\n':
                                split_line = line.split(',')
                                data_list.append(float(split_line[1][:-1]))
				det_list.append(split_line[0])
	
	min_data = min(data_list)
	max_data = max(data_list)
	num_bin = 10
	bin_width = (max_data - min_data)/num_bin

	plt.hist(data_list, bins = np.arange(min_data, max_data + bin_width, bin_width), fill = False, label = 'All') 
	plt.title(title) 
	plt.xlabel(xlabel) 

	H1 = []
	L1 = []
	V1 = []
	for idx in range(len(det_list)):
		if det_list[idx] == 'H1':
			H1.append(data_list[idx])
		elif det_list[idx] == 'L1':
			L1.append(data_list[idx])
		elif det_list[idx] == 'V1':
			V1.append(data_list[idx])
	
	if H1 != []:
		plt.hist(H1, bins = np.arange(min_data, max_data + bin_width, bin_width), alpha = 0.5, color = 'b', label = 'H1')
	if L1 != []:
		plt.hist(L1, bins = np.arange(min_data, max_data + bin_width, bin_width), alpha = 0.5, color = 'k', label = 'L1')
	if V1 != []:
		plt.hist(V1, bins = np.arange(min_data, max_data + bin_width, bin_width), alpha = 0.5, color = 'y', label = 'V1')
	plt.legend(loc = 'upper center')
	plt.savefig("histogram"+str(title)+str(xlabel)+".png")
