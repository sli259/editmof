#!/bin/bash

mkdir path_file

for i in {1..100}
    do
        python 2D_walk.py -a 50 -r 3 -n 20
        cp 2d-walk.dat run-$i.dat
        awk 'NR==4{print; }' run-$i.dat | awk '{$1=""; print}' >> data
        mv run-$i.dat ./path_file
    done
