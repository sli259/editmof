    # editmof
    # Create random MOF frames with CreateMOF.sh
#Syntex: ./Create.sh filename number_of_frame number_of_defect
#For example:
#./Create.sh uc.cif 8 3
#Create 8 different structure fragment based on the uc.cif structure, each structure has 3 random defects.

#Stack fragment structure to one supercell with buildconf.sh
#The random fragment structures can be stacked together to sinlge supercell with buildconf.sh
#Useage: buildconf.sh filename deminsion_x, deminsion_y, deminsion_z, number_of_defect
#For example:
#./buildconf.sh uc.cif 2 2 3 3
#Uses uc.cif as the template to create 2*2*3 total fragments, each fragment has 3 random defect points. Then the total 12 fragments are stacked together to a #2-2-3 super cell. 

