presence_detection_node:
		g++ presence_detection_safe.cpp -o presence_detection_safe -std=c++11 -lboost_system -L/lib -lrt -lm -lpthread
