# Import required libraries
import os
import glob
import numpy as np
import re
import statistics
from collections import OrderedDict
import json

def add_node(id, parent_id, fam_tree):
    """
    Function to add a node to the graph

    Params
    ======
    id        (str)
        : file name of the current node (to be added)

    parent_id (str)
        : file name (minus the extension) of the parent of id

    fam_tree  (dict)
        : Dictionary Containing {id: parents}

    """
    # Check if the parent_id is not None
    if parent_id != None:
        # Add the extension (.npy) to the parent_id
        parent_id = parent_id + ".npy"
    # Check if id is not in fam_tree
    if id not in fam_tree:
        # Add a new entry in the dict`
        fam_tree[id] = [parent_id]
    elif parent_id != []:
        # If the key already exists, append the parent_id to the value
        fam_tree[id].append(parent_id)


def gen_fam_graph(address):
    """
    Generate Family graph

    Params
    ======
    address (str)
        : Address of the folder containing the log Files

    Returns :
    ======
    fam_tree (dict)
        : Dictionary containing the family Trees. {id :[parent1, parent2]}
    """

    # Initialise Dictionary
    fam_tree = {}
    # Get file names from the directory
    f_names = os.listdir(address)
    # Filter out non .npy files
    f_names = check_ext(f_names)
    # Iterate over all the file names in the list f_names
    for f_name in f_names:
        # Load the values of a file
        log_values = np.load(address + "/" + f_name, allow_pickle=True)
        # Extract parents from log_values
        parents = log_values[1]
        # Check if there exists only one parent
        if parents.shape == (2,):
            # Make an entry in the fam_tree Dictionary
            add_node(f_name, str(parents[1]) + "-" + str(parents[0]), fam_tree)
        # Check if there exist two parents
        elif parents.shape == (2, 2):
            # Make entries in the fam_tree Dictionary
            add_node(f_name, str(parents[0][1]) + "-" + str(parents[0][0]), fam_tree)
            add_node(f_name, str(parents[1][1]) + "-" + str(parents[1][0]), fam_tree)
    return fam_tree


def add_life_exp(life, tob, life_data, id):
    """
    Function to add values to mean and variance

    Params
    ======
    life      (int)
        : The life time of the player
    tob       (int)
        : Time of birth of the player
    life_data (dict)
        : Dictionary containing the values {tob : life} for players
    id        (string)
        : String containing the name of the player

    Returns
    =======
    life_data (dict)
        : Dictionary Containing the values {tob : life} for players
    """
    # Check if tob already exists in life_data or not
    if tob not in life_data.keys():
        life_data[tob] = [[life],[id]]
    else:
        life_data[tob][0].append(life)
        life_data[tob][1].append(id)

    return life_data


def get_life_stats(address):
    """
    Return various stats based on lifetime of players

    Params
    ======
    address (str)
        : Address of the folder containing the log Files

    Returns
    =======
    mean     (dict)
        : Dictionary containting the mean of lifetimes of players born at a particular time. {time_of_birth: mean}

    variance (dict)
        : Dictionary containting the variance of lifetimes of players born at a particular time. {time_of_birth: variance}

    qof      (dic)
        : Dictionary containing the Quality of life index of players born at a particular time . {time: count_qof}
    """

    # Get all npy files from address
    f_names = glob.glob(os.path.join(address, '*.npy'))

    life_data = {}

    for f_name in f_names:
        # Load log file
        log_values = np.load(f_name, allow_pickle=True)

        # Extract tob (time of birth) and id of the player
        tob, id = os.path.basename(f_name).split("-")
        tob = int(tob)

        # Extract the tod (time of death) of the player
        tod = log_values[-1][1]

        # Calculate the lifetime of the player
        lifetime = tod - tob

        # Update life_data
        life_data = add_life_exp(lifetime, tob, life_data, id)

    # Initialise dictionaries to store various statistics
    variance = []
    mean = []
    qof = []

    for j in life_data.keys():
        # Check if jth index holds information of only one player
        if len(life_data[j][0]) == 1:
            variance.append({"tob": j, "value": 0 , "agents": [life_data[j][1]]})
            mean.append({"tob": j, "value": life_data[j][0][0], "agents": [life_data[j][1]]})
            qof.append({"tob": j, "value": int(1) if life_data[j][0][0] >= 85 else int(0), "agents": [life_data[j][1]]})
            continue

        qof.append({"x": j, "y": int(sum(np.array(life_data[j][0])) > 85) , "agents": life_data[j][1]})
        variance.append({"x": j, "y": statistics.stdev(life_data[j][0]), "agents": life_data[j][1]})
        mean.append({"x": j, "y": statistics.mean(life_data[j][0]), "agents": life_data[j][1]})

    # Return the mean, variance and qof
    mean = json.dumps(mean, indent=2)
    variance = json.dumps(variance, indent=2)
    qof = json.dumps(qof, indent=2)
    return mean, variance, qof


# Uncomment to check if the functions are working properly
if __name__ == "__main__":
    print(get_life_stats("C:\\Users\\PD-PC\\Desktop\\Projects\\pygeneses\\Players_Data"))
    print("#"*70)
    print(gen_fam_graph("C:\\Users\\PD-PC\\Desktop\\Projects\\pygeneses\\Players_Data"))
