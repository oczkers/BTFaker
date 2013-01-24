#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import random
import re
import requests

#torrent info
tracker_url = 'http://bt.pornolab.net'
pass_key = 'OydDvfRA1p'
hash = '6E2ABE1AD27148A0685F7A6D7717D5AC2603D482'

speed_min = 1024	# KiB/s
speed_max = 5120	# KiB/s
speed_min = speed_min * 1024 # KiB -> B
speed_max = speed_max * 1024 # KiB -> B

#torrent client info
user_agent = "uTorrent/2210(25273)"
port = 16800
peer_id = "-UT2210-%b9b%e4%c4%d0%aa%84LT%08%f7v"
key = "7C34F748"
numwant = 200

# DO NOT CHANGE !!
#setting global statements
uploaded = 0
time_start = time.time()
time_current = time_start-1

# convert info_hash
info_hash = ""
for n in range(0, len(hash), 2):
    info_hash += '%%%s' %(hash[n:n+2].upper())

def scrape(info_hash=info_hash, pass_key=pass_key):
	if pass_key:
		pass_key = "/%s" %(pass_key)
	return "%s/scrape?info_hash=%s" %(pass_key, info_hash)

def announce(event=None, pass_key=pass_key, info_hash=info_hash, peer_id=peer_id, port=port, uploaded=0, downloaded=0, left=0, corrupt=0, key=key, numwant=numwant):
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
	return '%s/announce?info_hash=%s&peer_id=%s&port=%s&uploaded=%s&downloaded=%s&left=%s&corrupt=%s&key=%s%s&numwant=%s&compact=1&no_peer_id=1' %(pass_key, info_hash, peer_id, str(port), str(uploaded), str(downloaded), str(left), str(corrupt), key, full_event, str(numwant))

def ann(event=None, pass_key=pass_key, info_hash=info_hash, peer_id=peer_id, port=port, uploaded=0, downloaded=0, left=0, corrupt=0, key=key, numwant=numwant):
	#event
	if event:
		full_event = "&event=%s" %(event)
		if event == "stopped":
			numwant = 0
	else:
		full_event = ""
	# build announce
	return '/ann?uk=%s&info_hash=%s&peer_id=%s&port=%s&uploaded=%s&downloaded=%s&left=%s&corrupt=%s&key=%s%s&numwant=%s&compact=1&no_peer_id=1' %(pass_key, info_hash, peer_id, str(port), str(uploaded), str(downloaded), str(left), str(corrupt), key, full_event, str(numwant))

# 		WORK !
headers = {"User-Agent":user_agent, "Accept-Encoding":"gzip"}
utorrent = requests.session(headers=headers)
#start
n = 1
#utorrent.get(tracker_url+scrape(info_hash))	#only once per torrent (new seed/peer)!
#response = utorrent.get('%s%s' %(tracker_url, announce("started"))).content
response = utorrent.get('%s%s' %(tracker_url, ann("started"))).content
open('log.log', 'w').write(response)	#log
interval = re.search(".*?intervali(.*?)e12.*?", response).group(1)
print '''	>>> Start !\n
User-Agent: %s
Client port: %s
Tracker adres: %s
Interval: %s min.''' %(user_agent, str(port), tracker_url[7:], str(int(interval)/60))
while True:
	#if "off" in open("tracker.ini", "r").read():	sys.exit()	# close connection if 'off' found in tracker.ini
	try:		time.sleep(int(interval))
	except:		break
	uploaded = int(uploaded + (time.time()-time_current)*random.randint(speed_min, speed_max))
	print '%s.	Uploaded: %s MiB (%s KiB/s)' %(str(n), str(uploaded/1024/1024), str(int(uploaded/1024/(time_current-time_start))))
	#response = utorrent.get('%s%s' %(tracker_url, announce(uploaded=uploaded))).content
	#utorrent.get('%s%s' %(tracker_url, announce(uploaded=uploaded)))	# no need to get response
	response = utorrent.get('%s%s' %(tracker_url, ann(uploaded=uploaded))).content	# no need to get response
	open('log.log', 'w').write(response)	#log
	time_current = time.time()
	n = n+1
#dodaj upload, zamknij sesje (event-stopped) - tylko po co skoro sama wygasnie ;-) ?
time.sleep(int(interval))
