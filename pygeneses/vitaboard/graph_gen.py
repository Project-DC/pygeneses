# Import required libraries
import os
import numpy as np
import re
import statistics
from collections import OrderedDict
import json

def check_ext(f_names):
    """
    Filter Files based on extension (.npy)

    Params
    ======
    f_name         (list)
        : list containing all the names of files
    Returns:
    ======
    filtered_names (list)
        : list containing all file names containing .npy extension
    """

    filtered_names = []

    for file_name in f_names:
        if len(file_name) > 4:
            # Check if the file name has a .npy extension
            if file_name[-4:] == ".npy":
                # Append the file name to list of valid names
                filtered_names.append(file_name)
    return filtered_names


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
    # Check if tob does not already exist as a key in the dictionary life_data
    if tob not in life_data.keys():
        # Add a new entry in life_data
        life_data[tob] = [[life],[id]]
    else:
        # If tob exists as a key in life_Data, append 'life' to the value at key tob
        life_data[tob][0].append(life)
        life_data[tob][1].append(id)
    # Return the dictionary life_data
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
    # Get the names of all files located in the directory stored in 'address'
    f_names = os.listdir(address)
    # Filter out files that do not have .npy extension
    f_names = check_ext(f_names)
    # Initialise a dict life_data
    life_data = OrderedDict()
    # Iterate over all file names stored in the list f_names
    for f_name in f_names:
        # Load the values stored in the file named f_name
        log_values = np.load(address + "/" + f_name, allow_pickle=True)
        # Extract tob (time of birth) and id of the player
        tob, id = f_name.split("-")
        # Extract the tod (time of death) of the player
        tod = log_values[-1][1]
        # Calculate the lifetime of the player
        lifetime = tod - int(tob)
        # Update life_data
        life_data = add_life_exp(lifetime, tob, life_data, id)
    # Initialise dictionaries to store various statistics
    variance = {}
    mean = {}
    qof = {}

    # Iterate over the keys of life_data
    for j in life_data.keys():
        i = str(j)
        # Check if Value at key 'i' holds information of only one player
        if len(life_data[j][0]) == 1:
            # Set value at key 'i' to 0 for variance
            variance[i] = list([ 0 , [ life_data[j][1] ] ])
            # Set mean equal to the value of dictionary mean at key 'i'
            mean[i] = list(life_data[j][0][0])
            # Set qof as 1 if the player lived for more than 85 units of time else set qof to 0
            qof[i] = list(int(1) if life_data[j][0][0] >= 85 else int(0))
            # Move over to the next iteration
            continue
        # Set the value of qof at key 'i' to the count of players living for more than 30 units of time
        qof[i] = list([int(sum(np.array(life_data[j][0])) > 85) , life_data[j][1]])
        # Calculate the variance of life for the values in life_data at key 'i'
        variance[i] = [statistics.stdev(life_data[j][0]), life_data[j][1]]
        # Calculate the mean of the life for the values in life_data at key 'i'
        mean[i] = [statistics.mean(life_data[j][0]), life_data[j][1]]
    # Return the mean, variance and qof
    mean = json.dumps(mean)
    variance = json.dumps(variance)
    qof = json.dumps(qof)
    return mean, variance, qof


# Uncomment to check if the functions are working properly
print(get_life_stats("C:\\Users\\PD-PC\\Desktop\\Projects\\pygeneses\\Players_Data"))
print("#"*70)
print(gen_fam_graph("C:\\Users\\PD-PC\\Desktop\\Projects\\pygeneses\\Players_Data"))
