rm log_events
fnames=`ls|grep xml`
for one_file in $fnames
do
	ligolw_print -t coinc_inspiral -c end_time -c ifos -c combined_far -c snr -c mchirp $one_file >> log_events
	#ligolw_print -t coinc_inspiral -c snr $one_file >> log_events
	#ligolw_print -t coinc_inspiral -c combined_far $one_file >> log_events

	ligolw_print -t sngl_inspiral -c end_time -c ifo -c snr -c chisq $one_file >> log_events
	#ligolw_print -t sngl_inspiral -c ifo -c far $one_file >> log_events
	echo "" >> log_events
done
