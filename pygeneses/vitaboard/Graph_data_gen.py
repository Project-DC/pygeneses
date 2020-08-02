#Imports
import os
import numpy as np
import re
import statistics
def check_ext(f_names):
    '''
    Filter Files based on extension (.npy)

    Params
    ======
    f_name (list)
            :- list containing all the names of files
    Returns:
    ======
    filtered_names (list)
            :- list containing all file names containing .npy extension
    '''
    filtered_names = []
    for name in f_names:
        if(len(name)>4):
            if(name[-4:] == ".npy"):
                filtered_names.append(name)
    return filtered_names




def add_node(id, parent_id, fam_tree):
    '''
        Function to add a node to the graph

        Params :
        ======
        id (String)
                :- file name of the current node (to be added)

        parent_id (String)
                :- file name (minus the extension) of the parent of id

        fam_tree (Dictionary)
                :- Dictionary Containing {id: parents}

    '''
    if parent_id != None:
        parent_id = parent_id+".npy"
    if id not in fam_tree:
        fam_tree[id] =[parent_id]
    elif parent_id != []:
        fam_tree[id].append(parent_id)



def gen_fam_graph(address):
    '''
        Generate Family graph

        Params :
        ======
        address (String)
            :- Address of the folder containing the log Files

        Returns :
        ======
        fam_tree (Dictionary)
            :- Dictionary containing the family Trees. {id :[parent1, parent2]}
    '''
    #Initialise Dictionary
    fam_tree = {}
    f_names = os.listdir(address)
    f_names = check_ext(f_names)

    for f_name in f_names:
        log_values = np.load(address+'/'+f_name, allow_pickle = True)
        parents = log_values[1]
        if parents.shape ==  (2,):
            add_node(f_name, str(parents[1])+'-'+str(i[0]), fam_tree)
        elif parents.shape == (2,2):
            add_node(f_name, str(parents[0][1])+'-'+str(parents[0][0]), fam_tree)
            add_node(f_name, str(parents[1][1])+'-'+str(parents[1][0]), fam_tree)
    return fam_tree

def add_life_exp(life, tob, life_data):
    '''
        Function to add values to mean and variance

        Params :-
        =====
        life (int)
            :- The life time of the player
        tob (int)
            :- Time of birth of the player
        life_data(Dictionary)
            :- Dictionary containing the values {tob : life} for players

        Returns :-
        =====
        life_data (Dictionary)
            :- Dictionary Containing the values {tob : life} for players
    '''

    if tob not in life_data.keys():
        life_data[tob] = [life]
    else:
        life_data[tob].append(life)
    return life_data

def get_life_stats(address):
    '''
        Return various stats based on lifetime of players

        Params:
        =====
        address (String)
            :-  Address of the folder containing the log Files
        Returns:
        =====
        mean  (Dictionary)
            :- Dictionary containting the mean of lifetimes of players born at a particular time. {time_of_birth: mean}

        variance (Dictionary)
            :- Dictionary containting the variance of lifetimes of players born at a particular time. {time_of_birth: variance}

        qof   (Dictionary)
            :- Dictionary containing the Quality of life index of players born at a particular time . {time: count_qof}
    '''
    f_names = os.listdir(address)
    f_names = check_ext(f_names)
    life_data = {}
    for f_name in f_names:
        log_values = np.load(address+'/'+f_name, allow_pickle = True)
        tob, id = f_name.split('-')
        tod = log_values[-1][1]
        lifetime = tod-int(tob)
        life_data = add_life_exp(lifetime, tob, life_data)
    variance = {}
    mean = {}
    qof = {}
    for i in life_data.keys():
        if len(life_data[i]) == 1:
            variance[i] = 0
            mean[i] = life_data[i][0]
            qof[i] = 1 if life_data[i][0] >= 85 else 0
            continue
        qof[i] = sum(np.array(life_data[i])>30)
        variance[i] = statistics.stdev(life_data[i])
        mean[i] = statistics.mean(life_data[i])
    return mean, variance, qof

#Uncomment to check if the functions are working properly
'''print(get_life_stats("C:\\Users\\PD-PC\\Desktop\\pygeneses\\Players_Data"))
print("#"*70)
print(gen_fam_graph("C:\\Users\\PD-PC\\Desktop\\pygeneses\\Players_Data")) '''
