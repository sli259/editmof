import random
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
from collections import defaultdict
import os

dcoef = {'v1': "0.174323", 'v2': "0.1918", 'v3': "0.1928", 'v4': "0.2155",         'v5': "0.2893", 'v6': "0.3308", 'v7': "0.347", 'v8': "0.4115", 'v9':"0.5688", 'v10': "1.0"}
D_list = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"]
D_list1 = ["v1", "v2"]
module_list1 = ["0.5688", "0.4115", "0.3470", "0.3308"]
module_list2 = ["0.3470", "0.3308", "0.2893", "0.2155"]
module_list3 = ["0.3308", "0.2893", "0.2155", "0.1928"]
d_uc = 26.6226e-8


def buildMOF(x, y, z):
    clist, mof, coord = [], [], []
    if len(z) == 0:
        for i in x:
            for j in y:
                clist.append((i,j))
    elif len(z) != 0:
        for i in x:
            for j in y:
                for k in z:
                    clist.append((i, j, k))

    for i in range(len(clist)):
        slist = ','.join([str(n) for n in clist[i]])
        coord.append(slist)
    for i in range(len(coord)):
        mof.append(random.choice(D_list1))

    dcoord = dict(zip(coord,mof))
    coef_list =[]
    for i in mof:
        coef_list.append(dcoef[i])


    return dcoord, coord, coef_list, mof


def get_key(val):
    for key, value in dcoef.items():
         if val == value:
            return key


def valid(points, p, distance):
    tx, ty = p
    if tx < 0 or ty < 0 or tx >= A or ty >= B:
        return false
    for x, y in points:
        ax = tx - x
        ay = ty - y
        if distance > math.sqrt(ax * ax + ay * ay):
            return False
    return True


def genselect(A, B, num_points, distance):
    matrix = np.random.rand(A, B)
    selected = []
    for p in range(num_points):
        best_i, best_j = -1, -1
        for i in range(A):
            for j in range(B):
                if not valid(selected, (i, j), distance):
                    continue
                elif best_i == -1 or matrix[i][j] < matrix[best_i][best_j]:
                    best_i, best_j = i, j
        if best_i != -1 and best_j != -1:
            selected.append((best_i, best_j))

    return selected


def neigh(smof, R):
    smof_x = int(smof[0])
    smof_y = int(smof[1])
    neigh = []
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            nei_mof = (smof_x + i, smof_y + j)
            if nei_mof[0] >= 0 and nei_mof[1] >=0 and nei_mof[0] < A and nei_mof[1] < A:
                neigh.append(nei_mof)
    if smof in neigh:
        neigh.remove(smof)

    return neigh



def makeRing(smof, R):
    l = [i for i in range(1, R+1)]
    p = []
    while R > 0:
        ring_out = neigh(smof, R)
        ring_in = neigh(smof, R-1)
        ring = list(set(ring_out) - set(ring_in))
        p.append(ring)
        R -= 1

    d_ring = dict(zip(l, p))

    return d_ring


def makeDir(selected, R):
    combined_dict = {}
    tp = []
    for i in range(len(selected)):
        d_ring = makeRing(selected[i], R)
        tp.append(d_ring)

    super_dict = defaultdict(list)  # uses set to avoid duplicates

    for d in tp:
        for k, v in d.items():
            super_dict[k] = list(set(super_dict[k] + v))


    for elem in super_dict.keys():
        combined_dict[elem] = super_dict[elem]


    return combined_dict


def update2D(selected, coef_list, coord, R):
    w = A
    h = B
    d = 100
    relist = np.array([float(i) for i in coef_list]).reshape(A,B)
    combined_dict = makeDir(selected, R)

    for x, y in selected:
        relist[x][y] = 1.00

    for i in combined_dict:
        neigh_ring = combined_dict.get(i)
        if int(i//(R/3)) <= 1:
            for x, y in neigh_ring:
                relist[x][y] = random.choice(module_list3)
        elif int(i//(R/3)) < 2 and int(i//(R/3)) > 1:
            for x, y in neigh_ring:
                relist[x][y] = random.choice(module_list2)
        else:
            for x, y in neigh_ring:
                relist[x][y] = random.choice(module_list1)

    new_list, mof_list = [], []
    for i in relist:
        for j in i:
            new_list.append(j)
    for i in new_list:
        mof_list.append(get_key(str(i)))
    mof_ary = np.array(mof_list).reshape(A,B)

    dcoord = dict(zip(coord,mof_list))

    return dcoord, relist, mof_ary


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
            break

    return path, dist, time, dt_list, dx_list


def plot(mof_ary, path):
    w = A
    h = B
    d = 100

    plt.figure(figsize=(w, h), dpi=d)

    tp2 = []
    for i in mof_ary:
        tp = list(int(item.split('v')[1]) for item in i)
        tp2.append(tp)

    newlist= np.array(tp2)

    color_map = plt.imshow(newlist)
    color_map.set_cmap("Blues_r")

    plt.savefig('fig_no_path.png')

    for i in path:
        x = i[0]
        y = i[1]
        newlist[y][x] = -1

    color_map = plt.imshow(newlist)
    color_map.set_cmap("Blues")
    plt.savefig('fig_path.png')


def makeplt(R, num_points):
    distance = 2 * R
    mof, clist, coord = [], [], []
    dcoord, coord, coef_list, mof = buildMOF(x, y, z)
    selected = genselect(A, B, num_points, distance)
    combined_dict = makeDir(selected, R)
    sub_list = forwardN(smof)
    neigh_D, str_list, mof_f = compNeigh(sub_list, dcoord)
    dcoord, relist, mof_ary = update2D(selected, coef_list, coord, R)
    path, dist, time, dt_list, dx_list = randwalk(smof, N, dcoord)
    plot(mof_ary, path)



def pltdata(R, num_points):
    distance = 2 * R
    mof, clist, coord = [], [], []
    dcoord, coord, coef_list, mof = buildMOF(x, y, z)
    selected = genselect(A, B, num_points, distance)
    combined_dict = makeDir(selected, R)
    sub_list = forwardN(smof)
    neigh_D, str_list, mof_f = compNeigh(sub_list, dcoord)
    dcoord, relist, mof_ary = update2D(selected, coef_list, coord, R)
    path, dist, time, dt_list, dx_list = randwalk(smof, N, dcoord)
    # output path result
    result, path_traj = [], []
    for i in path:
        cod_smof = ','.join(map(str,i))
        path_traj.append(dcoord[cod_smof])
    print(path_traj)
    nv1 = path_traj.count('v1')
    nv2 = path_traj.count('v2')
    nv3 = path_traj.count('v3')
    nv4 = path_traj.count('v4')
    nv5 = path_traj.count('v5')
    nv6 = path_traj.count('v6')
    nv7 = path_traj.count('v7')
    nv8 = path_traj.count('v8')
    nv9 = path_traj.count('v9')
    nv10 = path_traj.count('v10')

    total = sum([nv1, nv2, nv3, nv4, nv5, nv6, nv7, nv8, nv9, nv10])
    result = [total, nv1, nv2, nv3, nv4, nv5, nv6, nv7, nv8, nv9, nv10, dist, time]

    out = open('2d-walk.dat', 'w')
    print('#', total, nv1, nv2, nv3, nv4, nv5, nv6, nv7, nv8, nv9, nv10, file=out)
    print('# Time(ps) Distance (A^2)', file=out)
    for i in range(len(dt_list)):
        print(dt_list[i], dx_list[i], file=out)

    out.close()


if __name__ == '__main__':
    # Parse Command-line Input
    parser = argparse.ArgumentParser(description='Generate 2D walk plot and data')
    parser.add_argument('-a', nargs=1, help='Input lattice dimension', required=True)
    parser.add_argument('-r', nargs=1, help='Input defect ring radius', required=True)
    parser.add_argument('-n', nargs=1, help='Input number of defect rings', required=True)
    args = parser.parse_args()

    if vars(args)['r'][0] != 'NULL' and vars(args)['a'] != 'NULL' and vars(args)['n'] != 'NULL':
        A = int(vars(args)['a'][0])
        R = int(vars(args)['r'][0])
        num_points = int(vars(args)['n'][0])
        B = A
        smof = [0, int(A/2)]
        N = A*B
        tot_dist = A * d_uc
        C = 0
        x = [ i for i in range(A)]
        y = [ i for i in range(B)]
        z = [ i for i in range(C)]

        makeplt(R, num_points)

