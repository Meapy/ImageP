import cv2
import numpy as np
import easygui
import os

# Load the image
f = easygui.fileopenbox(filetypes=["*.jpg","*.jpeg","*.png"])
img = cv2.imread(f)

#smooth the image
img = cv2.GaussianBlur(img, (1,1), 0)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create a binary mask from the image using edge detection
ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
#create a function to remove small white pixels from the image
def remove_small_white_pixels(img, size):
    # find the contours of the image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # create a copy of the image
    img_copy = img.copy()
    # for each contour
    for cnt in contours:
        # if the contour is smaller than the size, remove it
        if cv2.contourArea(cnt) < size:
            cv2.drawContours(img_copy, [cnt], 0, (0, 0, 0), -1)
    # return the image
    return img_copy

thresh = remove_small_white_pixels(thresh, 100)

#count how many black pixels are in thresh image
black_pixels = np.sum(thresh == 0)
print(black_pixels *25*0.001)
number_of_white_pix = np.sum(thresh == 255)

edged = cv2.Canny(thresh, 30, 200)

#Extract the contours in the binary image
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Sort the contours by area so that the outline of the cell is the largest contour
contours = sorted(contours, key=cv2.contourArea, reverse=True)

#draw the contours on the image
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

cnt = contours[0]
ellipse = cv2.fitEllipse(cnt)
ellipse = cv2.ellipse(img,ellipse,(0,255,0),2)

#extract the dimensions of the eclipse
(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)

print(cv2.contourArea(contours[0]))
#convert the messurments to microns where 1 pixel = 25nm and 1nm is 0.001 microns
x = x*25*0.001
y = y*25*0.001
MA = MA *25*0.001
ma = ma *25*0.001

#write on the image: (x μm) x (y μm) and (angle °) to the top left corner
font = cv2.FONT_HERSHEY_COMPLEX
cv2.putText(img, '{:.2f} um x {:.2f} um and {:.2f} degrees'.format(MA,ma,angle), (10,30), font, 1, (0,0,255), 2, cv2.LINE_AA)

#show the image
cv2.imshow('Pollen', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
