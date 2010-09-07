#!/usr/bin/env python

"""
Walk through an events XML file and create or update events in Meetup Everywhere.
"""

import sys
import xml.dom.minidom
from httplib import HTTPConnection
import urllib

if len(sys.argv) != 4:
    print("Usage: xmlevents.py <input file> <api key> <urlname>")
    sys.exit(1)

cmd, file, key, urlname = sys.argv

doc = xml.dom.minidom.parse(file)
host = "api.meetup.com"

for node in doc.getElementsByTagName("t_event"):
    text = lambda name: node.getElementsByTagName(name)[0].childNodes[0].data.encode("ISO-8859-1")

    print(text("t_event_id"))
    conn = HTTPConnection(host)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    params = { "urlname" : urlname,
               "zip": text("t_store_zip_code"),
               "address1": text("t_store_address"),
               "venue_name": text("t_event_location"),
               "title": text("t_short_description"),
               "description": text("t_long_description"),
               "organize": "true",
               "udf_t_event_id": text("t_event_id"),
               "key": key }
    conn.request("POST", "/ew/event/", urllib.urlencode(params), headers)
    res = conn.getresponse()
    print res.read()
    assert res.status == 201
