ECAD Data Processor

The European Climat Assessment & Dataset provides many weather data in good quality. 
Sadly they offer no API. Therefore manual download is necessary from
 ---> https://www.ecad.eu/dailydata/predefinedseries.php
(Please download not only the feature zip, but also the station.txt.)

This script automates the processing of the downloaded zip files. 

It requires inputs for
- downloaded features (to be processed) like tn, tx, rr etc.
- list of countries for which this features should be processed.
- start date for the periode for which this features should be processed.

The sript works with a folder path: /data/ECAD/ecad_downloads

Outputs are processed data files as well as station files 
for given features, saved as csv file.

The script was created druing the 'Final Project' (module 10)
of WBS Coding School, Data Science Bootcamp #023
by Kaiko.

The script does not give a sampmle solution. It makes no claim on accuracy.

contact via https://www.linkedin.com/in/kaiko304 
