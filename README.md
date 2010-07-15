MEETUP API UTILITIES
----------------------------------

#### importMap.sh ####
Usage: <command> 'mapurl' 'meetupurlname' 'time' 'key'
     Where 'mapurl' is the google map url (EXAMPLE: "http://maps.google.com/maps/ms?ie=ISO-8859-1&oe=ISO-8859-1&hl=en&msa=0&output=georss&msid=116968845691849104850.00048835577f696c2984d")
     Where 'meetupurlname' is the name of the meetup everywhere container you will be adding events to
     Where 'time' is the time to set all the events to be at (IN MILLISECONDS)
     Where 'key' is your Meetup API Developer key
   
For questions, contact jake@meetup.com
######################

#### googlemapimport.java ####

usage:  javac goolgemapimport.java (to compile)
	java googlemapimport (to run)

	where 'urlname' is the the name of the everywhere container (example: "TechCrunch" refers to "http://www.meetup.com/TechCrunch/")
	where 'apikey' is your unique api key which can be found at "http://www.meetup.com/meetup_api/key/"
	where 'google map rss url' is the google map url (example: "http://maps.google.com/maps/ms?ie=ISO-8859-1&oe=ISO-8859-1&hl=en&msa=0&output=georss&msid=116968845691849104850.00048835577f696c2984d")
	where 'time' is the event time which is given in milliseconds since the epoch. to get the number use the date command on the command line (example: 'date +%s -d "Tue Jul 21 04:23:56 EDT 2010"')

For questions, contat michael@meetup.com
##############################