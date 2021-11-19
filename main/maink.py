import pyautogui
import cv2
import numpy as np
import pickle
#import init

import matplotlib.pyplot as plt
camera=0

#---------parameter init: color_data for mask,t=>threshold value, minarc and maxarc => contours values------------------

#temp=init.init()         #  temp one eg is for blue color :-({'v': 255, 'low': 72, 'sl': 10, 'vl': 0, 'high': 138, 's': 197}, 57, 180, 364)
#init is off and data read from already stored

file='thres.pkl'
with open(file, 'rb') as f:
  temp = pickle.load(f)

f.close()


color_data=temp[0]
t=temp[1]
minarc=temp[2]
maxarc=temp[3]
ksize=temp[4]
print(temp)
print(color_data)
print(t)
print(minarc)
print(maxarc)
print(ksize)


#------------function definations--------create_filter and find location=> will contain find_contours and centroids-----------------------------------------
def create_filter(frame):
 hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 #cv2.imshow('filter>>>>>hsv input',hsv)
 #cv2.waitKey(0)
 global color_data
 s_l=color_data['sl']
 v_l=color_data['vl']
 cl_low=color_data['low']
 cl_high=color_data['high']
 s=color_data['s']
 v=color_data['v']
 lower_h=np.array([cl_low,s_l,v_l])
 higher_h=np.array([cl_high,s,v])
 mask=cv2.inRange(hsv,lower_h,higher_h)
 #cv2.imshow('filter>>>>>hsv output',mask)
 #cv2.waitKey(0)
 return mask

#=======================================================
def find_location(masked_image_gray):   # it will take just masked image that is frame anded with mask and converted to gray scale
 global t
 _,for_cont=cv2.threshold(masked_image_gray,t,255,cv2.THRESH_BINARY) 
 im=for_cont.copy()
 kernel = np.ones((ksize,ksize),np.uint8)
 im = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
 im,cnts,_= cv2.findContours(im, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    
 global minarc
 global maxarc
 cnts=[c for c in cnts if cv2.arcLength(c, True)>minarc and cv2.arcLength(c, True)<maxarc]
 points=[]
 for c in cnts:
  M=cv2.moments(c)
  if M["m00"]==0:
   cx=0
   cy=0
  else:
   cx=int(M["m10"]/M["m00"])
   cy=int(M["m01"]/M["m00"])
  cord=(cx,cy)
  points.append(cord)
 return (cnts,points)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------


def pointloc(frame): #read frame and pass to it return com points [(cx,cy)....]
 temp_frame=frame.copy()
 mask=create_filter(temp_frame)
 res=cv2.bitwise_and(temp_frame,temp_frame,mask=mask)
 gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
 loc=find_location(gray)
 return loc
 
def closestindex(point,lastpoint):
 ind=0
 dis=10000000
 for i in point:
  ptx=i[0]
  pty=i[1]
  t=((ptx-lastpoint[0])**2+(pty-lastpoint[0])**2)
  if(t<dis):
   dis=t
   ind=i
 return ind  







lastpoint=(50,50)


#position finger 
cap=cv2.VideoCapture(camera)

while(1):
 ret ,frame=cap.read()
 frame = cv2.rectangle(frame,(45,45),(55,55),(0,255,0),3)
 loc=pointloc(frame)
 if len(loc)!=0:
  point=loc[1]
  if len(point) !=0:
    ind=closestindex(point,lastpoint)
    #==================================================================================================================================================
    ptx=ind[0]
    pty=ind[1]
    #==================================================================================================================================================
    frame = cv2.circle(frame,(ptx,pty), 10 , (0,0,255), -1) 
  else:
    print("no points ************")
    print(len(point))
 #number.append(len(point)) 
 cv2.imshow('position',frame)
 k = cv2.waitKey(25) & 0xff
 if k == 27:
   cv2.destroyAllWindows()
   break
 






#number=[]
#t=0

#frameCounter = 0
#pt = (0,point[ind][0],point[ind][1])
#frameCounter = frameCounter + 1
# kalman codes here
state = np.array([lastpoint[0],lastpoint[1]], dtype='float64') 
kalman = cv2.KalmanFilter(2,2,0)	
kalman.transitionMatrix = np.array([[1., 0.],[0., 1.]])
kalman.measurementMatrix = 1. * np.eye(2, 2)
kalman.processNoiseCov = 1e-5 * np.eye(2, 2)
kalman.measurementNoiseCov = 1e-3 * np.eye(2, 2)
kalman.errorCovPost = 1e-1 * np.eye(2, 2)
kalman.statePost = state
measurement = state 
font = cv2.FONT_HERSHEY_SIMPLEX
'''
while(1):
 ret ,frame=cap.read()
 loc=pointloc(frame)
 #if len(loc)!=0:
  point=loc[1]
  if len(point) !=0:
    ind=closestindex(point,lastpoint)
    #==================================================================================================================================================
    prediction = kalman.predict() #prediction
    ptx=ind[0]
    pty=ind[1]
    measurement = np.array([ptx, pty], dtype='float64')
    if not (ptx ==0 and pty==0):
            posterior = kalman.correct(measurement)
    if (ptx ==0 and pty==0):
            ptx,pty = prediction
    else:
      ptx,pty = posterior	
    
    #==================================================================================================================================================
    frame = cv2.circle(frame,(int(ptx),int(pty)), 10 , (0,0,255), -1) 
    #==================================================================================================================================================
    #dx=ptx-lastpoint[0]
    #dy=ptx-lastpoint[0]
    lastpoint=(ptx,pty)
    #if(abs(dx)>10):
    #if(dx<0):
    #  direction="==>>>>>"
    #  pyautogui.dragRel(50, 0, duration=0.1)
    # else:
    #  direction="<<<===="
    #  pyautogui.dragRel(-50, 0, duration=0.1)
    pyautogui.moveTo(ptx, pty, duration= 0.1)     
#cv2.putText(frame,direction,(10,500), font, 4,(255,255,255),2,cv2.LINE_AA) 
    #==================================================================================================================================================
    
    
  else:
    print("no points ************")
    print(len(point))
 #number.append(len(point)) 
 cv2.imshow('frame',frame)
 cv2.waitKey(10) 
 #t+=1
'''
#plt.hist(number, bins='auto')  # arguments are passed to np.histogram
#plt.title("Histogram with 'auto' bins")
#plt.show()


while(1):
  ret ,frame=cap.read()
  loc=pointloc(frame)
 #if len(loc)!=0:
  point=loc[1]
  if len(point) !=0:
    ind=closestindex(point,lastpoint)
    #==================================================================================================================================================
    prediction = kalman.predict() #prediction
    ptx=ind[0]
    pty=ind[1]
    measurement = np.array([ptx, pty], dtype='float64')
    if not (ptx ==0 and pty==0):
            posterior = kalman.correct(measurement)
    if (ptx ==0 and pty==0):
            ptx,pty = prediction
    else:
      ptx,pty = posterior	
    
    #==================================================================================================================================================
    frame = cv2.circle(frame,(int(ptx),int(pty)), 10 , (0,0,255), -1) 
    #==================================================================================================================================================
    dx=ptx-lastpoint[0]
    dy=ptx-lastpoint[0]
    lastpoint=(ptx,pty)
    if(abs(dx)>10):
    #if(dx<0):
    #  direction="==>>>>>"
    #  pyautogui.dragRel(50, 0, duration=0.1)
    # else:
    #  direction="<<<===="
    #  pyautogui.dragRel(-50, 0, duration=0.1)
     pyautogui.moveTo(ptx, pty, duration= 0.1)     
#cv2.putText(frame,direction,(10,500), font, 4,(255,255,255),2,cv2.LINE_AA) 
    #==================================================================================================================================================
    
    
  else:
    print("no points ************")
    print(len(point))
 #number.append(len(point)) 
  cv2.imshow('frame',frame)
  k = cv2.waitKey(10) & 0xff
  if k == 27:
   break
 #t+=1

