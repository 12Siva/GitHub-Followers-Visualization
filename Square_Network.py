import matplotlib.pyplot as plt
import networkx as nx
#
# # simple script to draw a square using the networkx library
# G = nx.DiGraph() # directed graph
#
#
# G.add_nodes_from([0, 1, 2, 3]) # nodes
# G.add_edges_from([(0,1), (1,2), (2,3), (3,0)]) # edges
#
# # labels for each of the nodes
# labels = {}
# labels[0] = 'a'
# labels[1] = 'b'
# labels[2] = 'c'
# labels[3] = 'd'
#
# nx.draw_networkx(G, node_size=500, with_labels=True, node_color='y')
# #l = nx.draw_networkx_labels(G, pos=nx.spring_layout(G), labels=labels, font_size=17)
#
# # matplotlib options for the final plot
#
# plt.axis('off')
# plt.show()
G=nx.path_graph(4)
shells=[[0],[1,2,3]]
pos=nx.shell_layout(G,shells)
nx.draw(G)
plt.show()