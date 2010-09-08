#!/usr/bin/env python

"""
Walk through an events XML file and create or update events in Meetup Everywhere.
"""

import sys, os, time
import xml.dom.minidom
from httplib import HTTPConnection
import urllib
from datetime import datetime, timedelta

if len(sys.argv) != 4:
    print("Usage: xmlevents.py <input file> <api key> <urlname>")
    sys.exit(1)

cmd, file, key, urlname = sys.argv

doc = xml.dom.minidom.parse(file)
host = "api.meetup.com"
os.environ['TZ']='UTC'
time.tzset()
now = datetime.now() + timedelta(hours=1)

for node in doc.getElementsByTagName("t_event"):
    def text(name):
        elems = node.getElementsByTagName(name)
        if elems and elems[0].childNodes:
            return elems[0].childNodes[0].data.encode("ISO-8859-1")
        else: return None

    t_event_id = text("t_event_id")
    print(t_event_id)

    try: dt = datetime.strptime(text("t_event_date").rstrip("0")[:-1], '%Y-%m-%d %H:%M:%S')
    except: dt = None
    if dt == None:
        print "bad time format: %s" % text("t_event_date")
    elif dt < now:
        print "skipping past event"
    else:
        endpoint = "/ew/event"
        conn = HTTPConnection(host)
        conn.request("GET", "/ew/events.xml?" + urllib.urlencode({
            "urlname" : urlname,
            "udf_t_event_id": t_event_id,
            "key": key}))
        res = conn.getresponse()
        assert res.status == 200
        resdoc = xml.dom.minidom.parseString(res.read())
        for item in resdoc.getElementsByTagName("item")[:1]:
            for id_node in [ch for ch in item.childNodes if ch.tagName.lower() == "id"][:1]:
                endpoint = "%s/%s" % (endpoint, id_node.childNodes[0].data)
        
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        first, last, ld = map(text, ("t_author_first_name", "t_author_last_name", "t_long_description"))
        desc = "Featuring %s %s\n\n%s" % (first, last, ld) if first and last else ld
        params = { "urlname" : urlname,
                   "local_time": int(time.mktime(dt.timetuple())) * 1000,
                   "zip": text("t_store_zip_code"),
                   "address1": text("t_store_address"),
                   "venue_name": text("t_event_location"),
                   "title": text("t_short_description"),
                   "description": desc,
                   "organize": "true",
                   "udf_t_event_id": t_event_id,
                   "key": key }
        conn.request("POST", endpoint, urllib.urlencode(params), headers)
        res = conn.getresponse()
        print res.read()
        assert res.status in [200,201] 
