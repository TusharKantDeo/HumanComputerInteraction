import cv2
import numpy as np
import pickle

camera=0

font = cv2.FONT_HERSHEY_SIMPLEX
cl_low=0
cl_high=180
end=0
s=255
s_l=0
v=255
v_l=0
color_data={'low':0,'high':0,'s':0,'v':0,'sl':0,'vl':0}

t=0
stop=0

stp_arc=0
maxarc=1000
minarc=0
ksize=1
itn=1

def store():
 #global cl
 global cl_low
 global cl_high
 global end
 global s
 global v
 global s_l
 global v_l
 global color_data
 #global relation_sel
 #col_name=relation_sel[cl]
 color_data['low']=cl_low
 color_data['high']=cl_high
 color_data['s']=s
 color_data['v']=v
 color_data['sl']=s_l
 color_data['vl']=v_l




def create_filter1(frame):
 hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 global s_l
 global v_l
 global cl_low
 global cl_high
 global end
 global s
 global v
 lower_h=np.array([cl_low,0,0])
 higher_h=np.array([cl_high,s,v])
 mask=cv2.inRange(hsv,lower_h,higher_h)
 return mask




def color_low(x):
 global cl_low
 cl_low=x

def color_high(x):
 global cl_high
 cl_high=x

def s_upper(x):
 global s
 s=x

def v_upper(x):
 global v
 v=x


def s_low(x):
 global s_l
 s_l=x

def v_low(x):
 global v_l
 v_l=x

def stop(x):
 global end
 end=x

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

def thresh_ip(x):
 global t
 t=x
def stop_call(x):
 global stop
 stop=x

def stop_arc(x):
 global stp_arc
 stp_arc=x

def call(x):
 global minarc
 minarc=x


def call_kernel(x):
 global ksize
 ksize=x
def call_iter(x):
 global itn
 itn=x
def call_max(x):
 global maxarc
 maxarc=x





finalvar=(color_data,t,minarc,maxarc,ksize)



def init():
 #-----------------------------------------------------
 cap=cv2.VideoCapture(camera)
 ret ,frame=cap.read()
 #frame=cv2.imread('test.jpg')
 cv2.imshow('window',frame)
 #cv2.createTrackbar('color','window',0,4,sel)
 cv2.createTrackbar('lower color blue','window',0,180,color_low)
 cv2.createTrackbar('higher color blue','window',180,180,color_high)
 cv2.createTrackbar('upper s','window',255,255,s_upper) 
 cv2.createTrackbar('lower s:','window',0,255,s_low)
 cv2.createTrackbar('upper v:','window',255,255,v_upper)
 cv2.createTrackbar('lower v:','window',0,255,v_low)
 cv2.createTrackbar('done','window',0,2,stop)
 while(end!=2):
  if end==1:
   store()
  ret ,frame=cap.read()
  frame_tt=frame.copy()
  mask=create_filter1(frame_tt)
  res=cv2.bitwise_and(frame_tt,frame_tt,mask=mask)
  text='#0:red 1:yellow 2:green #>>>3:blue <<<#4:brown# 5:exit'
  cv2.putText(res,text,(1,100),font,0.5,(0,0,255),2,cv2.LINE_AA)
  cv2.imshow('window',res)
  cv2.waitKey(30)
 cv2.destroyAllWindows()
 #--------------------------------------------------
 ret ,frame=cap.read()
 frame_tt=frame.copy()
 mask=create_filter(frame_tt)
 res=cv2.bitwise_and(frame_tt,frame_tt,mask=mask)
 img=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
 #cv2.imshow('pre processing>>>>>imgo input',img)
 done=1
 global t
 global stop
 t=0
 stop=0
 cv2.namedWindow('pre_processing')
 cv2.createTrackbar('threshold value','pre_processing',0,255,thresh_ip)
 cv2.createTrackbar('stop','pre_processing',0,1,stop_call)
 while(done):
  if stop==1:
   done=0
  ret ,frame=cap.read()
  frame_tt=frame.copy()
  mask=create_filter(frame_tt)
  res=cv2.bitwise_and(frame_tt,frame_tt,mask=mask)
  img=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY) 
  #cv2.imshow('original_pre_processing',img)
  im=img.copy()
  _,th_n=cv2.threshold(im,t,255,cv2.THRESH_BINARY)
  cv2.imshow('pre_processing',th_n)
  cv2.waitKey(100)
 #print('done come out of while pre_processing=>trackbar=>while')
 cv2.destroyAllWindows()
 #-------------------------------------------------------------------
 cv2.namedWindow('black')
 cv2.createTrackbar('arclen','black',0,50000,call)
 cv2.createTrackbar('max arclen','black',500,50000,call_max)
 cv2.createTrackbar('kernel size','black',1,20,call_kernel)
 cv2.createTrackbar('iteration','black',1,20,call_iter)
 cv2.createTrackbar('stop','black',0,1,stop_arc)

 im=th_n.copy()
 im,cnts,_= cv2.findContours(im, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    
 global minarc
 global maxarc
 global ksize
 global itn
 global stp_arc
 stp_arc=0
 black=th_n.copy()
 black[:]=0
 kernel = np.ones((5,5),np.uint8)
 while(1):
  ret ,frame=cap.read()
  frame_tt=frame.copy()
  mask=create_filter(frame_tt)
  res=cv2.bitwise_and(frame_tt,frame_tt,mask=mask)
  img=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY) 
  #cv2.imshow('original_pre_processing',img)
  im=img.copy()
  _,th_n=cv2.threshold(im,t,255,cv2.THRESH_BINARY)
  im=th_n.copy()
  kernel = np.ones((ksize,ksize),np.uint8)
  for i in range(itn):
   im = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
  im,cnts,_= cv2.findContours(im, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
  cnts_temp=[c for c in cnts if cv2.arcLength(c, True)>minarc and cv2.arcLength(c, True)<maxarc]
  temp_imgg=black.copy()
  im_black=cv2.drawContours(temp_imgg,cnts_temp, -1,(255,0,0), 3)
  cv2.imshow('black',im_black)
  cv2.waitKey(30)
  if stp_arc==1:
   break
 global color_data
 cv2.destroyAllWindows()
 global finalvar
 finalvar=(color_data,t,minarc,maxarc,ksize)
 

init()

file='thres.pkl'
with open(file, 'wb') as pickle_file:
 pickle.dump(finalvar, pickle_file)

pickle_file.close()






