#!/usr/bin/python

import numpy as np
import cv2
import sys
import os
import time

# global variables
images = list()
count = 0

# function responsible for processing the video
# -----------------------------------------------------------------------------
def process(video_path):#, timestamp, events_id):
	# variables initialization
	success = True
	global count
	# creating directory for new images
	video_name = os.path.basename(os.path.splitext(video_path)[0])
	print(video_name)
	if not os.path.isdir(video_name):
		os.mkdir(video_name)
	vidcap = cv2.VideoCapture(video_path)
	success,image = vidcap.read()
	
	# saving video frames into images list
	f_timestamps = open(video_name + "_timestamps.csv", 'w')
	f_eventsid = open(video_name + "_eventid.csv", 'w')
	print("start generating csv files")
	while success:
		images.append((count, image))
		t = time.time()
		f_timestamps.write(str(t) + '\n')
		f_eventsid.write(str(t) + ",event_id_" + str(int(count/20)) + '\n')
		f_eventsid.write(str(time.time()) + ",event_id_" + '123456' + '\n')
		# cv2.imwrite(os.path.join(video_name, "frame%d.jpg" % count), image)     # save frame as JPEG file
		count += 1
		success,image = vidcap.read()
	f_timestamps.close()
	f_eventsid.close()

	print("finished reading %d frames" %count)


# main function
# -----------------------------------------------------------------------------
def main():
	if len(sys.argv) == 2:
		video_path = sys.argv[1]
		if not os.path.isfile(video_path):
			print("Wrong number of arguments")
			print("Use: python3 generate_csv.py <video>")
			return
		process(video_path)

if __name__ == '__main__':
	main()