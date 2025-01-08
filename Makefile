CC = g++
CFLAGS = -Wall -I/usr/include/eigen3
SRC = active_1D.cpp
#SRC = active_1D.cpp
#SRC = main_2D.cpp
OUT = active_1D

all:
	$(CC) $(CFLAGS) -o $(OUT) $(SRC)
