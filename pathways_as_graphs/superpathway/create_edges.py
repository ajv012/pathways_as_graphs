import networkx as nx
import pandas as pd
import pdb
import pickle
import numpy as np

def _compare_dicts(dict1, dict2):
        return np.array([not(dict1[key] ^ dict2[key]) for key in dict1]).all()

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
    

# load idenitifies 
with open("/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/nodes/node_identifiers.pickle", "rb") as input_file:
     identifiers = pickle.load(input_file)

# define the proteins -> complexes edges 
df_compositions = pd.read_csv("/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/edges/edges_raw.txt", sep='\t', header=None)
df_compositions.rename(columns={0: "parent", 1:"child", 2: "type"}, inplace=True)
df_compositions["type"].value_counts()

edge_types = {
    "component>":"component",
    "member>":"component", 
    "-a>":"activation", 
    "-a|":"inhibition", 
    "-t>":"transcriptional_activation",
    "-t|":"transcriptional_inhibition",
    }

edge_attr_dict_raw = {
    "component":False,
    "activation":False,
    "inhibition":False,
    "transcriptional_activation":False,
    "transcriptional_inhibition":False
    }

df_compositions["type"] = df_compositions["type"].apply(lambda x : edge_types[x])

list_of_edges = []
print("Starting edge production...")
for edge_type in edge_attr_dict_raw:
    
    df_curr = df_compositions[df_compositions["type"] == edge_type]
    ignore = []
    
    for parent_name in df_curr["parent"]:
        if not (parent_name in ignore):
            parent_id = identifiers[parent_name]
            df_temp = df_curr[df_curr["parent"] == parent_name]

            for i in df_temp.index:
                child_name = df_temp.loc[i, "child"]
                child_id = identifiers[child_name]
                attr_dict = edge_attr_dict_raw.copy()
                attr_dict[edge_type] = True
                list_of_edges.append(Edge(source_id=parent_id, target_id=child_id, attr_dict=attr_dict))
            ignore.append(parent_name)

    print("Completed edge type {}".format(edge_type))


# combine same edges by attributes 
print('Combining edges...')
ignore_idx = []
for i in range(len(list_of_edges)):
    if i not in ignore_idx:
        curr_edge = list_of_edges[i]
        for j in range(i, len(list_of_edges)):
            if curr_edge == list_of_edges[j]:
                if i!= j: 
                    ignore_idx.append(j)
                    curr_edge._update_dict(list_of_edges[j])

dict_of_edges = {}
count = 0
for i in range(len(list_of_edges)):
    if not (i in ignore_idx):
        dict_of_edges[count] = list_of_edges[i]
        count += 1
    
pdb.set_trace()

save_dir = "/media/hdd1/Anurag/Projects/Code/reactome_gnn/superpathway/data/edges/edges.pickle"
with open(save_dir, 'wb') as handle: 
    pickle.dump(dict_of_edges, handle, protocol=pickle.HIGHEST_PROTOCOL)




