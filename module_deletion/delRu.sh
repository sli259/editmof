#!/bin/bash

delRu (){

INPUTCIF=$1

cp ${INPUTCIF} temp.cif

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
 
sed '/_atom_site_fract_z/q0' temp.cif > info
grep "C C\|H H" temp.cif > C_H_list 
grep "N1 N" temp.cif > N1_list 
grep "Ru Ru" temp.cif > Ru_list 
grep "Ru1 Ru" temp.cif > Ru1_list 
grep "N N" temp.cif > N_list 
grep "O1 O" temp.cif > O1_list
grep "O O" temp.cif > O_list
grep "C1 C" temp.cif > C1_list
grep "C2 C" temp.cif > C2_list 

cat Ru1_list Ru_list N1_list N_list O1_list O_list C1_list C2_list > temp_list
  
index=$(wc -l temp_list | awk '{print $1}')
  
for i in $(seq ${index})

do
echo $i >> insert_index

done

paste insert_index temp_list | awk '{print $1, $2, $3, $4, $5, $6}' > edit_list_index
 
rm insert_index
grep "Ru1 Ru" edit_list_index > Ru1_list_index
grep "Ru Ru" edit_list_index > Ru_list_index
grep "N1 N" edit_list_index > N1_list_index
grep "N N" edit_list_index > N_list_index
grep "C1 C" edit_list_index > C1_list_index
grep "O1 O" edit_list_index > O1_list_index
grep "O O" edit_list_index > O_list_index
grep "C2 C" edit_list_index > C2_list_index

#### Find the other Ru1 if on the edge
awk -f calcdist.awk master_d_list Ru1_list_index | grep "0.00000\|1.00000"  | awk '{print $2}' > Ru1_d_index

while read file
do 
grep "^$file Ru1" Ru1_list_index
done < Ru1_d_index > Ru1_d_list_new

### find the Ru1_Ru pair
awk -f calcdist.awk Ru1_d_list_new Ru_list_index | grep "0.08454"   | awk '{print $2}' > Ru_d_index

while read file
do 
grep "^$file Ru" Ru_list_index
done < Ru_d_index > Ru_d_list

#### find the Ru1_N1 pair
awk -f calcdist.awk Ru1_d_list_new N1_list_index  | grep "0.07935"   | awk '{print $2}' > N1_d_index

while read file
do 
grep "^$file N1" N1_list_index
done < N1_d_index > N1_d_list

#### find N1_N pair

awk -f calcdist.awk N1_d_list N_list_index | grep "0.04437\|0.08792"   | awk '{print $2}' > N_d_index
 
while read file
do 
grep "^$file N" N_list_index
done < N_d_index > N_d_list

### Find Ru1_O1 4 pairs
awk -f calcdist.awk Ru1_d_list_new O1_list_index  | grep "0.07565"   | awk '{print $2}' > O1_d_index
 
while read file
do 
grep "^$file O1" O1_list_index
done < O1_d_index > O1_d_list

### Find Ru_O 4 pairs
awk -f calcdist.awk Ru_d_list O_list_index  | grep "0.07565"   | awk '{print $2}' > O_d_index
 
while read file
do 
grep "^$file O" O_list_index
done < O_d_index > O_d_list

#### Find O_C1 
awk -f calcdist.awk O_d_list C1_list_index | grep "0.04798\|1.12792"   | awk '{print $2}' > C1_d_index
sort C1_d_index | sort -u > temp

while read file
do 
grep "^$file C1" C1_list_index
done < temp > C1_d_list


### Delete the atoms
cat Ru1_d_list_new Ru_d_list N1_d_list N_d_list O1_d_list O_d_list C1_d_list > d_list
cp edit_list_index temp_list

while read file 
do 
sed -i -e "/^$file/d" temp_list
done < d_list


### Find C2 to replace to N3
awk -f calcdist.awk C1_d_list C2_list_index | grep "0.05315\|0.96417"  | awk '{print $2}' > C2_s_index
 
while read file
do 
sed -i "s/$file C2 C/$file N3 N/g;" temp_list
done < C2_s_index  

grep "N3 N" temp_list > N3_list_index
grep "C2 C" temp_list > C2_list_new_index

# Create new cif 
awk '{print $2, $3, $4, $5, $6}' temp_list > new_list
cat new_list C_H_list > frame

##Clean up template file

rm *list *index info  Ru1_d_list_new temp temp.cif

}

delRu $1
