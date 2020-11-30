#!/bin/bash

formatCIF (){

   grep "C C\|H H" $1 > C_H_list
   grep "N1 N" $1 > N1_list
   grep "Ru Ru" $1 > Ru_list
   grep "Ru1 Ru" $1 > Ru1_list
   grep "N N" $1 > N_list
   grep "O1 O" $1 > O1_list
   grep "O O" $1 > O_list
   grep "C1 C" $1 > C1_list
   grep "C2 C" $1 > C2_list
   
   cat Ru1_list Ru_list N1_list N_list O1_list O_list C1_list C2_list > temp_list
   
   index=$(wc -l temp_list | awk '{print $1}')
   
   for i in $(seq ${index})
   
   do
   echo $i >> insert_index
   
   done
   
   paste insert_index temp_list | awk '{print $1, $2, $3, $4, $5, $6}' |\
   grep "Ru1 Ru" > pool
   sed -i -e 's/^/ /' pool

   mv Ru1_list Ru1
   rm insert_index *_list

}

   formatCIF $1

findRu (){

   Ru1_index=$(shuf pool | awk 'NR==1 {print $1}')

   grep " ${Ru1_index} Ru1 Ru" pool > Ru1_d_list

   awk -f calcdist.awk Ru1_d_list pool | grep "0.00000\|1.00000"  | awk '{print $2}' > Ru1_d_index_ext
   
   while read file
   do
   grep "^ $file Ru1" pool 
   done < Ru1_d_index_ext > Ru1_d_list_new

   awk -f calcdist.awk Ru1_d_list_new pool > temp
   awk '{print $3}' temp > temp2 
   sed -i '/^$/d' temp2 
   index=$(wc -l temp2 | awk '{print $1}')
   head -n ${index} temp | grep "0.31128\|0.36105\|0.39582" | awk '{print $2}' > Ru1_neigh
   rm temp*
   
   while read file
   do
   grep "^ $file Ru1" pool 
   done < Ru1_neigh > neigh_list

   awk -f calcdist.awk neigh_list pool | grep "0.00000\|1.00000"  | awk '{print $2}' > Ru1_neigh_new 

   while read file
   do
   grep "^ $file Ru1" pool 
   done < Ru1_neigh_new > neigh_list_new

   cat neigh_list_new Ru1_d_list_new  > remove_list 

   while read file 
   do
   sed -i -e "/^ $file/d" pool
   done < remove_list

   head -n 1 Ru1_d_list >> cum_list 
   rm neigh* Ru1* remove_list 
}
 
for i in $(seq 1 $2)
do
  findRu
done

awk '!seen[$0]++' cum_list > master_d_list

rm pool cum_list
