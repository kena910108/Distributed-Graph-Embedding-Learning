import networkx as nx
import nxmetis
import itertools
from operator import itemgetter

def sorted_outputlandmark(G,landmark_foreach_subgraph):
    selected_nodes=[]
    sorted_nodes=sorted(G.degree_iter(),key=itemgetter(1),reverse=True)
    #print sorted_nodes
    for i in range(landmark_foreach_subgraph):
    	#print "dictionary check"
    	#print sorted_nodes[i][0]
    	#print sorted_nodes[i][1]
        selected_nodes.append(sorted_nodes[i])
    #print selected_nodes
    return selected_nodes



if __name__ == '__main__':

    partition=4 #balance_partition_number
    landmark_foreach_subgraph=10#lankmark_number_foreach_subgraph
    #partition
    # read in graph
    G = nx.Graph()
    G = nx.read_edgelist("release-youtube-links.txt", nodetype=int) #read_in_graph_file
    print("Built graph G")
    g=nxmetis.partition(G,partition)
    print("Partition Finish")
    for i in range(0,partition):
    	name='graph_'+str(i)+'.txt'
    	if(len(g[1][i])==1):
    		print("only one node")
    		fo= open(name,"wb")
    		fo.write(str(g[1][i]))
    		fo.close()
    	else:
    		fo= open(name,"wb")
    		subgraphnodes=[]
    		for nodes in g[1][i]:
    			subgraphnodes.append(nodes)
    			#print subgraphnodes

    		print("This is node number for graph "+str(i))
    		print(len(subgraphnodes))
    		H=G.subgraph(subgraphnodes)
    		for alledge in H.edges():
    			fo.write(str(alledge[0])+' '+str(alledge[1])+' '+str(1)+'\n')
    ##################################

    #centrality
    all_landmark=[]
    for i in range(0,partition):
        name='graph_'+str(i)+'.txt'
        G = nx.Graph()
        G=nx.read_weighted_edgelist(name, nodetype=int)
        print('Built Subgraph ',str(i))
        #degreecentrality=nx.degree_centrality(G)
        subgraph_landmark=sorted_outputlandmark(G,landmark_foreach_subgraph)
        for nodes in subgraph_landmark:
            all_landmark.append(nodes[0])
        fo= open(name,"wb")
        for nodes in subgraph_landmark:
            for edges in G.edges(nodes):
				#print edges
                fo.write(str(edges[0])+' '+str(edges[1])+' '+str(1)+'\n')
        fo.close()
        fo= open(name,"a")
        for edges in G.edges():
            if edges[0] not in subgraph_landmark and edges[1] not in subgraph_landmark:
                fo.write(str(edges[0])+' '+str(edges[1])+' '+str(1)+'\n')
        fo.close()
		#####################################################################################################here finish
    

    fo= open("landmarks.txt", "wb") #File to save landmark
    for outputlandmark in all_landmark:
    	#print outputlandmark
        fo.write(str(outputlandmark)+'\n')
    fo.close()

    		
 
    ################################

    #calculate landmark distance
    G = nx.Graph()
    G = nx.read_edgelist("release-youtube-links.txt", nodetype=int) #read in graph again
    print('Built graph G')
    nodes_a=set()
    nodes_b=set()
    with open("landmarks.txt") as fp: #read lankmark file
    	for line in fp:
    		nodes_a.add(int(line))
    		nodes_b.add(int(line))
    print("finish reading lankmark")
    Combination=list(itertools.product(nodes_a,nodes_b))
    Real_Combination=set(tuple(sorted(p)) for p in Combination)
    fo = open("landmark_distance.txt","wb") #save graph only with landmark
    for pairs in Real_Combination:
    	if(pairs[0]!=pairs[1]):
    		path_length=nx.shortest_path_length(G,pairs[0],pairs[1])
    		fo.write(str(pairs[0])+" "+str(pairs[1])+" "+str(path_length)+"\n")
    fo.close()
