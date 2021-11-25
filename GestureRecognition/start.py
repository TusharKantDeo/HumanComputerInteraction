import train
import loading
def start():
	print "                      Welcome                    "
	print "                      Loading...                 "
	e,f=train.load_data_wrapper()
	net=loading.Network([784,30,10])
	s,t=net.SGD(e, 1, 10, 7.15)
	print "                  Press p to start               "
	print "               press p to stop(two times)        "
	print "               press l for next loop             "
	return(s,t)


