CC=g++

workerclient: workerClient.cpp
	$(CC) workerClient.cpp -o $@ 
