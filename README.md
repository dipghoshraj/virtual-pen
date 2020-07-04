# VIRTUAL PEN
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

virtual pen is a computer vision program to track object movement and draw line according the movement.

  - Detecting pen and set colur of drawing
  - Testing the objectdetection
  - Draw your line


#### Building for source
First install all requirement file:
```sh
>> pip install -r requirement.txt
```
- for linux edit requirement.txt and chnage opencv version from 4.2.0.34 to 4.2.0.26 this will run smoothly on the linux and raspberry pi enviroment
 

### Run the drawing code:

Step 1 :  setup pen 
```sh
$ python pensetup.py
```
Step 2 :  correct morphological operations to reduce noise in the video
```sh
$ python max_musk.py
```
Step 3 : Detect and track the colored object with contour detection
```sh
$ python pendecting.py
```
Step 4 : Draw the tracking object
```sh
$ python main.py
```

### Draw Instructions
 - Press button "s" to stop drawing lines 
 - press button "e" for enable ereaser
 - press button "p" to enable pen

### Todos
 - Need to fix a Wirper iuuse

### NOTE :
```
If you are want to use this on the raspberry pi then first setup opencv on raspberry pi 
with open cv version 4.0.2.26 or and never go for leatest if you are not full sure
"A developer don't get tired of error and never take warnings seriously" 
this quote will help you if you are seting up this project on raspberry pi.
```

License
----

MIT


**Free Software, Yeah it's fucking truth!**

Inspiration 
---
https://www.learnopencv.com/creating-a-virtual-pen-and-eraser-with-opencv/
