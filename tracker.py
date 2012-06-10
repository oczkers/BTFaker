#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import urllib2
import random
import re

#torrent info
tracker = 'http://tracker.puretna.com:6996'
pass_key = '00499d9deaeb24dd3ffb64ab61641df6'
hash = '5efe5793638c0243c99a292f57b25f7271992e00'
size = 24761542540

speed_min = 20	# KiB/s
speed_max = 450	# KiB/s
speed_min = speed_min * 1024 # KiB -> B
speed_max = speed_max * 1024 # KiB -> B

#torrent client info
user_agent = "uTorrent/2040(21586)"
port = 16800
peer_id = "-UT2040-RT%d0%2f%a1%e5U%e8X%de%1a1"
key = "21CB4DD9"
numwant = 200
additions = "&compact=1&no_peer_id=1"	#numwant = 0 przy zamykaniu sesji !

# DO NOT CHANGE !!
#setting global statements
uploaded = 0
time_start = time.time()
time_current = time_start-1

# convert info_hash
info_hash = ""
for n in range(0, len(hash), 2):
    info_hash += '%%%s' % hash[n:n+2].upper()

def scrape(info_hash=info_hash, pass_key=pass_key):
	if pass_key:
		pass_key = "/%s" %(pass_key)
	return "%s/scrape?info_hash=%s" %(pass_key, info_hash)

def announce(event=None, pass_key=pass_key, info_hash=info_hash, peer_id=peer_id, port=port, uploaded=0, downloaded=0, left=0, corrupt=0, key=key, numwant=numwant, additions=additions):
	#pass key
	if pass_key:
		pass_key = "/%s" %(pass_key)
	#event
	if event:
		full_event = "&event=%s" %(event)
		if event == "stopped":
			numwant = 0
	else:
		full_event = ""
	# build announce
	return '%s/announce?info_hash=%s&peer_id=%s&port=%s&uploaded=%s&downloaded=%s&left=%s&corrupt=%s&key=%s%s&numwant=%s%s' %(pass_key, info_hash, peer_id, str(port), str(uploaded), str(downloaded), str(left), str(corrupt), key, full_event, str(numwant), additions)

def header():
	return {"User-Agent":user_agent, "Accept-Encoding":"gzip"}

#get www page
def get(target, values=None, header=header()):
	req = urllib2.Request(target, values, header)
	return opener.open(req).read()


# 		WORK !
opener = urllib2.build_opener()
#start
n = 1
#get(tracker+scrape(info_hash))	#only once per torrent (new seed/peer)!
response = get('%s%s' %(tracker, announce("started")))
interval = re.search(".*?intervali(.*?)e12.*?", response).group(1)
print '''	>>> Start !\n
User-Agent: %s
Client port: 
Tracker adres: 
Interval: %s min.''' %(user_agent, str(port), tracker[7:], str(int(interval)/60))
while True:
	if "off" in open("tracker.ini", "r").read():	sys.exit()	# close connection if 'off' found in tracker.ini
	time.sleep(int(interval))
	uploaded = int(uploaded + (time.time()-time_current)*random.randint(speed_min, speed_max))
	print '%s.	Uploaded: %s MiB (%s KiB/s)' %(str(n), str(uploaded/1024/1024), str(int(uploaded/1024/(time_current-time_start))))
	response = get('%s%s' %(tracker, announce(uploaded=uploaded)))
	time_current = time.time()
	n = n+1
#dodaj upload, zamknij sesje (event-stopped) - tylko po co skoro sama wygasnie ;-) ?
time.sleep(int(interval))
