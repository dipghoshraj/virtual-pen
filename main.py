import cv2
import numpy as np
import time
import keyboard

load_from_disk = True
if load_from_disk:
    penval = np.load('penval.npy')

cap = cv2.VideoCapture(0)

# Load these 2 images and resize them to the same size.
pen_img = cv2.resize(cv2.imread('pen.png', 1), (50, 50))
eraser_img = cv2.resize(cv2.imread('eraser.png', 1), (50, 50))
no_pen_ing = cv2.resize(cv2.imread('nopen.png', 1), (50, 50))

kernel = np.ones((5, 5), np.uint8)

# Making window size adjustable
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# This is the canvas on which we will draw upon
canvas = None

# Create a background subtractor Object
backgroundobject = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

# This threshold determines the amount of disruption in the background.
background_threshold = 600

# A variable which tells you if you're using a pen or an eraser.
switch = 'Pen'

# With this variable we will monitor the time between previous switch.
last_switch = time.time()

# Initilize x1,y1 points
x1, y1 = 0, 0

# Threshold for noise
noiseth = 800

# Threshold for wiper, the size of the contour must be bigger than this for # us to clear the canvas
wiper_thresh = 40000

# A variable which tells when to clear canvas
clear = False

while (1):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Initilize the canvas as a black image
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Take the top left of the frame and apply the background subtractor
    # there
    top_left = frame[0:50, 0:50]
    fgmask = backgroundobject.apply(top_left)

    # Note the number of pixels that are white, this is the level of
    # disruption.
    switch_thresh = np.sum(fgmask == 255)

    # If the disruption is greater than background threshold and there has
    # been some time after the previous switch then you. can change the
    # object type.
    #if switch_thresh>background_threshold and (time.time()-last_switch) > 1:

    # if keyboard.is_pressed('e'):
    #     # Save the time of the switch.
    #     last_switch = time.time()

    #     if switch == 'Pen':
    #         switch = 'Eraser'
    #     else:
    #         switch = 'Pen'

    if keyboard.is_pressed('e'):
        switch = 'Eraser'

    if keyboard.is_pressed('s'):
        switch = 'stop'

    if keyboard.is_pressed('p'):
        switch = 'Pen'

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # If you're reading from memory then load the upper and lower ranges
    # from there
    if load_from_disk:
        lower_range = penval[0]
        upper_range = penval[1]

    # Otherwise define your own custom values for upper and lower range.
    else:
        lower_range = np.array([26, 80, 147])
        upper_range = np.array([81, 255, 255])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Perform morphological operations to get rid of the noise
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # Make sure there is a contour present and also it size is bigger than
    # noise threshold.
    if contours and cv2.contourArea(max(contours,
                                        key=cv2.contourArea)) > noiseth:

        c = max(contours, key=cv2.contourArea)
        x2, y2, w, h = cv2.boundingRect(c)

        # Get the area of the contour
        area = cv2.contourArea(c)

        # If there were no previous points then save the detected x2,y2
        # coordinates as x1,y1.
        if x1 == 0 and y1 == 0:
            x1, y1 = x2, y2

        else:
            if switch == 'Pen':
                # Draw the line on the canvas
                canvas = cv2.line(canvas, (x1, y1), (x2, y2), [255, 0, 0], 5)

            if switch == "stop":
                pass

            if switch == "Eraser":
                cv2.circle(canvas, (x2, y2), 20, (0, 0, 0), -1)

        # After the line is drawn the new points become the previous points.
        x1, y1 = x2, y2

        # Now if the area is greater than the wiper threshold then set the
        # clear variable to True
        if area > wiper_thresh:
            cv2.putText(canvas, 'Clearing Canvas', (0, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1,
                        cv2.LINE_AA)
            clear = True

    else:
        # If there were no contours detected then make x1,y1 = 0
        x1, y1 = 0, 0

    # Now this piece of code is just for smooth drawing. (Optional)
    _, mask = cv2.threshold(cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY), 20, 255,
                            cv2.THRESH_BINARY)
    foreground = cv2.bitwise_and(canvas, canvas, mask=mask)
    background = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
    frame = cv2.add(foreground, background)

    # Switch the images depending upon what we're using, pen or eraser.
    if switch == 'Eraser':
        cv2.circle(frame, (x1, y1), 20, (255, 255, 255), -1)
        frame[0:50, 0:50] = eraser_img

    if switch == "stop":
        # no_pen_ing
        frame[0:50, 0:50] = no_pen_ing

    if switch == "Pen":
        frame[0:50, 0:50] = pen_img

    cv2.imshow('image', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    # Clear the canvas after 1 second, if the clear variable is true
    if clear == True:
        time.sleep(1)
        canvas = None

        # And then set clear to false
        clear = False

cv2.destroyAllWindows()
cap.release()