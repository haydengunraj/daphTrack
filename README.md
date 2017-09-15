# daphTrack

A simple thresholding and contour finding program I used for identifying and tracking daphnia and copepods in videos. The videos in the img folder are ones I took myself, and the additional markings added by the code are shown in the output folder. The multi\_tracking file tracks multiple objects given HSV thresholds and contour size bounds (see output/copepods\_resized.avi), while the single\_tracking file does the same thing except for a single object and with the option to draw a trail behind the object (see output/trail\_tiny\_daphnia.avi).

![SbSComp](https://github.com/haydengunraj/daphTrack/blob/master/output/side_by_side.JPG "Side-by-side comparison")

Notably, the videos in the output folder are resized to meet GitHub maximum file size requirements, and so the picture quality is lower than usual. All videos and their corresponding outputs can be found here in their original quality: https://www.dropbox.com/sh/m4zcdxxtna5e8ql/AADDuuqyNqDyJvgGp4dEO86Oa?dl=0.

In terms of equipment, I used a compound light microscope with a digital imager to take video, as well as a digital camera on macro settings. The copeopods and daphnia were collected from the Dufferin Marsh in Schomberg, ON.

### Dependencies

- [Python 2.7](https://www.python.org/downloads/)
- [Numpy](http://www.numpy.org/)
- [OpenCV](http://opencv.org/)
