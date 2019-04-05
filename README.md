# GraceDB_data_visualisation
Visualising data (plots and tables) from the gravitational wave database GraceDB, broken into catagories based on detectors, pipelines and specific data types

1. Open "get_events.py" and change to desired search range in in 'event_type' variable and change to desired database in 'main_database' variable
2. Run "get_events.py"
3. [Not recommended] Open "print_events.sh" and change print statements to print the desired variables (though this will mean "make_histogram.py" may also need changing, as not all options are accounted for at this stage)
4. Run "print_events.sh"
5. [Not recommended] Open "make_histogram.py" and add functionality for any printed variables not accounted for from step 3
6. Run "make_histogram.py"
