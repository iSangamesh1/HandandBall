import cv2 as cv
import numpy as np 
from cvzone.HandTrackingModule import HandDetector #track our hands
import cvzone #to overlay and images on top of each other

cap = cv.VideoCapture(0) 
# this code is needed to open our webcam
# captcha object created
# camera index 0 means the very next i.e. in this my laptop case its my laptop's web cam

hd = HandDetector(detectionCon=0.7)
# initialize the hand detector
# then the parameter as quantitation confidence so that we can say detection confidence is 0.7 i.e. it should only detail something as hand if it's 70% sure that's a hand 

width, height = 640, 480
# width and heigh of the screen

cap.set(3, width)
cap.set(4,height )
# setting the resolution for our webcam


ball = cv.imread('cricball3.png', cv.IMREAD_UNCHANGED)
bat = cv.imread('bat2.png', cv.IMREAD_UNCHANGED)
gameover = cv.imread('gameover.png', cv.IMREAD_UNCHANGED)

ball = cv.resize(ball, (40, 40))
bat = cv.resize(bat, (120, 26))
gameover = cv.resize(gameover, (width,height))
# variable_name = cv.resize(variable_read_name, size(width, height))
# to resize the variable according to our need
# the calculationsare done manually we need to change it according our needs 

# default position of ball
# x-axis & y-axis
position = [50, 50]

# speed on x-direction
speedx = 5
# speed on y-direction
speedy = 5

score = 0

while True:
#as we are taking the video feed and we are takin it in a loop so while tru
    ret, img = cap.read()
    # ret - it is a boolean that shows there is video or not, so in the absence of video feed it gives you zero under the video feed and you get one from it so we are just reading our video here which we are storing in the image variable so that's what we need.

    # now we are going to put the rectangle around it define it playing area
    cv.rectangle(img, (0, 480), (640, 0), (0, 0, 255), 8)
    # starting pt, ending pt, color(red), thickness
    # the starting point is bottom left corner and the ending point is top right corner
    cv.rectangle(img, (0, 440), (640, 480), (0, 255, 255), 6)

    hands, img = hd.findHands(img, flipType=True) 
    # we are passing 'img' image which will find the hand image
    # this we return us with image and the Hand incase the hand is found 

    if hands: 
        # if there is hand then we can go for bounding box value
        bbox = hands[0]['bbox']
        # bbox will be equal to our hands at index zero and key of bbox, due to this we will be able to get the box around our hand
        # the values will be stored in bbox
        x, y, w, h = bbox
        print(bbox)
        # unpack the values in different varaibles
        # as it is automatically unpacked

        h1, w1, c = bat.shape
        # here we have taken the height, width and channel of bat  
        
        # now we will be subtracting the width of bat shape from the bounding box so we'll start that one in x1
        x1 = x-h1//2
        # x axis here is not width
        # x1 is the point at the middle of the bat that is connected to center of hand
        # x1 = 

        # we will put the part in the position we want
        # we need to overlay out image

        x1 = np.clip(x1, 5, 510)
        # as my bat is going at extreme left and end the game's window is getting closed and error is occuring so to resolve that we are using clipping function
        # cliping function taking the parameters (the element p, left wall , right wall)

        img = cvzone.overlayPNG(img, bat, [x1, 447])
        # cvzone.overlayPNG takes 3 parameters i.e. (imageback(i.e. webcam image), imagefront(i.e. bat), positions we will take it in list[])

        # now here we are going to make the ball move in the bounding box




        if position[1] < 50:
            speedy = -speedy
            position[0] -= 10
            # position -= 10 increase the speed and the ball will move faster in down direction

        # for ball hitting the bat 
        if x1-10 < position[0] < x1 + w1 and 380 < position[1] < 380+h1:
            # here we have the condition that we are checking at x-axis and y-axis as well 
            # x1-10
            speedy = -speedy
            position[0] += 30
            score += 1
        # gameover condition
    if position[1] > 400:
            # it means that if the center of ball is having value more than 400 on y-axis i.e it has surpass the bat and it has not hit the surface of bat
        img = gameover
        cvzone.putTextRect(gameover, 'Final Score -> ' + str(score), [300, 190], 1.9, 2, colorR=(0, 0, 0))
        cvzone.putTextRect(gameover, 'Press R to restart', [290, 305], 1.80, 2, colorR=(0, 0, 0))
        cvzone.putTextRect(gameover, 'Press Esc to Quit', [290, 345], 1.80, 2, colorR=(0, 0, 0))

    else:
        if position[0] >= 560 or position[0] <= 20: 
            # as the width of screen in 640 and we know that postion of ball boundary touches the screen  
            speedx = -speedx

        # now putting the ball in motion
        position[0] += speedx
        position[1] += speedy

    # for displaying the score
    cvzone.putTextRect(img, 'Score '+str(score), [270, 30], 1.5)

    img = cvzone.overlayPNG(img, ball, position)

    # this is just for checking purpose how ball is moving
    # position[0] += speedx    
    # position[1] += speedy  
      
    # now we need check that the balls hitting the wall i.e. left, top and bottom it should be rebounced 
    # so for that if the ball is having the distance less than 50 from the wall then
    # let us take top wall first

    cv.imshow('frame', img)
    # cv.imshow function we are passing 'frame' as frame name to the image
    key = cv.waitKey(1)  
    # here we are waiting 1 second we are taking image

    # when gaveover image will be displayed everything will be stopped but we don't want that we want our game should be continued so for that
    if key == ord('r') or key == ord('R'):
        # when r is pressed then we want to restart everything like position , speed etc..
        position = [50, 50]
        speedx = 10
        speedy = 10
        score = 0
        gameover = cv.resize(gameover, (width,height))

    else:
        if key == 27:
            # 27 is for Esc
            break