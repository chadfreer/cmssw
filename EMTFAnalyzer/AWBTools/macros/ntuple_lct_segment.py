#! /usr/bin/env python

import sys
import math
from ROOT import *

filename = '../NTupleMaker/EMTF_NTuple_ZMu_274198_debug.root'
file = TFile.Open(filename)

tree = file.Get("ntuple/tree")

for iEvt in range(tree.GetEntries()):
    
    ## if iEvt > 100: break
    ## if iEvt % 1 is 0: print 'Event #', iEvt
    tree.GetEntry(iEvt)

    for iReco in range(tree.numRecoMuons):

        for iSeg in range(tree.recoNumCscSegs[iReco]):
            if iSeg > 15: continue

            if tree.recoCscSeg_isMatched[iReco*16 + iSeg] == 1 and tree.recoCscSeg_lctId[iReco*16 + iSeg] >= 0:
                lct_id = tree.recoCscSeg_lctId[iReco*16 + iSeg]
            else: continue

            # if ( abs( tree.recoCscSeg_glob_eta[iReco*16 + iSeg] - tree.lctEta.at(lct_id) ) > 0.2 ):
            #     print '******* Eta difference *******'
            #     print 'Segment (LCT) endcap = %d (%d)' % ( tree.recoCscSeg_endcap[iReco*16 + iSeg], tree.lctEndcap.at(lct_id) )
            #     print 'Segment (LCT) station = %d (%d)' % ( tree.recoCscSeg_station[iReco*16 + iSeg], tree.lctStation.at(lct_id) )
            #     print 'Segment (LCT) sector = %d (%d)' % ( tree.recoCscSeg_sector[iReco*16 + iSeg], tree.lctSector.at(lct_id) )
            #     print 'Segment (LCT) eta = %.2f (%.2f)' % ( tree.recoCscSeg_glob_eta[iReco*16 + iSeg], tree.lctEta.at(lct_id) )
            #     print 'Segment (LCT) globalPhi = %.2f (%.2f)' % ( tree.recoCscSeg_glob_phi[iReco*16 + iSeg], tree.lctGlobalPhi.at(lct_id) )
            #     print ''
            if ( math.asin( math.sin( tree.recoCscSeg_glob_phi[iReco*16 + iSeg] - tree.lctGlobalPhi.at(lct_id) ) ) > 0.1 ):
                print '******* Phi difference *******'
                print 'Segment (LCT) endcap = %d (%d)' % ( tree.recoCscSeg_endcap[iReco*16 + iSeg], tree.lctEndcap.at(lct_id) )
                print 'Segment (LCT) station = %d (%d)' % ( tree.recoCscSeg_station[iReco*16 + iSeg], tree.lctStation.at(lct_id) )
                print 'Segment (LCT) sector = %d (%d)' % ( tree.recoCscSeg_sector[iReco*16 + iSeg], tree.lctSector.at(lct_id) )
                print 'Segment (LCT) eta = %.2f (%.2f)' % ( tree.recoCscSeg_glob_eta[iReco*16 + iSeg], tree.lctEta.at(lct_id) )
                print 'Segment (LCT) globalPhi = %.2f (%.2f)' % ( tree.recoCscSeg_glob_phi[iReco*16 + iSeg], tree.lctGlobalPhi.at(lct_id) )
                print ''

                

