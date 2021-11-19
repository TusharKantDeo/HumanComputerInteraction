import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
while(1):
 ret,frame = cap.read()
 cv2.imshow('frame',frame)
 k = cv2.waitKey(30) & 0xff
 if k == ord('a'):
  break
   
img =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow('frame',img)
cv2.waitKey(0)
# Initiate STAR detector
#orb = cv2.ORB()
orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img,None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

img2 = cv2.drawKeypoints(img,kp,None,color=(0,255,0), flags=0)
plt.imshow(img2),plt.show()




'''
# harri corrner
import cv2
import numpy as np

filename = 'chessboard.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()

'''

'''
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)

plt.imshow(img),plt.show()

'''


'''
import cv2
import numpy as np

img = cv2.imread('home.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT()
kp = sift.detect(gray,None)  # mask 

img=cv2.drawKeypoints(gray,kp)

cv2.imwrite('sift_keypoints.jpg',img)

img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imwrite('sift_keypoints.jpg',img)


'''



'''
finding triangle

import cv2
import numpy as np
image_obj = cv2.imread('image.jpg')

gray = cv2.cvtColor(image_obj, cv2.COLOR_BGR2GRAY)

kernel = np.ones((4, 4), np.uint8)
dilation = cv2.dilate(gray, kernel, iterations=1)

blur = cv2.GaussianBlur(dilation, (5, 5), 0)


thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

# Now finding Contours         ###################
_, contours, _ = cv2.findContours(
    thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
coordinates = []
for cnt in contours:
        # [point_x, point_y, width, height] = cv2.boundingRect(cnt)
    approx = cv2.approxPolyDP(
        cnt, 0.07 * cv2.arcLength(cnt, True), True)
    if len(approx) == 3:
        coordinates.append([cnt])
        cv2.drawContours(image_obj, [cnt], 0, (0, 0, 255), 3)

cv2.imwrite("result.png", image_obj)
'''


