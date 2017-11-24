# BMW_task

This module is a sequence of video frame handeling functionalities for a specific task.

## Task

A Python program that processes large video files, in both MJPG and H264 encodings, for which two annotation files exist:

* time.csv: Contains the timestamps in unix format for each frame of the video
* events.csv: Contains events (timestamp in unix format, eventID) for specific timestamps that may or may not overlap with the video

The program should be able to do the following:

* Load each video frame as a numpy array.
* Display the frame on screen (using matplotlib or PyQt5).
* Navigate through the frames using the cursor keys.
* Find the events from events.csv that apply to each frame.
* Create an overlay over the video frame displaying the eventId.
* Encode a video with the eventId overlays.

## Usage

* Generate dummy timestamp and events_id csv files to be used later for video processing:

```
$ python3 generate_csv.py <video>
```

* Run the video processing script. It is assumed that the timestamps are equal to the number of frames of the video:

```
$ python3 task.py <video> <timestamp.csv> <events_id.csv>
```

* Check the encoded output video file in H264 format:

```
encoded_video.mp4
```


### Program sequence

1. Run the task.py script with the right parameter.
2. A window displaying video frames appears and can be navigated using left and right video keys.
3. Turn of the window to continue the script.
4. A window displaying video frames after adding events ids appears and can be navigated using left and right video keys.
5. Turn of the window to continue the script.
6. The video is being encoded in H264 format and saved. Check encoded_video.mp4 for final output.

## General implementation comments
* Images are saved in a list of tuple (timestamp, image frame).
* Events ID are saved in a dictionary in the format {timestamp: eventID}.
* The program handels unrelevant event id timestamps by excluding them.


## Authors

* **Mohamed AbouHussein** - *abouhussein.mohamed@gmail.com* 