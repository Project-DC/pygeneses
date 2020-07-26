#Imports
import os
import numpy as np
import re

def check_ext(f_names):
    #Filter Files based on extension (.npy)
    '''
        Input:
            f_name :- list containing all the names of files
        Returns:
            filtered_names :- list containing all file names containing .npy extension
    '''
    filtered_names = []
    for name in f_names:
        if(len(name)>4):
            if(name[-4:] == ".npy"):
                filtered_names.append(name)
    return filtered_names


#Initialise Dictionary
Fam_Tree = {}

def add_node(id, parent_id):
    #Function to add a node to the graph
    '''
        Inputs:
            id :- file name of the current node (to be added)
            parent_id :- file name (minus the extension) of the parent of id
    '''
    if parent_id != None:
        parent_id = parent_id+".npy"
    if id not in Fam_Tree:
        Fam_Tree[id] =[parent_id]
    elif parent_id != []:
        Fam_Tree[id].append(parent_id)



def gen_fam_graph(address):
    #Generate Family graph
    '''
        Inputs:
            address :- Address of the folder containing the log Files
        Returns:
            Fam_Tree :- Dictionary containing the family Trees. {id :[parent1, parent2]}
    '''
    f_names = os.listdir(address)
    f_names = check_ext(f_names)
    for f_name in f_names:
        values = np.load(address+'/'+f_name, allow_pickle = True)
        i = values[0]
        if i[-1] == []:
            add_node(f_name,None)
        else:
            for j in i[-1]:
                add_node(f_name, str(j[1])+'-'+str(j[0]))
    return Fam_Tree
