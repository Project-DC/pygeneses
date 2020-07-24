import glob
import os
import sys
import numpy as np

folder = sys.argv[1]
target = folder + '_english'

if not os.path.exists(target):
    os.mkdir(target)

files = glob.glob(os.path.join(folder, '*.npy'))

id_to_action = {'0': 'left', '1': 'right', '2': 'up', '3': 'down', '4': 'up and left', '5': 'up and right',
                '6': 'down and left', '7': 'down and right', '8': 'stay', '9': 'ingestion',
                '10': 'asexual reproduction', '11': 'sexual reproduction', '12': 'fight'}

for filename in files:

    contents = np.load(filename, allow_pickle=True)
    
    f_target = open(os.path.join(target, os.path.basename(filename)), 'w')

    for line in contents:

        if (line[0]=='10'):
            f_target.write(f"The player performed action {id_to_action[str(line[0])]} at time {line[1]} and earned the reward of {line[2]} and its energy is {line[3]}. The number of offspring produced is {line[4]}.\n")

        if (line[0]=='11'):
            f_target.write(f"The player performed action {id_to_action[str(line[0])]} at time {line[1]} and earned the reward of {line[2]} and its energy is {line[3]}. The number of offspring produced is {line[4]} and the mate of player is {line[-1]}.\n")

        if (line[0]=='12'):
            f_target.write(f"The player performed action {id_to_action[str(line[0])]} at time {line[1]} and earned the reward of {line[2]} and its energy is {line[3]}. The player fought with {line[4]}.\n")

        if (line[0]=='Failed'):
            f_target.write(f"The player failed to perform the action {id_to_action[line[0][8:-1]]} at time {line[1]} and earned the reward of {line[2]} and its energy is {line[3]}.\n")

        else:
            f_target.write(f"The player performed action {id_to_action[str(line[0])]} at time {line[1]} and earned the reward of {line[2]} and its energy is {line[3]}\n")

    f_target.close()

