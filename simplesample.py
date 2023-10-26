#!/usr/bin/env python
# encoding: utf-8
"""
simplesample.py

This sample illustrates basic functionality of locating an AcqKnowledge
server, and starting to acquire data.

Copyright (c) 2009-2010 BIOPAC Systems, Inc. All rights reserved.

Updated to Python3 and modified by Preston Leigh @ the University of Arizona SensorLab.
"""

# import standard Python modules

import sys
import os
import time
import signal

# import our biopacndt support module

import biopacndt

# variables
channelnum = 0 # int deciding which channel to obtain data from 

# create a function to handle Ctrl+C and other exceptions
def signal_handler(sig, frame):
	print("Signal received. Exiting gracefully...")
	global server
	try:
		server.toggleAcquisition()
		server.Stop()  # Attempt to close the serial port
	except Exception as e:
		print(f"Error while closing the serial port: {e}")

	sys.exit(0)

def main():	
	""" Execute the simplesample.py example Python code.  
	
	This locates a server, sends it a template, and starts data acquisition 
	remotely.
	"""
	
	# First we must locate an AcqKnowledge server, a computer that is
	# running AcqKnowledge with the networking feature and that is set
	# to respond to autodiscovery requests.
	#
	# We will use the "quick connect" function which locates the
	# first available AcqKnowledge on the network and returns an
	# AcqNdtServer object for it.
	
	server = biopacndt.AcqNdtQuickConnect()
	if not server:
		print("No AcqKnowledge servers found!")
		sys.exit()
	
	signal.signal(signal.SIGINT, signal_handler)

	# Check if there is a data acquisition that is already running.
	# In order to acquire data into a new template, we need to halt
	# any previously running acquisition first.
	
	if server.getAcquisitionInProgress():
		server.toggleAcquisition()
		print("Current data acquistion stopped\n")

	# gives list of all active channels, each element is a dictionary with type, channel index, etc.
	channels = server.GetAllChannels()

	# converts a dictionary for a channel into a struct that can be passed into commands
	channelstruct = channels[channelnum].GetSimpleChannelStruct()

	# prints out what measurement is being taken on sensor, x or y, and what bionomadix reciever it is using
	print(f"First channel name: {server.GetChannelLabel(channelnum[0])}\n")

	# turns on sample acquiring if not already on
	if not server.getMostRecentSampleValueDeliveryEnabled(channelstruct):
		server.changeMostRecentSampleValueDeliveryEnabled(channelstruct, True)
	
	# Start data acquisition.
	server.toggleAcquisition()
	
	# Wait a second and then check if we started the acquisition successfully.
	time.sleep(1)

	if server.getAcquisitionInProgress():
		print("Acquisiton started successfully. Check AcqKnowledge to ensure an acquisition is in progress.")

		while True:
			time.sleep(0.5)
				
			if server.getAcquisitionInProgress():
				print(server.getMostRecentSampleValue(channelstruct))

			else:
				print("ERROR: the acquisition stopped!")
				break

	else:
		print("ERROR: the acquisition did not start!")

	server.toggleAcquisition()
	server.Stop()
		
if __name__ == '__main__':
	main()

