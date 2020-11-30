#!/usr/bin/env python
import random 
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

dcoef = {'v1': "0.174323", 'v2': "0.1918", 'v3': "0.1928", 'v4': "0.2155",         'v5': "0.2893", 'v6': "0.3308", 'v7': "0.347", 'v8': "0.4115", 'v9':"0.5688", 'v10': "1.0"}
D_list = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"]

d_uc = 26.6226e-8

def buildMOF(x, y, z):
    mof, clist, coord = [], [], []
    if len(z) == 0:
        for i in x:
            for j in y:
                clist.append([i,j])
    elif len(z) != 0:
        for i in x:
            for j in y:
                for k in z:
                    clist.append([i, j, k])
    for i in range(len(clist)):
        slist = ','.join([str(n) for n in clist[i]])
        coord.append(slist)
#    random.seed(10) 
    for i in range(len(coord)):
        mof.append(random.choice(D_list))
        
    dcoord = dict(zip(coord,mof))
    coord_split = [coord[i].split(',') for i in range(len(coord))]
    coef_list =[]
    for i in mof:
        coef_list.append(dcoef[i])
        
    return dcoord, mof, coord, coef_list


# In[15]:


def find2Dneigh(smof):
    neigh_list = []
    smof_x = int(smof[0])
    smof_y = int(smof[1])
    mol1 = [smof_x, smof_y-1]
    mol2 = [smof_x+1, smof_y-1]
    mol3 = [smof_x+1, smof_y]
    mol4 = [smof_x+1, smof_y+1]
    mol5 = [smof_x, smof_y+1]
    list1 = [mol1, mol2, mol3, mol4, mol5]
    
    for i in range(len(list1)):
        if (list1[i][1] != B) and (list1[i][0] != A) and (list1[i][1] != -1):
            neigh_list.append(list1[i]) 
    
    return neigh_list


# In[16]:


def forwardN(smof):
    n = 3
    f = int((1/3)*100 + n)
    v = int((1/3)*100 + n/2)
    b = 100 - f - v
    sub_list = []
    smof_x = int(smof[0])
    smof_y = int(smof[1])
    pk = random.randint(1,100)
    if smof_x == 0 and smof_y != 0:
        if pk <= 30:
            x = 0
            y = [1] 
        else:
            x = 1
            y = [0, 1]
    elif smof_x != 0 and smof_y == 0:
        if pk <= 30:
            x = 0
            y = [1]
        else: 
            x = 1
            y = [0, 1]
    elif smof_x == 0 and smof_y == 0:
        if pk <= 30:
            x = 0
            y = [1]
        else: 
            x = 1
            y = [0, 1]
    else: 
        if pk <= b:
            x = -1
            y = [-1, 0, 1]
        elif pk > b and pk <= b + v:
            x = 0
            y = [-1, 1]
        else:
            x = 1
            y = [-1, 0, 1]
      
    for i in y: 
        nei_mof1 = (smof_x + x, smof_y + i)
        if nei_mof1[0] >= 0 and nei_mof1[1] >=0 and nei_mof1[0] < A and nei_mof1[1] < A:
            sub_list.append(nei_mof1)
            
    return sub_list


# In[17]:


#sub_list = [(0, 26)]

def compNeigh(sub_list, dcoord):
    neigh_D, str_list, mof_f = [], [], []
    D_list = []
    local_d = {}

    for i in range(len(sub_list)):
        str_list_i = ','.join([str(n) for n in sub_list[i]])
        str_list.append(str_list_i) # '1,1'
        a = dcoord[str_list_i] # 6.0

        neigh_D.append(str(dcoord[str_list_i])) #'4'

        D_list.append(str(a))

    # find the next mof to walk to:
        d_t = dict(zip(str_list, D_list))
        dict2 = {}
        names = set(d_t.values())
        d = {}
        for n in names:
            d[n] = [k for k in d_t.keys() if d_t[k] == n ]
    pool = []
    
    if 'v10' in d:
        a = random.randint(1,100)
        if a <= 90:
            temp_f = random.choice(d.get('v10'))
            mof_f = list(map(int, temp_f.split(',')))
        else:
            new_d = {key:val for key, val in d.items() if key != 'v10'}
            for i in new_d:
                f = int(len(new_d[i]))*int(i[1])
                for j in range(f):
                    pool.append(str(new_d[i])[1:-1].replace("'", ""))
            temp = random.choice(random.choice(pool).split(', '))
            mof_f = list(map(int, temp.split(',')))

    else:
        for i in d:
            f = int(len(d[i]))*int(i[1])
            for j in range(f):
                pool.append(str(d[i])[1:-1].replace("'", ""))
                
        tp, tp2 = [], []
        for i in pool:
            tp.append(list(i.split(', ')))
        for i in tp:
            for j in i:
                tp2.append(j)
        temp = random.choice(tp2)
        mof_f = list(map(int, temp.split(',')))
    
    
    return neigh_D, str_list, mof_f



# In[18]:


def caldist(mof1, mof2):
    dist = math.sqrt(((mof2[0]-mof1[0])**2) + ((mof2[1]-mof1[1])**2)) 
    #for 3D walk
#    dist = math.sqrt(((mof2[0]-mof1[0])**2) + ((mof2[1]-mof1[1])**2))  + ((mof2[2]-mof1[2])**2))
    return dist


def randwalk(smof, N, dcoord):
    path = [smof]
    dist = 0
    temp = 0
    time1 = 0
    time1_list, time2_list = [], []
    dt_list, dx_list = [], []
    time2 = 0
    time = 0
    sub_list = forwardN(smof)
    for i in range(N):
        neigh_D, str_list, mof_f = compNeigh(sub_list, dcoord)
        cod_smof = ','.join(map(str,smof))
        cod_mof_f = ','.join(map(str,mof_f))
        D_smof = dcoef[dcoord[cod_smof]]
        D_mof_f = dcoef[dcoord[cod_mof_f]]
        dx = caldist(mof_f, smof)
        if dcoord[cod_smof] != 'v10':
            d_time = (dx**2)/(4*float(D_smof))
            time1_list.append((dx**2)/(4*float(D_smof)))
            time1 += (dx**2)/(4*float(D_smof))
        elif dcoord[cod_mof_f] == 'v10':
            d_time = (dx)/(2*float(D_mof_f))
            time2_list.append((dx)/(2*float(D_mof_f)))
            time2 += (dx)/(2*float(D_mof_f))
        elif dcoord[cod_smof] == 'v10':
            d_time = (dx)/(2*float(D_smof))
            time2_list.append((dx)/(2*float(D_smof)))
            time2 += (dx)/(2*float(D_smof))

        temp += d_time
        dt_list.append(round(temp, 3))

       
        dist += caldist(mof_f, smof)
        dx_list.append(round(dist, 3))
        
        sub_list = forwardN(mof_f)
        
        if smof in sub_list:
            sub_list.remove(smof)
        else:
            pass
        smof = mof_f
        path.append(smof)
        time = time1 + time2
        if len(sub_list) == 0 or (mof_f[0] == A-1):
#             print("Reach the boundary before reach the defined iteration, total walk:", i+1, "steps")
            break
        
    return path, dist, time, dt_list, dx_list


# In[33]:


def cmap(path, coef_list):
    w = A 
    h = B 
    d = 100
#    plt.figure(figsize=(w/5, h/5), dpi=d)
    relist = np.array([float(i) for i in coef_list]).reshape(A,B)
    
    color_map = plt.imshow(relist)
    color_map.set_cmap("Blues_r")
    
    plt.savefig('temp1.png')
    
    for i in path:
        x = i[0]
        y = i[1]
        relist[y][x] = 0 
        
    color_map = plt.imshow(relist)
    color_map.set_cmap("Blues_r")
#    plt.colorbar()
#    plt.show()
    plt.savefig('temp2.png')

    


# In[23]:


if __name__ == '__main__':
    # Parse Command-line Input
    parser = argparse.ArgumentParser(description='Generate 2D walk plot and data')
    parser.add_argument('-a', nargs=1, help='Input lattice dimension', required=True)
    args = parser.parse_args()

    if vars(args)['a'][0] != 'NULL':
        A = int(vars(args)['a'][0])
        B = A
        smof = [0, int(A/2)]
        N = A*B*10
        tot_dist = A * d_uc
        C = 0
        x = [ i for i in range(A)]
        y = [ i for i in range(B)]
        z = [ i for i in range(C)]
        dcoord, mof, coord,  coef_list = buildMOF(x, y, z)
        sub_list = forwardN(smof)
        neigh_D, str_list, mof_f = compNeigh(sub_list, dcoord)
        path, dist, time, dt_list, dx_list = randwalk(smof, N, dcoord)
        cmap(path, coef_list) 


# In[ ]:





# In[ ]:




