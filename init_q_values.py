import json
from itertools import chain

# Script to create Q-Value JSON file, initilazing with zeros

qval = {}

for mx in range(3,15):
    for my in range(-9,10):
        for by in range(-9,10):
            qval[str(mx)+'_'+str(my)+'_'+str(by)] = [0,0]


fd = open('qvalues.json', 'w')
json.dump(qval, fd)
fd.close()