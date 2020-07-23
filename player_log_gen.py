import glob
import os
import sys

folder = sys.argv[1]
target = folder + '_english'

if not os.path.exists(target):
    os.mkdir(target)

files = glob.glob(os.path.join(folder, '*.txt'))

id_to_action = {'0': 'left', '1': 'right', '2': 'up', '3': 'down', '4': 'up and left', '5': 'up and right',
                '6': 'down and left', '7': 'down and right', '8': 'stay', '9': 'ingestion',
                '10': 'asexual asexual_reproduction', '11': 'sexual reproduction', '12': 'fight'}

for filename in files:

    f = open(filename, "r")
    if f.mode == 'r':
        contents = f.readlines()
    f.close()

    f_target = open(os.path.join(target, os.path.basename(filename)), 'w')

    for line in contents:
        entity = list()
        log = line[1:len(line)-3]
        entity = log.split(',')

        if (entity[0]=='10'):
            f_target.write(f"The player performed action {id_to_action[entity[0]]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}. The number of offspring produced is {entity[4]}.\n")

        if (entity[0]=='11'):
            f_target.write(f"The player performed action {id_to_action[entity[0]]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}. The number of offspring produced is {entity[4]} and the mate of player is {entity[-1]}.\n")

        if (entity[0]=='12'):
            f_target.write(f"The player performed action {id_to_action[entity[0]]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}. The player fought with {entity[4]}.\n")

        if 'Failed' in entity[0]:
            f_target.write(f"The player failed to perform the action {id_to_action[entity[0][8:-1]]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}.\n")

        else:
            f_target.write(f"The player performed action {id_to_action[entity[0]]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}\n")

    f_target.close()
