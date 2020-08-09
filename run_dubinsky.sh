#!/bin/sh

#TIME_LIMIT=0.000001
TIME_LIMIT=0.00001

# build with the new team sizes

#rm -f bin/barneshut-p
make clean
make --silent -f Makefile-parallel
#make --silent -f Makefile-parallel

# run
bin/barneshut-p datasets/dubinski $TIME_LIMIT

# delete output files
rm -rf out_dubinski_* gif_out_dubinski_*
