#!/bin/bash

runfunc () {
    file=$1
    a=$2
    b=$3
    c=$4
    def=$5
    #tot_N=$(echo $(($a-1))*$(($b-1))*$(($c-1))| bc )
    tot_N=$(echo $(($a))*$(($b))*$(($c))| bc )
    #echo ${tot_N}
    ratio=$(echo "scale = 0; $def*100/32 " | bc )
    #echo $ratio
    
    count=1
    
    ./CreateMOF.sh $1 ${tot_N} $5
    
    if (( $count < ${tot_N} ))
    then
    for i in $(seq 1 $a)
    do 
    for j in $(seq 1 $b)
    do
    for k in $(seq 1 $c)
    do
    awk -v aext=$i -v bext=$j -v cext=$k '{print $1, $2, $3+aext-1, $4+bext-1, $5+cext-1}' frame_${ratio}_$count > new_${i}_${j}_${k}_$count
    
    let count++
    done
    done
    done
    
    fi
}

runfunc $1 $2 $3 $4 $5

cat > head <<!
data_primitive
_symmetry_cell_setting           triclinic
_symmetry_space_group_name_H-M   'P 1'
_symmetry_Int_Tables_number      1
loop_
_symmetry_equiv_pos_site_id
_symmetry_equiv_pos_as_xyz
1 x,y,z
_cell_length_a                   26.662
_cell_length_b                   26.662
_cell_length_c                   26.662
_cell_angle_alpha                90.0
_cell_angle_beta                 90.0
_cell_angle_gamma                90.0
_cell_volume                     18953 
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
!

cat head new_* > new.cif
rm head new_* frame*
