import cv2
import numpy as np


points=[]
#p0=
font = cv2.FONT_HERSHEY_SIMPLEX
lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
color = np.random.randint(0,255,(100,3))



def draw_circle(event,x,y,flags,param):
 global points
 global p0   
 if event == cv2.EVENT_LBUTTONDBLCLK:
  cv2.circle(img,(x,y),5,(0,0,255),-1)
  cv2.putText(img,str(len(points)),(x,y), font, 1,(255,255,255),2,cv2.LINE_AA)
  points.append((x,y))
  p0=np.asarray(points)
  p0=p0.astype(np.float32)
  p0=p0.reshape(-1,1,2) 


cap = cv2.VideoCapture(0)
ret,frame = cap.read()
#cv2.imshow('hey',frame)
#cv2.waitKey(0)
img = np.zeros_like(frame)
cv2.namedWindow("frame")
cv2.setMouseCallback("frame",draw_circle)

done=True

while(1):
   ret,frame = cap.read()
   frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   if(done):
    imgo = cv2.add(frame,img)
    
    
   else:  #(len(points)>0) 
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]
    #print("else")
    # draw the tracks
    if(len(good_new)==0):
     print("could not track")
     good_new = p0
     good_old = p0
    else:  
     for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        img = cv2.line(img, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    imgo = cv2.add(frame,img)
    p0 = good_new.reshape(-1,1,2) 
   cv2.imshow('frame',imgo)
   k = cv2.waitKey(30) & 0xff
   if k == 27:
        break
   elif k == ord('a'):
    done=False
    # Now update the previous frame and previous points
   old_gray = frame_gray.copy()
  
cv2.destroyAllWindows()
cap.release()

