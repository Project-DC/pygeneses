import sys
files = sys.argv[1:]

for filename in files:
    
    f = open(filename, "r")
    if f.mode == 'r':
        contents = f.readlines()

    for line in contents:
        entity = list()
        log = line[1:len(line)-3]
        entity = log.split(',')

        if (entity[0]=='10'):
            print(f"The player performed action {entity[0]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}. The number of offspring produced is {entity[4]}.")

        if (entity[0]=='11'):
            print(f"The player performed action {entity[0]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}. The number of offspring produced is {entity[4]} and the mate of player is {entity[-1]}")

        if (entity[0]=='12'):
            print(f"The player performed action {entity[0]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}. The player fought with {entity[4]}")

        if 'Failed' in entity[0]:
            print(f"The player failed to perform the action {entity[0][8:-1]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}.")
        
        else:
            print(f"The player performed action {entity[0]} at time {entity[1]} and earned the reward of {entity[2]} and its energy is {entity[3]}")
        
