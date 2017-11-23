#!/usr/bin/python

import numpy as np
import cv2
import sys
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

# global variables
cursor_index = 0
images = list()
count = 0
fig = 0

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
	while success:
		images.append((count, image))
		# cv2.imwrite(os.path.join(video_name, "frame%d.jpg" % count), image)     # save frame as JPEG file
		count += 1
		success,image = vidcap.read()

	print("finished reading %d frames" %count)

# -----------------------------------------------------------------------------
def navigate_frames():
	global fig
	fig = plt.figure()
	fig.canvas.mpl_connect('key_press_event', key_event)
	plt.subplot(111)
	plt.imshow(images[0][1])
	plt.gca().axes.get_xaxis().set_visible(False)
	plt.gca().axes.get_yaxis().set_visible(False)
	plt.show()

# -----------------------------------------------------------------------------
def key_event(e):
	global cursor_index
	global fig

	if e.key == "right":
		cursor_index = cursor_index + 1
	elif e.key == "left":
		cursor_index = cursor_index - 1
	else:
		return
	cursor_index = cursor_index % count

	plt.cla()
	plt.imshow(images[cursor_index][1])
	fig.canvas.draw()


# main function
# -----------------------------------------------------------------------------
def main():
	if len(sys.argv) == 2:
		video_path = sys.argv[1]
		if not os.path.isfile(video_path):
			print("Wrong number of arguments")
			print("Use: python3 task.py <video> <timestamp.csv> <events_id.csv>")
			return
		process(video_path)
		navigate_frames()

if __name__ == '__main__':
	main()