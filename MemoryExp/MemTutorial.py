#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: katherineduncan
"""

#%% import packages
import numpy as np
import pandas as pd
import os, sys, random, shutil

#%% Randomizing and renaming stimuli 
"""
Many stimulus banks systematically order stimuli using descriptive names.
If you want to randomly assign stimului to conditions, randomizing their names
is a good place to start!
"""

# set file directories
oldDir = os.path.join('Stim', 'objects')
newDir = os.path.join('Stim', 'objectsRand')

# make new directory
if  os.path.isdir(newDir) == False:
    os.mkdir(newDir)

# read in files
oldNames = os.listdir(oldDir)
# remove hidden files using list comprehension 
oldNames = [f for f in oldNames if not f.startswith('.')]

# get file type extension
ext = '.' + oldNames[0].split('.')[1]

# randomize file list (for good measure...)
random.shuffle(oldNames)

# loop and copy
# make a dataframe to keep track of renaming system
log = pd.DataFrame(columns = ["oldName","newName"])
for f in np.arange(len(oldNames)):
    newName= os.path.join(newDir, str(f+1) + ext)
    
    shutil.copyfile(os.path.join(oldDir, oldNames[f]),newName)
    log.loc[f,'oldName'] = oldNames[f]
    log.loc[f,'newName'] = os.path.split(newName)[-1]
    

log.to_csv(os.path.join('Stim','ObjRenameLog.csv'), index = False)
    
    
#%% Try it yourself
"""
Copy and adjust this code to rename and randomize the scene stimuli
"""



#%% making a stimulus list
"""
Now that we have have random file names to work with, let's define our trials
in a csv file that can be read into the builder or coder

This will be a silly experiment: 
    We will test whether people of have better memory for stimuli associated 
    with a positive vs. a negative noise (manipulated within subject). 
    
    We will also see if this noise variable interacts with stimulus category 
    (object vs. scene; manipulated across subjects)

Let's begin by making one trial list for objects and one for scenes
"""

numTrials = 20
toneDir = os.path.join('Stim', 'sounds')

# make a list with an even number of trials per cond
toneCond = np.array(['chime.wav','error.wav']*int(numTrials/2))

# and randomize the order
random.shuffle(toneCond)

# or perhaps you want to pseudorandomize with some restrictions, like no more 
# than two consecuative trials with a particular tone in a row
 
goodList = 0
while goodList == 0:
    random.shuffle(toneCond)
    
    # test where shifted versions of the sequences are equivilent to eachother
    if any((toneCond[0:-2]==toneCond[1:-1]) & 
         (toneCond[1:numTrials-1]==toneCond[2:len(toneCond)+1])) == False:
             goodList = 1
             break

# Let's say participants need to press a button when they hear a chime
corResp = pd.Series(np.repeat('None', numTrials))   
corResp[toneCond == 'chime.wav'] = 'Space'  

# add path to each tone filename using list comprehension
toneCond = [os.path.join(toneDir, s ) for s in toneCond]
 
         
# now make image lists
imageNum = np.arange(1,numTrials+1)
objPaths = [os.path.join('Stim', 'objectsRand', str(s) + '.jpg') for s in imageNum]
scenePaths = [os.path.join('Stim', 'scenesRand', str(s) + '.jpg') for s in imageNum]
# alternatively you could just read in the image names from your stimulus directory
 
# put together in dataframe, where each row is a trial     
objTrialList = pd.DataFrame(columns=['image', 'sound','corResp'])
objTrialList['image'] = objPaths
objTrialList['sound'] = toneCond
objTrialList['corResp'] = corResp

# scene trial list is almost the same as the object so you can just make a copy
sceneTrialList = objTrialList.copy()
sceneTrialList['image'] = scenePaths


if  os.path.isdir('subFiles') == False:
    os.mkdir('subFiles')

objTrialList.to_csv(os.path.join('subFiles', 'objectTrialList.csv'),index=False)
sceneTrialList.to_csv(os.path.join('subFiles', 'sceneTrialList.csv'),index=False)


#%% making a stimulus list
"""
But what if the stimuli in one tone condition happen to be more memorable than
the other?  We should make multiple version so that each stimulus is equally 
likely to be in each tone condition

An easy way to do this is to make a pair of orders and reverse the tone 
condition in the second
"""    

objTrialList.to_csv(os.path.join('subFiles', '1TrialList.csv'),index=False)
sceneTrialList.to_csv(os.path.join('subFiles', '2TrialList.csv'),index=False)
  

chimeInd = objTrialList['sound'].str.contains('chime')
errorInd = objTrialList['sound'].str.contains('error')

objTrialList.loc[errorInd,'sound'] = os.path.join('Stim','sounds','chime.wav')
objTrialList.loc[chimeInd,'sound'] = os.path.join('Stim','sounds','error.wav')

## TRY IT YOURSELF
# find and replace the corResp information and then save out the dataframe

