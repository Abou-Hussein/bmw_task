#!/usr/bin/python
"""This module is a sequence of video frame handeling functionalities for a specific task."""

import os
import sys
import csv
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib as mpl

# global variables
cursor_index = 0
images = list()
timestamp_list = list()
events_id_dict = dict()
count = 0
fps = 0
fig = 0 # figure object for veiwing frames and navigation

# function that handels csv data supported
# -----------------------------------------------------------------------------
def process_csv(timestamps_path, events_id_path):
    # save timestamps in a list
    with open(timestamps_path) as f:
        for row in f:
            timestamp_list.append(row.strip())
    # save timestamps: event_ids in a dictionary for fast retrieval
    with open(events_id_path) as f:
        read_file = csv.reader(f, delimiter=',')
        for row in read_file:
            events_id_dict[row[0]] = row[1]


# function responsible for processing the video and extracting the frames
# -----------------------------------------------------------------------------
def process_video(video_path):#, timestamp, events_id):
    # variables initialization
    global count
    global fps
    success = True
    # creating directory for new images
    video_name = os.path.basename(os.path.splitext(video_path)[0])
    print("Start processing: " + video_name)
    if not os.path.isdir(video_name):
        os.mkdir(video_name)
    # initialize captured video and retrieve the frames per second for the video
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read() # images are numpy.ndarray

    # saving video frames into images list
    while success:
        images.append((timestamp_list[count], image))
        # save frame as JPEG file, uncomment if needed
        # cv2.imwrite(os.path.join(video_name, "frame%d.jpg" % count), image)
        count += 1
        success, image = vidcap.read()

    print("finished reading %d frames" %count)

# adds events id to the relevant frame timestamp
# -----------------------------------------------------------------------------
def add_event_id():
    height, width, layers = images[0][1].shape
    for timestamp, image in images:
        if timestamp in events_id_dict:
            cv2.putText(img=image, text=events_id_dict.get(timestamp), org=(int(0.65*width),
                int(0.9*height)), fontFace=4, fontScale=0.5, color=(0, 0, 255), thickness=1)

# generates encoded video with frames events id added
# -----------------------------------------------------------------------------
def generate_video():
    print("\nStarting video encoding with new frame ID")
    height, width, layers = images[0][1].shape
    encoded_video = 'encoded_video.mp4'
    if os.path.isfile(encoded_video):
        os.remove(encoded_video)
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    video = cv2.VideoWriter(encoded_video, fourcc, fps, (width, height))
    for timestamp, image in images:
        video.write(image)
    cv2.destroyAllWindows()
    video.release()
    print("Video generated. Check encoded_video.mp4")


# function responsible for displaying and navigating the frames
# -----------------------------------------------------------------------------
def navigate_frames():
    print('Start image viewer .. navigate using left and right keyboard keys')
    global fig
    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', key_event)
    plt.subplot(111)
    plt.imshow(images[0][1])
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.show()

# key event handler for navigating the frames with the left and right
# keyboard cursor buttons
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
    if len(sys.argv) == 4:
        video_path = sys.argv[1]
        timestamps_path = sys.argv[2]
        events_id_path = sys.argv[3]
        if not os.path.isfile(video_path):
            print("Wrong number of arguments")
            print("Use: python3 task.py <video> <timestamp.csv> <events_id.csv>")
            return
        process_csv(timestamps_path, events_id_path)
        process_video(video_path)
        navigate_frames()
        add_event_id()
        navigate_frames()
        generate_video()

if __name__ == '__main__':
    main()
