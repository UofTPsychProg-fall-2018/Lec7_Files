#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: katherineduncan
"""

#%% import packages
import numpy as np
import pandas as pd
import os, sys, random
import itertools as it


#%% counterbalancing experiment designs
"""
The itertools package is helpful when making counterbalanced designs
You can find the full documation herer https://docs.python.org/3/library/itertools.html
"""

# lets say you have 3 conditions and you want to fully counterbalance their 
# order across participant -- have all possible sequences
# you can use the permutations() function to generate this list

Conds = ['A','B','C']
CondSeq = list(it.permutations(Conds))
# note that you need to wrap the itertools commands in a list because they return
# iterator objects (like a container that you can unpack into a list)
# you can also wrap the list in a dataframe if you want a nicer format


# it's not to hard to do this by hand with 3 conditions, but what if you had 6?

# TRY IT YOURSELF



# this could be helpful, but you likely won't be running 720 subjects!

# let's try an incomplete but practical counterbalancing approach: Latin Square
# the goal is to get each codition in each row and column once

# A B C
# B C A
# C A B

# let's warm up by hard coding it for three conditions
lsq =[]

Conds = ['A','B','C']
lsq.append(Conds)

# now rotate Conds by 1
Conds = Conds[-1:] + Conds[:-1]
lsq.append(Conds)

# and rotate Conds by 1 again
Conds = Conds[-1:] + Conds[:-1]
lsq.append(Conds)


# now let's build a loop to make it more efficient and flexible

lsq = []
for c in np.arange(len(Conds)):
    lsq.append(Conds)
    Conds = Conds[-1:] + Conds[:-1]


# TRY IT YOURSELF
# turn this loop into a function that you can use with any list of condtions

def latinSq(...):

    return ...
    

#%% putting together a stroop task
"""
You can also use itertools to put together lists of trials
Let's try this out with a simple stroop task which has three blocks:
    congruent, incongruent and neutral
    We'll have 6 trials of each
"""  

colours = ['red','blue','green']

# itertools permuations function can give us every mismatched permuatation 
incongruent = list(it.permutations(colours, 2))

# now we can turn it into a formatted csv file by putting it into a dataframe
incongDF = pd.DataFrame(incongruent, columns = ['word','colour'])
# add correct response key as the first letter of the colour; 'r' for red
incongDF['corResp'] = incongDF['colour'].astype(str).str[0]
incongDF.to_csv('incong.csv', index=False)

#############################################################################
# now let's make 6 congruent trials
#############################################################################
congruent = colours*2

# now we can turn it into a formatted csv file by putting it into a dataframe
congDF = pd.DataFrame(congruent, columns=['word'])
congDF['colour'] = congruent # just copy the same colour list
# add correct response key as the first letter of the colour; 'r' for red
congDF['corResp'] = congDF['colour'].astype(str).str[0]
congDF.to_csv('cong.csv', index=False)

#############################################################################
# and finally the neutral
#############################################################################
neutral = ['cat', 'dog', 'mouse', 'house', 'desk', 'table']

# now we can turn it into a formatted csv file by putting it into a dataframe
neutralDF = pd.DataFrame(neutral, columns=['word'])
neutralDF['colour'] = congruent
# add correct response key as the first letter of the colour; 'r' for red
neutralDF['corResp'] = neutralDF['colour'].astype(str).str[0]
neutralDF.to_csv('neutral.csv', index=False)

#############################################################################
# lastly, let's make a list of block orders using our latinSq function
#############################################################################
conds = ['cong.csv','incong.csv','neutral.csv']
condOrders =latinSq(conds)

# save out each order in a different subject file
for s in np.arange(len(condOrders)):
    df = pd.DataFrame(condOrders[s], columns=['blockList'])
    df.to_csv(str(s+1) + 'PickBlocks.csv', index=False)
    

# we have all we need for the builder!  
