# Data-Sonification
A study project: data sonification tool based on Pyo library and Flask web framework. Works without using MIDI for the sake of more precise sonification.
In this context the data means, specifically, time series, e.g. exchange rates or daily temperature.
At this point the service doesn't deployed anywhere. I'm going to do some experiments with task queues and then deploy it on one of the cloud platforms 
(except for Heroku: there is issues with Pyo import during the deploy on Heroku).

The service takes user's excel (*.xls, *.xlsx), or *.csv file, parses it and maps certain frequencies to the values in the user's data.
Also user has to set up sample duration (from 10 to 999 sec). Then, this array of frequencies proceeds to oscillators.
An output is a *.wav file which user is prompted to save or open.

Common restrictions:
•	maximum number of the time series to sonify is three ;
•	each one can contain maximum 300 points (values); 
•	only valid data format is integers or floating point numbers.
•	no other data except for that which should be sonified is allowed (e.g. column headers of row names).

Excel restrictions: 
•	the data should be placed on the first sheet 
•	the data should be placed in the first three columns (depending on the quantity of the series), each of the columns represents one of the time series.

CSV restrictions: 
•	all of the values should be quoted for correct parsing; 
•	the data should be placed in the first three columns (depending on the quantity of the series), each of the columns represents one of the time series;
•	the number of values in each of time series should be equal;
•	if the time series has gaps or ends earlier than others, empty quotes must be in place of missing values.
