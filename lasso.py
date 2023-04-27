from numpy.linalg import pinv
from numpy.linalg import matrix_rank
import numpy as np
from numpy import array
import struct
import sys,time
import threading
from sklearn import linear_model

#################################################################
def computing_weight(s,e,i):
    global local_graph_arr
    global local_landmark_arr
    global global_landmark_arr
    global global_embedding
    start = time.time()
    for n in range(s,e):
        clf = linear_model.Lasso(alpha=0.001,positive = True)
        clf.fit(local_landmark_arr[i].T, local_graph_arr[i][n])
        global_embedding[i][n] = np.dot(global_landmark_arr[i].T,clf.coef_)
        #global_embedding[i][n] = local_graph_arr[i][n]
        if s == 0 and i ==0 and n%100 == 0:
            end = time.time()
            sys.stdout.write("%d %d\r"%(n,start-end))
            sys.stdout.flush()

def read_global_landmark_embedding():
    g = []
    fo= open('local_landmark.txt',"r")
    line = fo.readline()
    number = int(line.split()[0])
    dimension = int(line.split()[1])
    print(number,dimension)

    for s in range(0,number):
        c = fo.read(1)
        x = []
        while c!=' ':
            x.append(c)
            c = fo.read(1)
        xt =''.join(x)
        tmp = [struct.unpack('<d',fo.read(8))[0] for k in range(0, 128)]
        fo.read(1)
        tmp.insert(0, float(xt))
        print(tmp)
        g.append([float(n) for n in tmp])
    fo.close()
    return g
def read_embedding(partition):

    local_graph = [[] for i in range(partition)]
    local_landmark = [[] for i in range(partition)]
    global_landmark = [[] for i in range(partition)]
    global local_name 
    global landmark_name 
    global dimension
    local_name = [[] for i in range(partition)]
    landmark_name = [[] for i in range(partition)]
    g = read_global_landmark_embedding()
    g0 = [x[0] for x in g]

    for i in range(0,partition):
        name='local_'+str(i)+'.txt'
        #name='vec_1st_wo_norm.txt'############### needed to be deleted 
        fo= open(name,"r")
        line = fo.readline()
        number = int(line.split()[0])
        dimension = int(line.split()[1])

        print(number, dimension)
        for j in range(0,number):
            c = fo.read(1)
            x = []
            while c!=' ':
                x.append(c)
                c = fo.read(1)
            xt =''.join(x)
            tmp = [struct.unpack('<d',fo.read(8))[0] for k in range(0, 128)]
            fo.read(1)
            if float(xt) not in g0:
                local_name[i].append(xt)
                local_graph[i].append(array([float(n) for n in tmp]))
            else:
                landmark_name[i].append(xt)
                g[g0.index(float(xt))].pop(0)
                global_landmark[i].append(array(g[g0.index(float(xt))]))
                local_landmark[i].append(array([float(n) for n in tmp]))
        fo.close()


    global local_graph_arr
    global local_landmark_arr
    global global_landmark_arr
    local_graph_arr = [array([e for e in xi]) for xi in local_graph]
    local_landmark_arr = array([array([e for e in xi]) for xi in local_landmark])
    global_landmark_arr = array([array([e for e in xi]) for xi in global_landmark])
    for i in range(partition):
        print(len(local_graph_arr[i]))
    print(local_landmark_arr.shape)
    print(global_landmark_arr.shape)

def write_file(partition):   
    global local_name 
    global landmark_name 
    global dimension
    print("write file")
    fv= open("test_positive.txt","wb")
    number = 0
    for i in range(partition):
        number = number + len(local_graph_arr[i])
    fv.write(str(number)+' '+str(dimension)+'\n')
    for i in range(0,len(global_embedding)):
        for j in range(0,len(global_embedding[i])):
            sys.stdout.write("%d %d\r"%(i,j))
            sys.stdout.flush()
            fv.write(str(int(local_name[i][j]))+' ')
            for k in range(0,dimension):
                fv.write(struct.pack('<f',global_embedding[i][j][k]))
            fv.write('\n')
    for i in range(0,len(global_landmark_arr)):
        for j in range(0,len(global_landmark_arr[i])):
            fv.write(str(int(local_name[i][j]))+' ')
            for k in range(0,dimension):
                fv.write(struct.pack('<f',global_landmark_arr[i][j][k]))
            fv.write('\n')

    fv.close()

def process(partition):
    global local_graph_arr
    global local_landmark_arr
    global global_landmark_arr
    global global_embedding
    n_thr = int(60/partition)
    threads = []

    read_embedding(partition)
    global_embedding = local_graph_arr[:]
    for i in range(partition):
        s = 0
        r = int(local_graph_arr[i].shape[0]/n_thr)
        print("r",r)
        for j in range(n_thr):
            if s+r > local_graph_arr[i].shape[0]:
                threads.append(threading.Thread(target = computing_weight, args = (s,local_graph_arr[0].shape[0],i)))
            else:
                threads.append(threading.Thread(target = computing_weight, args = (s,s+r,i)))
            threads[i*n_thr+j].start()
            s = s+r
    for i in range(n_thr):
        threads[i].join()
    write_file(partition)
    print("finish")


if __name__ == '__main__':
    partition = int(sys.argv[1])
    process(partition)