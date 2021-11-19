#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/core.hpp"
#include <iostream>
#include <stdlib.h>

using namespace std;
using namespace cv;

void on_low_r_thresh_trackbar(int, void *);
void on_high_r_thresh_trackbar(int, void *);
void on_low_g_thresh_trackbar(int, void *);
void on_high_g_thresh_trackbar(int, void *);
void on_low_b_thresh_trackbar(int, void *);
void on_high_b_thresh_trackbar(int, void *);

int low_r = 101, low_g = 106, low_b = 87;
int high_r = 164, high_g = 180, high_b = 108;

int main()
{
	VideoCapture vid(1);
	Mat frame2;
	namedWindow("Video Capture", WINDOW_NORMAL);
	namedWindow("Object Detection", WINDOW_NORMAL);
	//-- Trackbars to set thresholds for RGB values
	createTrackbar("Low R", "Object Detection", &low_r, 255, on_low_r_thresh_trackbar);
	createTrackbar("High R", "Object Detection", &high_r, 255, on_high_r_thresh_trackbar);
	createTrackbar("Low G", "Object Detection", &low_g, 255, on_low_g_thresh_trackbar);
	createTrackbar("High G", "Object Detection", &high_g, 255, on_high_g_thresh_trackbar);
	createTrackbar("Low B", "Object Detection", &low_b, 255, on_low_b_thresh_trackbar);
	createTrackbar("High B", "Object Detection", &high_b, 255, on_high_b_thresh_trackbar);
		
	while(1)
	{
		//Mat frame2;
		vid.read(frame2);
		if(frame2.empty())
		{
			cout<<"frame not read"<<endl;
		}
		Mat frame1, frame_threshold,frame3;
		frame3=frame2.clone();


		cvtColor(frame2, frame1, COLOR_BGR2HSV);
		

		//-- Detect the object based on RGB Range Values
		inRange(frame1, Scalar(low_b, low_g, low_r), Scalar(high_b, high_g, high_r), frame_threshold);
		//--remove noise and dilate using median blur and dilation

		int blurSize = 5;
        int elementSize = 5;
        medianBlur(frame_threshold, frame_threshold, blurSize);
        Mat element = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(2 * elementSize + 1, 2 * elementSize + 1), cv::Point(elementSize, elementSize));
        dilate(frame_threshold, frame_threshold, element);


        //--contour detect

        std::vector<std::vector<cv::Point> > contours;
        std::vector<cv::Vec4i> hierarchy;
        cv::findContours(frame_threshold, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, cv::Point(0, 0));
        size_t largestContour = 0;
        size_t ndlargestContour = 0;
        for (size_t i = 1; i < contours.size(); i++)
         {
           if (cv::contourArea(contours[i]) > cv::contourArea(contours[largestContour]))
              ndlargestContour=largestContour;
              largestContour = i;

         }
        cv::drawContours(frame3, contours, largestContour, cv::Scalar(0, 0, 255), 1);
        cv::drawContours(frame3, contours, ndlargestContour, cv::Scalar(0, 0, 255), 1);



		//-- Show the frames
		//namedwindow("object Detection",WINDOW_NORMAL);
		imshow("Video Capture", frame2);
		imshow("Object Detection", frame_threshold);
		imshow("Contour", frame3);
		waitKey(1);
		
	}

	return 0;
}

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