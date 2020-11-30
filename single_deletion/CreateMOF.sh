
#!/bin/bash

cat > calcdist.awk<<!
{
  # create associative arrays that store relevant information
  # from both files - atom id and xyz co-ordinates
  if (NR == FNR) {
    x[FNR] = \$1":"\$4":"\$5":"\$6
  } else {
    y[FNR] = \$1":"\$4":"\$5":"\$6
    n = FNR
  }
}
END {
  # The distance calculating formula is
  # SQRT ((X1-X2)^2 + (Y1-Y2)^2 + (Z1-Z2)^2)
  for (i=1; i<=n; i++) {
    split(x[i], a, ":")
    for (j=1; j<=n; j++) {
      split(y[j], b, ":")
      printf("%4s %4s %.5f\n",a[1],b[1],sqrt((a[2]-b[2])^2 + (a[3]-b[3])^2 + (a[4]-b[4])^2))
    }
  }
}
!

CreateMOF () {

    cp $1 temp.cif

    dupli=$2
    
    sed '/_atom_site_fract_z/q0' temp.cif > info
    grep "Ru1 Ru\|Ru Ru\|C1 C\|C2 C\|C C\|N1 N\|N2 N\|N N\|O O\|H H" temp.cif > body_list
    
    cat info body_list > edit.cif
    
    
    for j in $(seq 1 $dupli)
    
    do
    
    for NUM in $3 
    
    do
    
    sed '/_atom_site_fract_z/q0' edit.cif > info
    grep "N1 N\|Ru\|C C\|H H\|N N" edit.cif > end_list 
    grep "C1 C\|O O" edit.cif > C1_O_list
    grep "C2 C" edit.cif > C2_list 
    ratio=$(echo "scale = 0; $NUM*100/32 " | bc )
    
    cp C2_list C2_temp
    
    ###Random select a C on benzene and replace to N for pyridine. 
        
    list=($(shuf -i 0-31 -n $NUM | sort -n))
        
    #echo ${list[@]}
    
    
    #for NUM in {2..32..8}
     
    for i in "${list[@]}"
    
    do
    #row1=$(($i*3+1))
    #row2=$(($i*3+2))
    #row3=$(($i*3+3))
    #
    #rand=$[ $RANDOM % 3 ]
    
    arr[0]=$(($i*3+1))
    arr[1]=$(($i*3+2))
    arr[2]=$(($i*3+3))
    
    rand=$[ $RANDOM % 3 ]
    
    lineNo=${arr[$rand]}
    
    #echo $lineNo
    
    sed -e "${lineNo}s/C2 C /N3 N /" C2_temp > C2_int
     
    mv C2_int C2_temp
     
    done
     
    grep "N3 N" C2_temp > N3_list
    grep "C2 C" C2_temp > C2_list
     
    #Creat the new list of C2,N3
    mv C2_temp C2_N3_list
    #cat header C2_N3_list C1_O_list end_list > format2.cif
     
    cat N3_list C1_O_list C2_list > edit_list 
     
    ####Calculate the nearest COO- group to the N on the pyridine
    ###Make a list for the Pryidine N and all COO- group for search
    
    index=$(wc -l edit_list | awk '{print $1}')
     
    for i in $(seq ${index})
    
    do
    echo $i >> insert_index
    
    done
    
    paste insert_index edit_list | awk '{print $1, $2, $3, $4, $5, $6}' > edit_list_index
    
    rm insert_index
    
    grep "C2 C" edit_list_index > C2_list_index
    grep "N3 N" edit_list_index > N3_list_index
    grep "C1 C" edit_list_index > C1_list_index
    grep "O O" edit_list_index > O_list_index
    
    ## Find the nearest Carbon to the Pyridine N, put it in a list for delete
    awk -f calcdist.awk N3_list_index C1_list_index | grep "0.05315\|0.96417"  | awk '{print $2}' > C1_d_index
    awk -f calcdist.awk N3_list_index C2_list_index | grep "0.09354"  | awk '{print $2}' > C3_d_index
     
    # Find same C on the pyridine ring
    while read file
    do 
    grep "^$file C2" C2_list_index 
    
    done < C3_d_index > C3_replace_list
    
    cp C2_list_index C2_temp
    
    while read file
    do
    sed -i -e "s/$file C2 C /$file C3 C /" C2_temp
    done < C3_d_index 
    
    mv C2_temp C2_C3_index
    
    awk '{print $2, $3, $4, $5, $6}' C2_C3_index > C2_C3_new_list
    
    # Delete the Carbon and update the new C1_list 
    while read file
    do 
    grep "^$file C1" C1_list_index 
    
    done < C1_d_index > C1_d_list
    
    cp C1_list_index C1_backup
    while read file 
    do 
    sed -i -e "/^$file/d" C1_list_index 
    done < C1_d_list
    awk '{print $2, $3, $4, $5, $6}' C1_list_index > C1_new_list
    awk '{print $2, $3, $4, $5, $6}' N3_list_index > N3_new_list
    
    # Find the nearest Oxygen to the COO carbon, put it in a list for delete
    awk -f calcdist.awk C1_d_list O_list_index | grep "0.04798"  | awk '{print $2}' > O_d_index
     
    # Delete the Oxygen and update the new O_list 
    while read file
    do 
    grep "^$file O" O_list_index 
    done < O_d_index > O_d_list
    
    cp O_list_index O_backup
    
    while read file 
    do 
    sed -i -e "/^$file/d" O_list_index 
    done < O_d_index 
    awk '{print $2, $3, $4, $5, $6}' O_list_index > O_new_list
     
    cat N3_new_list C1_new_list C2_C3_new_list O_new_list end_list > frame_${ratio}_$j
    
    done
    
    #Clean up
    
    done
    
    rm temp.cif body_list info
    rm *list *index *_backup 
}

CreateMOF $1 $2 $3

rm calcdist.awk 
