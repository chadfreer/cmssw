########################################################
## eff_modules.py   A script to find CSCTF efficiency by segment-Lct matching
##
## By David Curry
##
########################################################


import sys
import os
import re
import numpy as np
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT
from array import *



def EMTF_Bx(iEvt, tree, iTrk, printLevel):

    '''
    Takes in an EMTF track and assigns it a Bx based on second in time LCT Bx from the event record.
    '''

    Bx = 0
    bx_list = []
    
    # Loop over EMTF LCTs
    for iLct in range(0,tree.numTrkLCTs[iTrk]):
    
        if iLct > 3: continue
        if iTrk > 3: continue
        
        # Loop over Event LCTS, Match by wire/strip and take its' BX.
        for iEvtLCT in range(0,tree.numLCTs):
            
            if iEvtLCT > tree.numLCTs: continue

            if tree.trkLctWire[iTrk*4 + iLct]  != tree.lctWire[iEvtLCT]:  continue
            if tree.trkLctStrip[iTrk*4 + iLct] != tree.lctStrip[iEvtLCT]: continue

            # take the event LCT BX. Store in a list.
            bx_list.append(tree.lctBx[iEvtLCT])
            
    
             
    # Take the second highest BX form the list and assign t=it to EMTF track Bx.

    if len(bx_list) > 1:
        bx_list.remove(max(bx_list))
        Bx = bx_list[0] - 6

    elif len(bx_list) == 1:
        Bx = bx_list[0] - 6


    return Bx

def deltaPhi(phi1, phi2):
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result


def deltaRLegTrackMuon(iEvt, tree, iReco, printLevel):
    
    '''
    Takes in a Reco Muon and legacy track collection and matches with dR.  
    Returns a list [bool, [trkId]]
    '''

    if printLevel > 0: print '-----> Checking for dR Muon-Track Match.'
    
    list = [False, 999]
    
    dr = 999
    min_dr = 0.3

    # Loop over tracks
    for iTrk in range(tree.numTrks_unpack):
        
        trkPhi = tree.leg_trkPhi[iTrk]
        trkEta = tree.leg_trkEta[iTrk]
        
        mounPhi = tree.gmrPhi[iReco]
        mounEta = tree.gmrEta[iReco]
    
        dphi = deltaPhi(trkPhi, mounPhi)
        deta = trkEta - mounEta
                
        dr = np.sqrt(dphi*dphi + deta*deta) 
        
        if dr < min_dr:
            min_dr = dr
            list[0] = True
            list[1] = iTrk

    return list


# ==========================================

def dphi_plots(tree, iTrk):
    
    '''
    Takes in a track to make dphi plots from its' LCTs
    '''

    phi1, phi2, phi3, phi4 = -99, -99, -99, -99
    eta1, eta2, eta3, eta4 = -99, -99, -99, -99
    
    if tree.trkMode[iTrk] == 15:
        
        for iLct in range(tree.numTrkLCTs[iTrk]):
            
            if tree.trkLctStation[iTrk*4 +iLct] == 1: 
                phi1 = tree.trkLctGblPhi[iTrk*4 + iLct]
                eta1 = tree.trkLctGblEta[iTrk*4 + iLct]

            if tree.trkLctStation[iTrk*4 +iLct] == 2: 
                phi2 = tree.trkLctGblPhi[iTrk*4 + iLct]
                eta2 = tree.trkLctGblEta[iTrk*4 + iLct]

            if tree.trkLctStation[iTrk*4 +iLct] == 3: 
                phi3 = tree.trkLctGblPhi[iTrk*4 + iLct]
                eta3 = tree.trkLctGblEta[iTrk*4 + iLct]
                
            if tree.trkLctStation[iTrk*4 +iLct] == 4: 
                phi4 = tree.trkLctGblPhi[iTrk*4 + iLct]
                eta4 = tree.trkLctGblEta[iTrk*4 + iLct]
                
    
        dphi12 = abs(phi1-phi2)
        dphi13 = abs(phi1-phi3)
        dphi14 = abs(phi1-phi4)
        dphi23 = abs(phi2-phi3)
        dphi24 = abs(phi2-phi4)
        dphi34 = abs(phi3-phi4)

        deta12 = abs(eta1-eta2)
        deta13 = abs(eta1-eta3)
        deta14 = abs(eta1-eta4)
        deta23 = abs(eta2-eta3)
        deta24 = abs(eta2-eta4)
        deta34 = abs(eta3-eta4)
        

        hdphi12_trk15.Fill(dphi12)
        hdphi13_trk15.Fill(dphi13)
        hdphi14_trk15.Fill(dphi14)
        hdphi23_trk15.Fill(dphi23)
        hdphi24_trk15.Fill(dphi24)
        hdphi34_trk15.Fill(dphi34)
        
        h2dphi_trk15.Fill(1, dphi12)
        h2dphi_trk15.Fill(2, dphi13)
        h2dphi_trk15.Fill(3, dphi14)
        h2dphi_trk15.Fill(4, dphi23)
        h2dphi_trk15.Fill(5, dphi24)
        h2dphi_trk15.Fill(6, dphi34)
        
        h2deta_trk15.Fill(1, deta12)
        h2deta_trk15.Fill(2, deta13)
        h2deta_trk15.Fill(3, deta14)
        h2deta_trk15.Fill(4, deta23)
        h2deta_trk15.Fill(5, deta24)
        h2deta_trk15.Fill(6, deta34)

        
    # end mode 15


    phi1, phi2, phi3, phi4 = -99, -99, -99, -99
    eta1, eta2, eta3, eta4 = -99, -99, -99, -99
    
    # Now look at bending between track LCTs and event LCTs
    if tree.trkMode[iTrk] == 10: # Stations 1-3
        
        for iLct in range(tree.numTrkLCTs[iTrk]):

            if tree.trkLctStation[iTrk*4 +iLct] == 1: 
                phi1 = tree.trkLctGblPhi[iTrk*4 + iLct]
                eta1 = tree.trkLctGblEta[iTrk*4 + iLct]
                
            if tree.trkLctStation[iTrk*4 +iLct] == 3: 
                phi3 = tree.trkLctGblPhi[iTrk*4 + iLct]
                eta3 = tree.trkLctGblEta[iTrk*4 + iLct]
                
            # Loop over event LCTs
            for iEvtLct in range(tree.numLCTs):
                
                if tree.lctStation[iEvtLct] == 2: 
                    phi2 = tree.lctGlobalPhi[iEvtLct]
                    eta2 = tree.lctGlobalEta[iEvtLct]
                    
                if tree.lctStation[iEvtLct] == 4: 
                    phi4 = tree.lctGlobalPhi[iEvtLct]
                    eta4 = tree.lctGlobalEta[iEvtLct]




        if phi1 != -99 and phi2 != -99:            
            dphi12 = abs(phi1-phi2)
            h2dphi_trk10.Fill(1, dphi12)
        if phi1 != -99 and phi3 != -99:
            dphi13 = abs(phi1-phi3)
            h2dphi_trk10.Fill(2, dphi13)
        if phi1 != -99 and phi4 != -99:
            dphi14 = abs(phi1-phi4)
            h2dphi_trk10.Fill(3, dphi14)
        if phi2 != -99 and phi3 != -99:
            dphi23 = abs(phi2-phi3)
            h2dphi_trk10.Fill(4, dphi23)
        if phi2 != -99 and phi4 != -99:
            dphi24 = abs(phi2-phi4)
            h2dphi_trk10.Fill(5, dphi24)
        if phi3 != -99 and phi4 != -99:
            dphi34 = abs(phi3-phi4)
            h2dphi_trk10.Fill(6, dphi34)

            
        h2dphi_trk10_noEvtLCTs.Fill(2,dphi13)

        if eta1 != -99 and eta2 != -99:
            deta12 = abs(eta1-eta2)
            h2deta_trk10.Fill(1, deta12)
        if eta1 != -99 and eta3 != -99:
            deta13 = abs(eta1-eta3)
            h2deta_trk10.Fill(2, deta13)
        if eta1 != -99 and eta4 != -99:
            deta14 = abs(eta1-eta4)
            h2deta_trk10.Fill(3, deta14)
        if eta2 != -99 and eta3 != -99:
            deta23 = abs(eta2-eta3)
            h2deta_trk10.Fill(4, deta23)
        if eta2 != -99 and eta4 != -99:
            deta24 = abs(eta2-eta4)
            h2deta_trk10.Fill(5, deta24)
        if eta3 != -99 and eta4 != -99:
            deta34 = abs(eta3-eta4)
            h2deta_trk10.Fill(6, deta34)
        

#============================================================




def dphi_plots_leg(tree, iLegTrk):

    '''
    Takes in a track to make dphi plots from its' LCTs
    '''

    phi1, phi2, phi3, phi4 = -99, -99, -99, -99
    eta1, eta2, eta3, eta4 = -99, -99, -99, -99

    if iLegTrk != -999:
        if tree.leg_trkMode[iLegTrk] == 15:
        
            for iLct in range(tree.numLegTrkLCTs[iLegTrk]):
            
                if tree.leg_trkLctStation[iLegTrk*4 +iLct] == 1: 
                    phi1 = tree.leg_trkLctGblPhi[iLegTrk*4 + iLct]
                    eta1 = tree.leg_trkLctGblEta[iLegTrk*4 + iLct]
                    
                if tree.leg_trkLctStation[iLegTrk*4 +iLct] == 2: 
                    phi2 = tree.leg_trkLctGblPhi[iLegTrk*4 + iLct]
                    eta2 = tree.leg_trkLctGblEta[iLegTrk*4 + iLct]
                        
                if tree.leg_trkLctStation[iLegTrk*4 +iLct] == 3: 
                    phi3 = tree.leg_trkLctGblPhi[iLegTrk*4 + iLct]
                    eta3 = tree.leg_trkLctGblEta[iLegTrk*4 + iLct]
                            
                if tree.leg_trkLctStation[iLegTrk*4 +iLct] == 4: 
                    phi4 = tree.leg_trkLctGblPhi[iLegTrk*4 + iLct]
                    eta4 = tree.leg_trkLctGblEta[iLegTrk*4 + iLct]
                
    
            dphi12 = abs(phi1-phi2)
            dphi13 = abs(phi1-phi3)
            dphi14 = abs(phi1-phi4)
            dphi23 = abs(phi2-phi3)
            dphi24 = abs(phi2-phi4)
            dphi34 = abs(phi3-phi4)
            
            deta12 = abs(eta1-eta2)
            deta13 = abs(eta1-eta3)
            deta14 = abs(eta1-eta4)
            deta23 = abs(eta2-eta3)
            deta24 = abs(eta2-eta4)
            deta34 = abs(eta3-eta4)
            
            h2deta_trk15_leg.Fill(1, deta12)
            h2deta_trk15_leg.Fill(2, deta13)
            h2deta_trk15_leg.Fill(3, deta14)
            h2deta_trk15_leg.Fill(4, deta23)
            h2deta_trk15_leg.Fill(5, deta24)
            h2deta_trk15_leg.Fill(6, deta34)
            
            h2dphi_trk15_leg.Fill(1, dphi12)
            h2dphi_trk15_leg.Fill(2, dphi13)
            h2dphi_trk15_leg.Fill(3, dphi14)
            h2dphi_trk15_leg.Fill(4, dphi23)
            h2dphi_trk15_leg.Fill(5, dphi24)
            h2dphi_trk15_leg.Fill(6, dphi34)


# ======================================================================    


def get_Tchain(directory, num_files):

    '''
    Takes a directory of root files and gives a tchain of the desired length(numfiles)
    '''

    os.system('rm tchain')
    
    # define the tchain object
    tchain_reco  = TChain('recoMuons') 
    tchain_csctf = TChain('csctfTTree')

    # print the contents of directory to a txt file
    temp_str = "cmsLs "+directory+ " | grep root | awk '{print ""$5""}' >> tchain"
    os.system(temp_str)
    
    with open('tchain') as file:

        for i, line in enumerate(file):

            #if i is num_files: break

            print '-----> Tchain adding root://eoscms//eos/cms/', line
            
            #first add the recoMuon tree to the chain
            tchain_reco.Add('root://eoscms//eos/cms/'+line)
            
            # now add the csctf tree
            tchain_csctf.Add('root://eoscms//eos/cms/'+line)
            
            
    # end file loop
    
    chain_list = [tchain_reco, tchain_csctf]
            
    return chain_list


def whichQ(iTrk, csc):

    '''
    Checks track quality
    '''

    # first get the track mode
    trkMode = track_mode(iTrk, csc)

    trkQ = -999

    # quality 3
    if trkMode == 2 and abs(csc.leg_trkEta[iTrk]) > 1.2: trkQ = 3
    if trkMode == 3 or trkMode == 4 or trkMode == 5 or trkMode == 12: trkQ = 3
    

    # quality 2
    if trkMode == 6 and abs(csc.leg_trkEta[iTrk]) > 1.2: trkQ = 2
    if trkMode == 7 and abs(csc.leg_trkEta[iTrk]) < 2.1: trkQ = 2 
    if trkMode == 13 and abs(csc.trkEta[iTrk]) > 2.1: trkQ = 2
    
    if trkQ == -999:  trkQ = 1
    
    return trkQ


def track_mode(iTrk, csc):
    
    '''
    Returns track mode
    '''

    final_mode = -999
    
    if csc.numLegTrkLCTs[iTrk] < 3:
        # first look at two hit tracks
        # Possible modes are station combinations:
        # 1-2  Mode 6 : sum 3
        # 1-3  Mode 7 : sum 4
        # 1-4  Mode 13: sum 5
        # 2-3  Mode 8 : sum 5
        # 2-4  Mode 9 : sum 6
        # 3-4  Mode 10: sum 7
    
        temp_mode = 0; track_mode = 0
        isStation_1 = False; isStation_2 = False

        # loop over tracks hits to find mode
        for iCsc in range(csc.numLegTrkLCTs[iTrk]):

            temp_mode += csc.leg_trkLctStation[iTrk*4 + iCsc]
        
            if csc.leg_trkLctStation[iTrk*4 + iCsc] == 1: isStation_1 = True
            if csc.leg_trkLctStation[iTrk*4 + iCsc] == 2: isStation_2 = True

        # Which mode is track
        if temp_mode == 3: final_mode = 6
        if temp_mode == 4: final_mode = 7
        if temp_mode == 6: final_mode = 9
        if temp_mode == 7: final_mode = 10

        # In the event of mode 5 we need to find which configuration
        if track_mode == 5 and isStation_1: final_mode = 13
        elif final_mode == -999: final_mode = 8
    
        # for overlap track
        if final_mode == -999: final_mode = 15

    # end 2 hit tracks

    # 3 or more hit tracks
    # Possible modes are station combinations:
    # 1-2-3-4 Mode 1 sum 10
    # 1-2-3   Mode 2 sum 6
    # 1-2-4   Mode 2 sum 7
    # 1-3-4   Mode 3 sum 8
    # 2-3-4   Mode 4 sum 9

    if csc.numLegTrkLCTs[iTrk] > 2:
        
        temp_mode = 0
        isStation1 = False
        isStation2 = False
        isStation3 = False
        isStation4 = False

        for iCsc in range(csc.numLegTrkLCTs[iTrk]):
            temp_mode += csc.leg_trkLctStation[iTrk*4 + iCsc]

        # Which mode is track
        if temp_mode == 10: final_mode = 2 
        if temp_mode == 6:  final_mode = 2
        if temp_mode == 7:  final_mode = 3
        if temp_mode == 8:  final_mode = 4
        if temp_mode == 9:  final_mode = 5
        
        if final_mode == -999: final_mode = 12
        
    return final_mode
        


# ============================================================================

def is_two_segs(iEvt, iReco, tree, printLevel):

    ''' Returns a list: [Bool, [Lct Ids] ]
    Bool is whether the muon has two Segs matched to event Lcts.
    Lct Id is which Lct the Seg is matched to. Minimum two Ids
    '''

    if printLevel > 0:
        print '----> Checking muon for two matched segments.'

    # create list to be returned.  [bool, list[int]]
    list = [False, []]

    # Fill with endcap values to check for halo muon
    halo_list = []
    
    for iSeg in range(tree.muonNsegs[iReco]):
        
        if printLevel > 2: print '\nLooping over Segment # ', iSeg
        
        # Check if seg is matched to Lct
        if iSeg > 15: continue

        if printLevel > 2:
            print ' segStation :', tree.muon_cscsegs_station[iReco*16 + iSeg]
            print ' segEndcap  :', tree.muon_cscsegs_endcap[iReco*16 + iSeg]


        if tree.muon_cscsegs_ismatched[iReco*16 + iSeg]:
            
            id = tree.muon_cscsegs_lctId[iReco*16 + iSeg]
            
            if id == -999: continue
            
            if printLevel > 2:
                print '\nSegment is matched to Lct', id, \
                    '\n LctStation = ', tree.lctStation.at(id), \
                    '\n LctEndcap  = ', tree.lctEndcap.at(id)
            
            halo_list.append(tree.lctEndcap.at(id))
                
            if id not in list[1]: list[1].append(id)
            
    # end seg loop
            

    if len(list[1]) > 1:
        
        list[0] = True 

        if printLevel > 0: print'\n-----> Muon has two segments matched to LCTs...'

        # check for halo muon.
        if halo_list.count(halo_list[0]) < len(halo_list):  
            #list[0] = False
            if printLevel > 1: '\n-----> Halo Muon!!!!'

    return list
    

# end is two segs matched


def is_track_match(iEvt, csc, id_list, printLevel):

    '''
    Returns a list:  [Bool, track Id].
    Bool is whether a track match was found to Seg Lcts, and track id is which track was macthed
    '''

    if printLevel > 0: print '-----> Checking for Track Lct - Seg Lct Match.'

    # the final list returned with best matched track
    return_list = [False, 999]

    # keep list of all matched tracks.  Choose the best mode. [iTrk, modeTrk]
    track_list = [ [], [] ]

    isTrk_match = False
    
    # Does a track have the same Lcts that segs matched to?
    # Loop over tracks
    for iTrk in range(0, csc.numTrks):

        if iTrk > 3: break

        is_lct_match = False
        
        for iLct in range(0, csc.numTrkLCTs[iTrk]):
            
            if is_lct_match: break
            
            if printLevel > 1:
                print '\nLooping over Track #', iTrk, ', Lct #', iLct, \
                    '\n trLctStation = ', csc.trkLctStation[iTrk*4 + iLct], \
                    '\n trLctEndcap  = ', csc.trkLctEndcap[iTrk*4 + iLct], \
                    '\n trLctSector  = ', csc.trkLctSector[iTrk*4 + iLct], \
                    '\n trLctRing    = ', csc.trkLctRing[iTrk*4 + iLct], \
                    '\n trLctChamber = ', csc.trkLctChamber[iTrk*4 + iLct], \
                    '\n trLctWire    = ', csc.trkLctWire[iTrk*4 + iLct], \
                    '\n trLctStrip   = ', csc.trkLctStrip[iTrk*4 + iLct], \
                    #'\n trLctglobalEta  = ', csc.trLctglobalEta[iTrk*4 + iLct], \
                    #'\n trLctglobalPhi  = ', csc.trLctglobalPhi[iTrk*4 + iLct]
                
            # compare track Lct to seg matched Lcts.  Loop over id_list
            for x in id_list:
                
                if is_lct_match: break

                if printLevel > 1:
                    print '\n\tLooping over LCTs in id_list:', x, \
                      '\n LctStation = ', csc.lctStation.at(x), \
                      '\n LctEndcap  = ', csc.lctEndcap.at(x), \
                      '\n LctSector  = ', csc.lctSector.at(x), \
                      '\n LctRing    = ', csc.lctRing.at(x), \
                      '\n LctChamber = ', csc.lctChamber.at(x), \
                      '\n LctWire    = ', csc.lctWire.at(x), \
                      '\n LctStrip   = ', csc.lctStrip.at(x), \
                      #'\n LctglobalEta  = ', csc.lctglobalEta.at(x), \
                      #'\n LctglobalPhi  = ', csc.lctglobalPhi.at(x)
                
                if csc.trkLctEndcap[iTrk*4 + iLct] == 2: trkLctEndcap = -1
                else: trkLctEndcap = 1 
                    
                if csc.trkLctStation[iTrk*4 + iLct]   != csc.lctStation.at(x):   continue
                if trkLctEndcap != csc.lctEndcap.at(x):    continue
                #if csc.trkLctEndcap[iTrk*4 + iLct]    != csc.lctEndcap.at(x):    continue
                #if csc.trkLctSector[iTrk*4 + iLct]    != csc.lctSector.at(x):    continue
                if csc.trkLctRing[iTrk*4 + iLct]      != csc.lctRing.at(x):      continue
                if csc.trkLctChamber[iTrk*4 + iLct]   != csc.lctChamber.at(x):   continue
                if csc.trkLctWire[iTrk*4 + iLct]      != csc.lctWire.at(x):      continue
                if csc.trkLctStrip[iTrk*4 + iLct]     != csc.lctStrip.at(x):     continue
                #if csc.trLctglobalEta[iTrk*4 + iLct] != csc.lctglobalEta.at(x):   continue
                #if csc.trLctglobalPhi[iTrk*4 + iLct] != csc.lctglobalPhi.at(x):   continue
                
                is_lct_match = True

                isTrk_match  = True
                    
                if printLevel > 1: print'\n-----> Seg Lct and Track Lct are matched.'
                
                track_list[0].append(iTrk)
                track_list[1].append(csc.trkMode[iTrk])
                


    if isTrk_match:

        # Choose best mode as matched track
        bestIndex = track_list[1].index(max(track_list[1]))
        bestTrk   = track_list[0][bestIndex]
        
        #print 'track list[0]: ', track_list[0]
        #print 'track list[1]: ', track_list[1]
        #print 'best Index: ', bestIndex, 'best Trk: ', bestTrk
    
        return_list[0], return_list[1] = True, bestTrk
                        
    
    if printLevel > 0 and not isTrk_match: print '-----> Could not match muon to a track.'
                    
    return return_list
                
# end is track match


def is_track_match_leg(iEvt, csc, id_list, printLevel):

    '''
    Returns a list:  [Bool, track Id].
    Bool is whether a track match was found to Seg Lcts, and track id is which track was macthed
    Works for legacy CSCTF tracks
    '''

    if printLevel > 0: print '-----> Checking for Track Lct - Seg Lct Match.'

    return_list = [False, 999]

     # keep list of all matched tracks.  Choose the best mode. [iTrk, modeTrk]
    track_list = [ [], [] ]

    isTrk_match = False
    
    # Does a track have the same Lcts that segs matched to?
    # Loop over tracks
    for iTrk in range(0, csc.numLegTrks):
        
        if iTrk > 3: break

        is_lct_match = False
        
        for iLct in range(0, csc.numLegTrkLCTs[iTrk]):
            
            if is_lct_match: break
            
            if printLevel > 1:
                print '\nLooping over Track #', iTrk, ', Lct #', iLct, \
                    '\n trLctStation = ', csc.leg_trkLctStation[iTrk*4 + iLct], \
                    '\n trLctEndcap  = ', csc.leg_trkLctEndcap[iTrk*4 + iLct], \
                    '\n trLctSector  = ', csc.leg_trkLctSector[iTrk*4 + iLct], \
                    '\n trLctRing    = ', csc.leg_trkLctRing[iTrk*4 + iLct], \
                    '\n trLctChamber = ', csc.leg_trkLctChamber[iTrk*4 + iLct], \
                    '\n trLctWire    = ', csc.leg_trkLctWire[iTrk*4 + iLct], \
                    '\n trLctStrip   = ', csc.leg_trkLctStrip[iTrk*4 + iLct], \
                    #'\n trLctglobalEta  = ', csc.trLctglobalEta[iTrk*4 + iLct], \
                    #'\n trLctglobalPhi  = ', csc.trLctglobalPhi[iTrk*4 + iLct]
                
            # compare track Lct to seg matched Lcts.  Loop over id_list
            for x in id_list:
                
                if is_lct_match: break

                if printLevel > 1:
                    print '\n\tLooping over LCTs in id_list:', x, \
                      '\n LctStation = ', csc.lctStation.at(x), \
                      '\n LctEndcap  = ', csc.lctEndcap.at(x), \
                      '\n LctSector  = ', csc.lctSector.at(x), \
                      '\n LctRing    = ', csc.lctRing.at(x), \
                      '\n LctChamber = ', csc.lctChamber.at(x), \
                      '\n LctWire    = ', csc.lctWire.at(x), \
                      '\n LctStrip   = ', csc.lctStrip.at(x), \
                      #'\n LctglobalEta  = ', csc.lctglobalEta.at(x), \
                      #'\n LctglobalPhi  = ', csc.lctglobalPhi.at(x)
                

                if csc.leg_trkLctStation[iTrk*4 + iLct]   != csc.lctStation.at(x):   continue
                if csc.leg_trkLctEndcap[iTrk*4 + iLct]    != csc.lctEndcap.at(x):    continue
                #if csc.trkLctSector[iTrk*4 + iLct]    != csc.lctSector.at(x):    continue
                if csc.leg_trkLctRing[iTrk*4 + iLct]      != csc.lctRing.at(x):      continue
                if csc.leg_trkLctChamber[iTrk*4 + iLct]   != csc.lctChamber.at(x):   continue
                if csc.leg_trkLctWire[iTrk*4 + iLct]      != csc.lctWire.at(x):      continue
                if csc.leg_trkLctStrip[iTrk*4 + iLct]     != csc.lctStrip.at(x):     continue
                #if csc.trLctglobalEta[iTrk*4 + iLct] != csc.lctglobalEta.at(x):   continue
                #if csc.trLctglobalPhi[iTrk*4 + iLct] != csc.lctglobalPhi.at(x):   continue
                
                is_lct_match = True
                    
                isTrk_match  = True

                if printLevel > 1: print'\n-----> Seg Lct and Track Lct are matched.'

                track_list[0].append(iTrk)
                track_list[1].append(csc.leg_trkMode[iTrk])
                

    
    if isTrk_match:

        # Choose best mode as matched track
        bestIndex = track_list[1].index(max(track_list[1]))
        bestTrk   = track_list[0][bestIndex]

        return_list[0], return_list[1] = True, bestTrk
                        
    if printLevel > 0 and not isTrk_match: print '-----> Could not match muon to a track.'
                    
    return return_list
                
# end is track match





def deltaR(iEvt, iReco, tree, printLevel):

    '''
    Takes in muon and track and returns a deltaR value
    '''

    list = [False, 999]

    dr = 999
    min_dr = 0.3

    # Loop over tracks
    for iTrk in range(tree.numTrks_unpack):

        #trkBx = tree.trkBx[iTrk] - 6
        #if trkBx != 0: continue
        
        trkPhi = tree.trkPhi_unpack[iTrk]
        trkEta = tree.trkEta_unpack[iTrk]
        
        mounPhi = tree.gmrPhi[iReco]
        mounEta = tree.gmrEta[iReco]

        

        dphi = deltaPhi(trkPhi, mounPhi)
        deta = trkEta - mounEta

        dr = np.sqrt(dphi*dphi + deta*deta)

        if dr < min_dr:
            min_dr = dr
            list[0] = True
            list[1] = iTrk

    return list



    

# ==== Binning for efficiency plots ======

num_phiBins = 24
num_etaBins = 24

scale_phi_temp = [0]*num_phiBins
scale_eta_temp = [0]*num_etaBins

scale_pt_temp = [0, 3, 5, 8, 10, 12, 16, 20, 25, 30, 35, 50, 75, 100]

# Initialize phi
phiMin = -np.pi

scale_phi_temp[0] = phiMin

for iphi in range(1,len(scale_phi_temp)):
    scale_phi_temp[iphi] = scale_phi_temp[iphi-1] + (2*np.pi/(num_phiBins-1))
    

etaMin = 1.2
scale_eta_temp[0] = etaMin

for ieta in range(len(scale_eta_temp)):
    scale_eta_temp[ieta] = etaMin + (1.5*ieta/(num_etaBins-1))

#print scale_eta_temp
#print scale_phi_temp

scale_pt  = array('f', scale_pt_temp)    
scale_phi = array('f', scale_phi_temp)
scale_eta = array('f', scale_eta_temp)


# ========================================

# some useful arrays
# Array of delta phi depending on eta.  v = [ eta , delta phi ]
eta_dphi_ME1toME2 = [127, 127, 127, 127, 57, 45, 41,  42,  42,  31,
                     127, 127,  29,  28, 29, 30, 35,  37,  34,  34,
                     36,  37,  37,  37, 39, 40, 52, 126, 104, 104,
                     87,  90,  93,  87, 85, 82, 80,  79,  82,  79,
                     79,  77,  75,  75, 67, 67, 69,  68,  67,  65,
                     65,  64,  60,  58, 57, 57, 57,  55,  53,  51,
                     49,  46,  36, 127]

eta_dphi_ME1toME3 = [127, 127, 127, 127, 127, 127, 40, 80, 80, 64,
                     127, 127,  62,  41,  41,  45, 47, 48, 47, 46,
                     47,  50,  52,  51,  53,  54, 55, 73, 82, 91,
                     91,  94, 100,  99,  95,  94, 95, 91, 96, 96,
                     94,  94,  88,  88,  80,  80, 84, 84, 79, 78,
                     80,  78,  75,  72,  70,  71, 69, 71, 71, 66,
                     61,  60,  43, 127]

dt_csc_dphi = [127, 127, 127, 127,  90,  78,  76,  76,  66,  65,
               59,  90,  50,  49,  37, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
               127, 127, 127, 127]
