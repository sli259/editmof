    # Use the diffusion coefficient calculated from RASPA package to simulate random diffusion of particales. 
    # Usage:
    # python 2D_walk.py -a 20 -r 3 -n 10
    # Created a 20 * 20 lattice grid with 10 random defects. Each defect has a radius of 3. 

    The code also makes two figures, one shows the original lattice grid. One with the simulated random diffusion path. 
    The overall diffusion path was defined given slightly higher priority to move forward. 
    (Forward: 36.4%, vertical: 34.8%, backward: 28.8%)
    The local diffusion path was defined by given higher proiortiy to move to the neighbour gird site with higher level of defect,
    There is a 10% change of moving to lower defect site. 
