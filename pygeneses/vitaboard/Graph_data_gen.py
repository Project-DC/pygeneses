#Imports
import os
import numpy as np
import re
import statistics
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




def add_node(id, parent_id, Fam_Tree):
    #Function to add a node to the graph
    '''
        Inputs:
            id :- file name of the current node (to be added)
            parent_id :- file name (minus the extension) of the parent of id
            Fam_Tree :- Dictionary Containing {id: parents}
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
    #Initialise Dictionary
    Fam_Tree = {}

    f_names = os.listdir(address)
    f_names = check_ext(f_names)

    for f_name in f_names:
        values = np.load(address+'/'+f_name, allow_pickle = True)
        i = values[1]
        if i.shape ==  (2,):
            add_node(f_name, str(i[1])+'-'+str(i[0]), Fam_Tree)
        elif len(i) == (2,2):
            add_node(f_name, str(i[0][1])+'-'+str(i[0][0]), Fam_Tree)
            add_node(f_name, str(i[1][2])+'-'+str(i[1][3]), Fam_Tree)
    return Fam_Tree

def add_life_exp(life, tob, life_data):
    #Function to add values to mean and variance
    '''
        Inputs :-
            life        :- The life time of the player
            tob         :- Time of birth of the player
            life_data   :- Dictionary containing the values {tob : life} for players
    '''

    if tob not in life_data.keys():
        life_data[tob] = [life]
    else:
        life_data[tob].append(life)
    return life_data

def get_life_stats(address):
    #Return various stats based on lifetime of players
    '''
        Inputs:
            address :-  Address of the folder containing the log Files
        Returns:
            mean :- Dictionary containting the mean of lifetimes of players born at a particular time. {time_of_birth:mean}
            variance :- Dictionary containting the variance of lifetimes of players born at a particular time. {time_of_birth:variance}
    '''
    f_names = os.listdir(address)
    f_names = check_ext(f_names)
    life_data = {}
    for f_name in f_names:
        vals = np.load(address+'/'+f_name, allow_pickle = True)
        tob, id = f_name.split('-')
        tod = vals[-1][1]
        life = tod-int(tob)
        life_data = add_life_exp(life, tob, life_data)
    variance = {}
    mean = {}
    for i in life_data.keys():
        if len(life_data[i]) == 1:
            variance[i] = 0
            mean[i] = life_data[i][0]
            continue
        variance[i] = statistics.stdev(life_data[i])
        mean[i] = statistics.mean(life_data[i])
    return mean, variance

#Uncomment to check if the functions are working properly
'''print(get_life_stats(r"C:\Users\PD-PC\Desktop\pygeneses\Players_Data"))
print("#"*100)
print(gen_fam_graph(r"C:\Users\PD-PC\Desktop\pygeneses\Players_Data"))'''
