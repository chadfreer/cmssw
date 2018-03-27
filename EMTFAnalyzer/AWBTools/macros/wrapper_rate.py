########################################################
## Wraps the different pt and eta cuts
##
## By David Curry
##
########################################################


import sys
import re
import os
import fileinput
import subprocess
from ROOT import *
import numpy as np
from array import *
from collections import Counter
#from eff_modules import *



# Set the TF pt cut and the probe muon pt cut
pt_list = [0, 5, 12, 16]

probe_pt_list = [3, 8, 17, 20]



# Loop over pt list
for i, pt in enumerate(pt_list):

    # Modify rate.py for new pt cut
    new_cut = 'pt_cut = '+str(pt)+'\n'
    
    print 'new pt cut:', new_cut

    for line in fileinput.input("eff_L1T.py", inplace=True):

        if 'pt_cut =' in line:

            print line.replace(line, new_cut),

        else: print line,
    # end file modification
        
        
    # now probe pt cut
    new_probe_cut = 'probe_ptCut = '+str(probe_pt_list[i])+'\n'
    
    print 'new probe cut:', new_probe_cut

    for line in fileinput.input("eff_L1T.py", inplace=True):

        if 'probe_ptCut =' in line:

            print line.replace(line, new_probe_cut),

        else: print line,
    # end file modification
        
    # change the histogram file name
    new_name = 'newfile = TFile("plots/L1T_analysis_singleMu'+str(pt)+'_stage2.root","recreate")\n'
    
    for line in fileinput.input("eff_L1T.py", inplace=True):

        if 'newfile =' in line:

            print line.replace(line, new_name),

        else: print line,
    # end file modification

    # Run rate.py
    os.system('python eff_L1T.py')
    

