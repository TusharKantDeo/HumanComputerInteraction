//opencv
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/core/core.hpp"
//--c++
#include <iostream>

using namespace cv;
using namespace std;

int i=0;
// Input Quadilateral or Image plane coordinates
Point2f inputQuad[4];
void Callbackfunc(int Event, int x, int y, int flags, void *userdata)
{
	Point2f p;
	if (Event == EVENT_LBUTTONDOWN)
	{
		p.x=x;p.y=y;
		
		inputQuad[i]= p;
		i++;
	}
}

void on_low_r_thresh_trackbar(int, void *);
void on_high_r_thresh_trackbar(int, void *);
void on_low_g_thresh_trackbar(int, void *);
void on_high_g_thresh_trackbar(int, void *);
void on_low_b_thresh_trackbar(int, void *);
void on_high_b_thresh_trackbar(int, void *);

int low_r = 101, low_g = 106, low_b = 87;
int high_r = 164, high_g = 180, high_b = 108;

 
int main( )
{
  VideoCapture vid(1);
 
    // Output Quadilateral or World plane coordinates
    Point2f outputQuad[4];
         
    // Lambda Matrix
    Mat lambda( 2, 4, CV_32FC1 );
    //Input and Output Image;
    Mat input, output;

    cout<<"The 4 points that select quadilateral on the input , from top-left in clockwise order and press q to proceed further\n"<<endl;


    while ((char)waitKey(1) != 'q')
    {
    vid.read(input);
    imshow("win",input);
   
    // Set the lambda matrix the same type and size as input
    lambda = Mat::zeros( input.rows, input.cols, input.type() );
 
    // The 4 points that select quadilateral on the input , from top-left in clockwise order
    // These four pts are the sides of the rect box used as input 

    setMouseCallback("win", Callbackfunc, NULL);
    setMouseCallback("win", Callbackfunc, NULL);
    setMouseCallback("win", Callbackfunc, NULL);
    setMouseCallback("win", Callbackfunc, NULL);
    }

    if(i==4)
        destroyWindow("win");

    //windows for track bar
    namedWindow("Video Capture", WINDOW_NORMAL);
    namedWindow("Object Detection", WINDOW_NORMAL);
    //-- Trackbars to set thresholds for RGB values
    createTrackbar("Low R", "Object Detection", &low_r, 255, on_low_r_thresh_trackbar);
    createTrackbar("High R", "Object Detection", &high_r, 255, on_high_r_thresh_trackbar);
    createTrackbar("Low G", "Object Detection", &low_g, 255, on_low_g_thresh_trackbar);
    createTrackbar("High G", "Object Detection", &high_g, 255, on_high_g_thresh_trackbar);
    createTrackbar("Low B", "Object Detection", &low_b, 255, on_low_b_thresh_trackbar);
    createTrackbar("High B", "Object Detection", &high_b, 255, on_high_b_thresh_trackbar);
    //video input
    while(1)
    {
     
        //Load the image
        vid.read(input);

        //--initialising mat for detecting finger
        Mat frame1, frame_threshold,frame3;
        frame3=input.clone();

        cvtColor(input, frame1, COLOR_BGR2HSV);
        //-- Detect the object based on RGB Range Values
        inRange(frame1, Scalar(low_b, low_g, low_r), Scalar(high_b, high_g, high_r), frame_threshold);
        if((char)waitKey(1) != 'r')
        {
            imshow("Video Capture",input);
            imshow("Object Detection",frame_threshold);
            waitKey(1);
        }   

        //--remove noise and dilate using median blur and dilation frame threshold1 used for detecting shadow and 
        Mat frame_threshold1;
        int blurSize = 5;
        int elementSize = 5;
        medianBlur(frame_threshold, frame_threshold1, blurSize);
        Mat element = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(2 * elementSize + 1, 2 * elementSize + 1), cv::Point(elementSize, elementSize));
        //dilate(frame_threshold1, frame_threshold1, element);
        erode(frame_threshold1, frame_threshold1, element);
                if((char)waitKey(1) != 'r')
        {
            imshow("dilated",frame_threshold1);
          
            waitKey(1);
        } 


        // The 4 points where the mapping is to be done , from top-left in clockwise order
        outputQuad[0] = Point2f( 0,0 );
        outputQuad[1] = Point2f( input.cols-1,0);
        outputQuad[2] = Point2f( input.cols-1,input.rows-1);
        outputQuad[3] = Point2f( 0,input.rows-1  );
     
        // Get the Perspective Transform Matrix i.e. lambda 
        lambda = getPerspectiveTransform( inputQuad, outputQuad );
        // Apply the Perspective Transform just found to the src image
        warpPerspective(input,output,lambda,output.size() );
        /*
        //--ycrcb colorscale to determine skin color
        Mat nim,nmim;
        cvtColor(output,nim,COLOR_BGR2YCrCb);
        inRange(nim, Scalar(0, 133, 77), Scalar(255, 173, 127), nmim);
        */
        //thresholding screen frame for finger detect
        Mat im1,im2;
        cvtColor(output,im1,COLOR_BGR2HSV);
        inRange(im1, Scalar(low_b, low_g, low_r), Scalar(high_b, high_g, high_r), im2);



     


        //Display input and output
        
        //--showing normal window transformed into screen frame -- imshow("Output",output);
        //--showing skin color detected using ycrcb in screen frame-- imshow("finger_screen_frame",nmim);
        waitKey(1);
        if((char)waitKey(1)=='q')
            break;
    }


    return 0;
}

//functions definitions

void on_low_r_thresh_trackbar(int, void *)
{
    low_r = min(high_r - 1, low_r);
    setTrackbarPos("Low R", "Object Detection", low_r);
}

void on_high_r_thresh_trackbar(int, void *)
{
    high_r = max(high_r, low_r + 1);
    setTrackbarPos("High R", "Object Detection", high_r);
}

void on_low_g_thresh_trackbar(int, void *)
{
    low_g = min(high_g - 1, low_g);
    setTrackbarPos("Low G", "Object Detection", low_g);
}

void on_high_g_thresh_trackbar(int, void *)
{
    high_g = max(high_g, low_g + 1);
    setTrackbarPos("High G", "Object Detection", high_g);
}

void on_low_b_thresh_trackbar(int, void *)
{
    low_b = min(high_b - 1, low_b);
    setTrackbarPos("Low B", "Object Detection", low_b);
}

void on_high_b_thresh_trackbar(int, void *)
{
    high_b = max(high_b, low_b + 1);
    setTrackbarPos("High B", "Object Detection", high_b);
}