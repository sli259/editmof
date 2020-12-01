    # Use the diffusion coefficient calculated from RASPA package to simulate random diffusion of particales. 
    #### 2D_walk.py
    # Usage:
    # python 2D_walk.py -a 20 -r 3 -n 10
    # Created a 20 * 20 lattice grid with 10 random defects. Each defect has a radius of 3 that expand on the lattice grid. 
    

    The code also makes two figures and a data file "2d-walk.dat", one figure shows the original lattice grid. The other figure use the same layout with the simulated random diffusion path. 
    The overall diffusion path was defined given slightly higher priority to move forward. 
    (Forward: 36.4%, vertical: 34.8%, backward: 28.8%)
    The local diffusion path was defined by given higher priority to move to the neighbour gird site with more defects,
    There is also a 10% change of abnormal behavior which move to lower defect site. 
    The data file contains the path trajectory and the mean square displacement. 
    
    #### 2d_random.py
    # Usage:
    # python 2d_random.py -a 20
    # This make a 20 by 20 lattice grid with randomly distributed lattice point, the diffusion behavior is same to the above.
    
    
    
    #### mult_run.sh violineplt.py
    # Generally, multiple runs should be applied to generate data for analysis, here the mult_run.sh make 100 50*50 lattice grid.
      Each grid has 20 defect rings expand to 3 unit cell length. The path trajectory are combined to the data file, which can be plot by the violineplt.py
