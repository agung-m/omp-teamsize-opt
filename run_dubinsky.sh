#!/bin/sh

#TIME_LIMIT=0.000001
TIME_LIMIT=0.00001

# build with the new team sizes
#rm -f bin/barneshut-p
make clean
make -f Makefile-parallel

# run
bin/barneshut-p datasets/dubinski $TIME_LIMIT
