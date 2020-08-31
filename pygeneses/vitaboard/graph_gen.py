# Import required libraries
import os
import glob
import numpy as np
import re
from collections import OrderedDict
import json
from sklearn.manifold import TSNE

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

def add_life_exp(life, tob, life_data, id, address):
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
    id        (str)
        : String containing the name of the player
    address   (str)
        : Address of the folder containing the log Files

    Returns
    =======
    life_data (dict)
        : Dictionary Containing the values {tob : life} for players
    """

    # Check if tob already exists in life_data or not
    if tob not in life_data.keys():
        life_data[tob] = [[life],[os.path.join(address, str(tob) + "-" + str(id))]]
    else:
        life_data[tob][0].append(life)
        life_data[tob][1].append(os.path.join(address, str(tob) + "-" + str(id)))

    return life_data

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
        : Dictionary containting the mean of lifetimes of players born at a particular time {time_of_birth: mean}

    variance (dict)
        : Dictionary containting the variance of lifetimes of players born at a particular time {time_of_birth: variance}

    qof      (dic)
        : Dictionary containing the Quality of life index of players born at a particular time {time_of_birth: count_qof}
    """

    # Get all npy files from address
    f_names = glob.glob(os.path.join(address, '*.npy'))

    if len(f_names) == 0:
        return -1, -1, -1

    life_data = {}

    for f_name in f_names:
        # Load log file
        log_values = np.load(f_name, allow_pickle=True)

        # Extract tob (time of birth) and id of the player
        tob, id = os.path.basename(f_name).split("-")
        tob = int(tob)

        if(len(log_values) == 2):
            continue

        # Extract the tod (time of death) of the player
        tod = log_values[-1][1]

        # Calculate the lifetime of the player
        lifetime = tod - tob

        # Update life_data
        life_data = add_life_exp(lifetime, tob, life_data, id, address)

    # Initialise dictionaries to store various statistics
    variance = []
    mean = []
    qof = []

    for j in life_data.keys():
        life, id = life_data[j]

        # Check if jth index holds information of only one player
        if len(life) == 1:
            variance.append({"tob": j, "value": 0 , "agents": [id]})
            mean.append({"tob": j, "value": life, "agents": [id]})
            qof.append({"tob": j, "value": int(1) if life >= 60 else int(0), "agents": [id] if life >= 60 else []})
            continue

        qof.append({"x": j, "y": int(sum(np.array(life) >= 60))/len(life) , "agents": [id[idx] for idx in range(len(life)) if life[idx] >= 60]})
        variance.append({"x": j, "y": np.array(life).var(), "agents": id})
        mean.append({"x": j, "y": np.array(life).mean(), "agents": id})

    # Return the mean, variance and qof
    mean = json.dumps(mean)
    variance = json.dumps(variance)
    qof = json.dumps(qof)
    return mean, variance, qof

def tsne(address):
    """
    Return t-SNE coordinates of agent embeddings

    Params
    ======
    address (str)
        : Address of the folder containing the log files

    Returns
    =======
    coord  (dict)
        : Dictionary containting the t-SNE embedding of players. {time_of_birth: mean}
    """

    embeddings = glob.glob(os.path.join(address, "Embeddings/*.npy"))

    if len(embeddings) == 0:
        return -1

    embedding_values = []
    embedding_ids = []
    for i, embedding in enumerate(embeddings):
        data = np.load(embedding, allow_pickle=True)
        if data[0].shape != ():
            embedding_values.append(data[0])
            embedding_ids.append(i)

    embedding_values = np.array(embedding_values)

    X_embedded = TSNE(n_components=2, random_state=42).fit_transform(embedding_values)

    coord = []
    for i, embedding in enumerate(X_embedded):
        path = embeddings[embedding_ids[i]]
        path = os.path.normpath(path)
        path = "/".join(path.split(os.sep)[:-2] + [path.split(os.sep)[-1]])
        coord.append({"x": int(embedding[0]), "y": int(embedding[1]), "agent": path})

    coord = json.dumps(coord)
    return coord

def get_parents(path, filename, ancestor_list, level=0):
    """
    Generates list of parents recursively until the initial population

    Params
    ======
    path          (str)
        : Path of the folder containing the log files
    filename      (str)
        : Log file name containing log of agent whose parents are to be found
    ancestor_list (list)
        : A list of dictionaries containing information about parents and their level of depth
    level         (int)
        : Depth of ancestor tree denoting the generation (generation 1 denotes immediate parents)

    """

    # Read the log file
    agent_data = np.load(os.path.join(path, filename), allow_pickle=True)

    # If the agent is from initial population and died without performing any action then break from recursion
    if(len(agent_data) < 2):
        return
    # If the agent is from initial population then he/she will not have any other parent
    elif(len(agent_data[1]) != 2):
        return
    # Otherwise recursively find parent at each generation
    else:
        parents = agent_data[1]

        # If there are two parents (sexual reproduction)
        if type(parents[0]) == list:
            level += 1

            # Extract data of both parents from child log
            id_1, tob_1 = parents[0]
            id_2, tob_2 = parents[1]

            # Append to ancestor_list the details of first parent and find parent(s) of parent recursively
            ancestor_list.append({"parent_of": filename,
                                  "filename": os.path.join(path, str(tob_1) + "-" + str(id_1) + ".npy"),
                                  "level": int(level)})
            get_parents(path, str(tob_1) + "-" + str(id_1) + ".npy", ancestor_list, level)

            # Append to ancestor_list the details of second parent and find parent(s) of parent recursively
            ancestor_list.append({"parent_of": filename,
                                  "filename": os.path.join(path, str(tob_2) + "-" + str(id_2) + ".npy"),
                                  "level": int(level)})
            get_parents(path, str(tob_2) + "-" + str(id_2) + ".npy", ancestor_list, level)
        # If there is only single parent (asexual reproduction)
        else:
            level += 1

            # Extract data of parent from child log
            id_1, tob_1 = parents

            # Append to ancestor_list the details of parent and find parent(s) of parent recursively
            ancestor_list.append({"parent_of": filename,
                                  "filename": os.path.join(path, str(tob_1) + "-" + str(id_1) + ".npy"),
                                  "level": int(level)})
            get_parents(path, str(tob_1) + "-" + str(id_1) + ".npy", ancestor_list, level)

def get_children(path, filename, successor_list, level=0):
    """
    Generates list of parents recursively until the initial population

    Params
    ======
    path          (str)
        : Path of the folder containing the log files
    filename      (str)
        : Log file name containing log of agent whose parents are to be found
    ancestor_list (list)
        : A list of dictionaries containing information about parents and their level of depth
    level         (int)
        : Depth of ancestor tree denoting the generation (generation 1 denotes immediate parents)

    """

    full_path = os.path.join(path, filename)

    # If the agent was alive when training stopped then break from recursion
    if not os.path.exists(full_path):
        return

    # Load agent logs
    agent_data = np.load(full_path, allow_pickle=True)

    # If agent died without performing any action then there won't be any children
    if(len(agent_data) <= 2):
        return
    # Otherwise search for children
    else:
        # Boolean flag to check if the current agent had any children or not
        has_child = False

        level += 1

        # Logs for action starts from index 2 for agents not in initial population otherwise they start
        # at index 1
        logdata = agent_data[2:] if not filename.startswith('0-') else agent_data[1:]

        for data in logdata:
            # Extract type of action and reward for current action
            action = data[0]
            reward = data[2]

            # If action was sexual or asexual reproduction and it was successful then append children to tree
            if(action in [10, 11] and reward > 0):
                # The agent has atleast one child
                has_child = True

                # Extract action time, number of offsprings and their ids
                time = data[1]
                num_offsprings = data[4]
                offspring_ids = data[5]

                for offspring_id in offspring_ids:
                    # Append the child details into successor_list and find its children recursively
                    successor_list.append({"child_of": filename,
                                           "filename": os.path.join(path, str(time) + "-" + str(offspring_id) + ".npy"),
                                           "level": int(level)})
                    get_children(path, str(time) + "-" + str(offspring_id) + ".npy", successor_list, level)

        # If the current agent does not have any child then break out of recursion
        if not has_child:
            return

# Uncomment to check if the functions are working properly
if __name__ == "__main__":
    mean, variance, qof = get_life_stats("/Users/frankhart/Downloads/Players_Data")
    print(qof)
    # print(get_life_stats("C:\\Users\\PD-PC\\Desktop\\Projects\\pygeneses\\Players_Data"))
    # print("#"*70)
    # print(gen_fam_graph("C:\\Users\\PD-PC\\Desktop\\Projects\\pygeneses\\Players_Data"))
