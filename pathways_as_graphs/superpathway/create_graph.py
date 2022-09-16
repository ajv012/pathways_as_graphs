import pickle 
import networkx as nx
import pdb
import matplotlib.pyplot as plt

class Edge:
    def __init__(self, source_id, target_id, attr_dict):
        self.source_id = source_id
        self.target_id = target_id
        self.attr_dict = attr_dict
    
    def _get_source(self):
        return self.source_id
    
    def _get_target(self):
        return self.target_id
    
    def _get_attr(self):
        return self.attr_dict
    
    def __eq__(self, other):
        return (self._get_source() == other._get_source()) and (self._get_target() == other._get_target())
    
    def _update_dict(self, other):
        final_dict = {}
        for key in self._get_attr():
            final_dict[key] = self._get_attr()[key] or other._get_attr()[key]
        return final_dict


class Node:
    def __init__(self, name, id, type):
        self.name = name
        self.id = id
        self.type = type 
    
    def _get_name(self):
        return self.name
    
    def _get_type(self):
        return self.type
    
    def _get_id(self):
        return self.id

def summary(G):
    print(str(G))
    print("number of components in G: {}".format(nx.number_connected_components(G.to_undirected())))
    print("is G connected? {}".format(nx.is_connected(G.to_undirected())))
    # print("diameter of G is: {}".format(nx.diameter(nx.connected_components(G.to_undirected()))))
    
    # print("number of cycles in G: {}".format(len(nx.simple_cycles(G))))

def viz_and_save(G):
    fig = plt.figure(figsize=(12,12))
    ax = plt.subplot(111)
    ax.set_title('Graph - Shapes', fontsize=10)

    nx.draw(G)

    plt.tight_layout()
    plt.savefig("Graph.png", format="PNG")
    plt.show()


# load edges and nodes
with open("/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/edges/edges.pickle", "rb") as input_file:
     edges_dict = pickle.load(input_file)
    
with open("/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/nodes/nodes.pickle", "rb") as input_file:
     nodes_dict = pickle.load(input_file)

# create graph 
G = nx.DiGraph()

# add nodes to graph 
for key in nodes_dict:
    curr_node = nodes_dict[key]
    curr_id = curr_node._get_id()
    curr_type = curr_node._get_type()
    curr_name = curr_node._get_name()

    G.add_node(curr_id, type=curr_type, name=curr_name)

# add edges to graph 
for key in edges_dict:
    curr_edge = edges_dict[key]
    u_of_edge = curr_edge._get_source()
    v_of_edge = curr_edge._get_target()
    attr_of_edge = curr_edge._get_attr()
    G.add_edge(u_of_edge, v_of_edge, **attr_of_edge)

# add edges to pathways 
with open("/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/edges/edges_to_pathways.pickle", "rb") as input_file:
     edges_to_pathways_dict = pickle.load(input_file)

for key in edges_to_pathways_dict:
    curr_edge = edges_to_pathways_dict[key]
    u_of_edge = curr_edge._get_source()
    v_of_edge = curr_edge._get_target()
    attr_of_edge = curr_edge._get_attr()
    G.add_edge(u_of_edge, v_of_edge, **attr_of_edge)

summary(G)

nx.write_gpickle(G, "/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/graph/graph_rev1.pickle")
