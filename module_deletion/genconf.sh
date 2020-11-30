#!/bin/bash

genconf (){
sed '/_atom_site_fract_z/q0' uc.cif > info

a=$1
b=$2
c=$3

round (){
    printf "%.${2}f" "${1}"
}
alen=$(echo "scale=3; $a*26.662" | bc)
blen=$(echo "scale=3; $b*26.662" | bc)
clen=$(echo "scale=3; $c*26.662" | bc)
V=$(echo "$alen*$blen*$clen" | bc)
V_round=`round $V 0`

sed -i "s/_cell_length_a                   26.662/_cell_length_a                   $alen/g" info
sed -i "s/_cell_length_b                   26.662/_cell_length_b                   $blen/g" info
sed -i "s/_cell_length_c                   26.662/_cell_length_c                   $clen/g" info
sed -i "s/_cell_volume                     18953/_cell_volume                     ${V_round}/g" info

tot_N=$(echo $a*$b*$c | bc )

count=1

if (( $count < ${tot_N} ))
then
for i in $(seq 1 $a)
do 
for j in $(seq 1 $b)
do
for k in $(seq 1 $c)

do
awk -v aext=$i -v bext=$j -v cext=$k -v a=$a -v b=$b -v c=$c '{printf "%3s %3s %3.5f %3.5f %3.5f\n", $1, $2, ($3+aext-1)/a, ($4+bext-1)/b, ($5+cext-1)/c}' frame_$count > new_${i}_${j}_${k}_$count

#echo $count

let count++
done
done
done

fi

}

genconf $1 $2 $3

