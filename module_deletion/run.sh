#!/bin/bash

#SBATCH -J mol      # job name
#SBATCH -o mol.err
#SBATCH -e mol.out

#SBATCH -N 1        # number of nodes requested
#SBATCH -n 4        # total number of mpi tasks requested
#SBATCH -t 72:00:00     # run time (hh:mm:ss) - 60 hours

source /scratch/data/source/torch.sh

set -e

##########User defined variables##########

filename=gaussian_test.log
sampleN=500

##########################################

echo "#SPG_Num Sample_Num Energy(H.) Density(g/cm^3) Packing_Type" > data1

for SPG in 1 4 5 7 9 13 14 15 18 19 29 33 43 56 60 61 76 88 92 144 147 169

do
mkdir $SPG

cp *.py ./$SPG

cd $SPG
sg=$(basename "$PWD")
rm -rf result traj packing
mkdir result traj packing
for i in $(seq 1 $sampleN)
    do
        python makeXtal-v2b.py -f ../$filename -s $SPG
        mv opt.cif opt-spg${sg}-00$i.cif
        mv opt.gro opt-spg${sg}-00$i.gro
		python assign_pack-v3.py -f ../$filename -g opt-spg${sg}-00$i.gro
		mv struc_info.dat pk-spg${sg}-00$i.dat
        mv opt.traj spg${sg}-00$i.traj
		pk=$(head pk-spg${sg}-00$i.dat)	
        info=$(head result.dat)
        echo "$sg 00$i" $info $pk >> ../data1
        mv result.dat result-${sg}-00$i.dat 
		mv pk-spg${sg}-00$i.dat ./packing
        mv result-${sg}-00$i.dat ./result
        mv spg${sg}-00$i.traj ./traj
    done

cd ../
done
