# Distributed-Graph-Embedding-Learning


Algorithm:
	Partition original graph to k subgraphs.
	For every subgraph, select landmarks. 
	Construct basis graph G_B={V,E}, where V is the set of all selected landmarks in step 2 and edge weight is sigmoid function of original graph’s Adamic/Adar index.
	Running LINE to construct k local embeddings (subgraph embedding) and landmark graph embedding.
	Running Lasso to compute “positive” weight w_(i,j) summarizing the contribution of landmark j to vertex i in local embedding space.
	Reconstruct global embedding by linear combination of landmark graph embedding and weights.

Implementation:
	Python2.7 
	Python3
	Networkx 1.10 
	LINE: Install on Github





partition.py
Run:
python partition.py k j
	-k, number of subgraphs
	-j, number of degree centrality landmarks per subgraph
Note: k*j = #total landmarks (#nodes in basis graph) 
Input: youtube-links.txt
Output: basis_graph.txt、graph_0.txt、graph_1.txt、....、graph_k-1.txt
Note: 
	Partition is obtained by nxmetis.partition in NetworkX-METIS
	landmark graph is aclique among landmarks with edge weight induced by sigmoid of adamic_adar。

Reference:
https://github.com/tangjianpku/LINE/blob/master/linux/train_youtube.sh
https://networkx-metis.readthedocs.io/en/latest/reference/generated/nxmetis.partition.html


lasso.py
Run:
python lasso.py k 
	-k, number of subgraphs
	
Note: 
	multi-thread is set as 60



Input: subgraph embedding and landmark graph embedding

Output: global embedding

Reference:
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html


