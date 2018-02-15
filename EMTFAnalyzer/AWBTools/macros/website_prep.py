# ===================================================
# Python script to perform BDT regression loop
# Tests performance as a function of several parmeters
#
#  !!!! Needs to be ran from python directory
#
# 2/15/2015 David Curry
# ===================================================

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *
import multiprocessing


# Which main directory:
# https://dcurry.web.cern.ch/dcurry/xxxx
main_dir = 'L1T_5_24'


# Move old datacards to a repository
try:
     os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir)
     temp_string1 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir
     temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir

     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator')
     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker')

     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/rate')
     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/eff')

     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/rate')
     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/eff')
     
     #os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/comparison/')
     
     #temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/rate/'
     #temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/rate/'
     
     #temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/eff/'
     #temp_string6 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/eff/'

     #temp_string7 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/eff/'
     #temp_string8 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/eff/'

     #temp_string9 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/rate/'
     #temp_string10 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/rate/'

     #temp_string11 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/'
     #temp_string12 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/'

     #temp_string13 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/'
     #temp_string14 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/'

     #temp_string15 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/comparison/'
     #temp_string16 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/comparison/'

     # Now make the individual dirs
     #t3 = 'mkdir '

     os.system(temp_string1)
     os.system(temp_string2)
     #os.system(temp_string3)
     #os.system(temp_string4)
     
     #os.system(temp_string5)
     #os.system(temp_string6)
     #os.system(temp_string7)
     #os.system(temp_string8)
     #os.system(temp_string9)
     #os.system(temp_string10)
     #os.system(temp_string11)
     #os.system(temp_string12)
     #os.system(temp_string13)
     #os.system(temp_string14)
     #os.system(temp_string15)
     #os.system(temp_string16)



except:
     print main_dir+' already exists...'
     
     '''
     temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/rate/'
     temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/rate/'

     temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/eff/'
     temp_string6 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/eff/'

     temp_string7 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/'
     temp_string8 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/'

     temp_string9 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/'
     temp_string10 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/'

     temp_string9 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/comparison/'
     temp_string10 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/comparison/'
     
     os.system(temp_string3)
     os.system(temp_string4)
     os.system(temp_string5)
     os.system(temp_string6)
     os.system(temp_string7)
     os.system(temp_string8)
     os.system(temp_string9)
     os.system(temp_string10)
     '''


#t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/rate/'
#t2 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/eff/'

#temp_string_r1 = 'cp /afs/cern.ch/work/d/dcurry/private/emtf8v2/CMSSW_8_0_2/src/TrackAnalyzer/CSCplusRPCTrackAnalyzer/macros/plots/emulator/rate/* /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/rate/'

#temp_string_r2 = 'cp /afs/cern.ch/work/d/dcurry/private/emtf8v2/CMSSW_8_0_2/src/TrackAnalyzer/CSCplusRPCTrackAnalyzer/macros/plots/unpacker/rate/* /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/rate/'

#temp_string_e1 = 'cp /afs/cern.ch/work/d/dcurry/private/emtf8v2/CMSSW_8_0_2/src/TrackAnalyzer/CSCplusRPCTrackAnalyzer/macros/plots/emulator/eff/* /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/emulator/eff/'

#temp_string_e2 = 'cp /afs/cern.ch/work/d/dcurry/private/emtf8v2/CMSSW_8_0_2/src/TrackAnalyzer/CSCplusRPCTrackAnalyzer/macros/plots/unpacker/eff/* /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/unpacker/eff/'


temp_string_c = 'cp /afs/cern.ch/work/d/dcurry/private/emtf8v2/CMSSW_8_0_2/src/TrackAnalyzer/CSCplusRPCTrackAnalyzer/macros/L1T/plots/L1T/* /afs/cern.ch/user/d/dcurry/www/'+main_dir

#os.system(temp_string_r1)
#os.system(temp_string_e1)
#os.system(temp_string_r2)
#os.system(temp_string_e2)
os.system(temp_string_c)

