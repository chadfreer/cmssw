#! /usr/bin/env python

import sys
import math
from ROOT import *

filename = '../NTupleMaker/EMTF_NTuple_ZMu_274198_debug.root'
file = TFile.Open(filename)

tree = file.Get("ntuple/tree")

for iEvt in range(tree.GetEntries()):
    
    if iEvt > 10: break
    ## if iEvt % 1 is 0: print 'Event #', iEvt
    tree.GetEntry(iEvt)
    if ( tree.numRecoMuons == 0 and tree.numTrks == 0 ):
        continue

    lctIDs = []
    for iLCT in range(tree.numLCTs):
        lctIDs.append(iLCT)

    reco_lctIDs = []
    for iReco in range(tree.numRecoMuons):
        print 'RECO track pT = %.1f, eta = %.2f, phi = %.2f' % ( tree.recoPt[iReco], tree.recoEta[iReco], tree.recoPhi[iReco] )
        for iSeg in range(tree.recoNumCscSegs[iReco]):
            ## if iSeg > 15: continue
            if tree.recoCscSeg_isMatched[iReco*16 + iSeg] == 1 and tree.recoCscSeg_lctId[iReco*16 + iSeg] >= 0:
                recoID = tree.recoCscSeg_lctId[iReco*16 + iSeg]
                reco_lctIDs.append( recoID )
                print 'Station %d seg with eta = %.2f, phi = %.2f' % ( tree.recoCscSeg_station[iReco*16 + iSeg], tree.recoCscSeg_glob_eta[iReco*16 + iSeg], tree.recoCscSeg_glob_phi[iReco*16 + iSeg] )
                print 'Station %d hit with eta = %.2f, phi = %.2f' % ( tree.lctStation.at(recoID), tree.lctEta.at(recoID), tree.lctGlobalPhi.at(recoID) )
        print ''
                

    trk_lctIDs = []
    for iTrk in range(tree.numTrks):
        for iLCT in range(tree.numTrkLCTs[iTrk]):
            has_match = False
            for lctId in lctIDs:
                if ( (tree.trkLct_endcap[iTrk*4 + iLCT] == 1) == (tree.lctEndcap.at(lctId) == 1) and
                     tree.trkLct_station[iTrk*4 + iLCT] == tree.lctStation.at(lctId) and
                     tree.trkLct_chamber[iTrk*4 + iLCT] == tree.lctChamber.at(lctId) and
                     tree.trkLct_strip[iTrk*4 + iLCT] == tree.lctStrip.at(lctId) and
                     tree.trkLct_wire[iTrk*4 + iLCT] == tree.lctWire.at(lctId) and
                     not has_match ):
                    has_match = True
                    trk_lctIDs.append(lctId)

    matched = []
    unmatched = []
    extra = []
    for recoID in reco_lctIDs:
        if recoID in trk_lctIDs:
            matched.append(recoID)
        else:
            unmatched.append(recoID)

    for trkID in trk_lctIDs:
        if not trkID in reco_lctIDs:
            extra.append(trkID)

    print 'In event with %d RECO tracks and %d EMTF tracks' % ( tree.numRecoMuons, tree.numTrks )
    print '%d LCTs, %d in RECO tracks, %d in EMTF tracks' % ( len(lctIDs), len(reco_lctIDs), len(trk_lctIDs) )
    print '%d matched, %d unmatched, %d extra' % ( len(matched), len(unmatched), len(extra) )
    print ''


    






                

