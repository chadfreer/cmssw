#! /usr/bin/env python

import sys
import math
import numpy
from ROOT import *

## in_filename = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Emulator/files/EMTF_NTuple_ZMu_274198_10k_B.root'
in_filename = '../NTupleMaker/EMTF_NTuple_ZMu_274198_10k.root'
in_file = TFile.Open(in_filename)
tree = in_file.Get("ntuple/tree")

out_file = TFile('plots/segment_RECO_matching.root', 'recreate')


eta_bins = [100, -2.5, 2.5]
phi_bins = [128, -3.2, 3.2]
pt_bins = [100, 0, 100]
station_bins = [6, -0.5, 5.5]

dEta_bins = [1000, -5, 5]
dPhi_bins = [700,-3.5,3.5]

h_eta_mu = TH1F('h_eta_mu', 'Muon eta', eta_bins[0], eta_bins[1], eta_bins[2]) 
h_phi_mu = TH1F('h_phi_mu', 'Muon phi', phi_bins[0], phi_bins[1], phi_bins[2]) 
h_pt_mu = TH1F('h_pt_mu', 'Muon pt', pt_bins[0], pt_bins[1], pt_bins[2]) 
h_station = TH1F('h_station', 'Segment station', station_bins[0], station_bins[1], station_bins[2])

h_eta_mu_hi_dPhi = TH1F('h_eta_mu_hi_dPhi', 'Muon eta, high dPhi', eta_bins[0], eta_bins[1], eta_bins[2]) 
h_phi_mu_hi_dPhi = TH1F('h_phi_mu_hi_dPhi', 'Muon phi, high dPhi', phi_bins[0], phi_bins[1], phi_bins[2]) 
h_pt_mu_hi_dPhi = TH1F('h_pt_mu_hi_dPhi', 'Muon pt, high dPhi', pt_bins[0], pt_bins[1], pt_bins[2]) 
h_station_hi_dPhi = TH1F('h_station_hi_dPhi', 'Segment station, high dPhi', station_bins[0], station_bins[1], station_bins[2])

h_dEta_mu = TH1F('h_dEta_mu', 'dEta(segment, muon)', dEta_bins[0], dEta_bins[1], dEta_bins[2])
h_dPhi_mu = TH1F('h_dPhi_mu', 'dPhi(segment, muon)', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2])
h_dEta_mu_hi_dPhi = TH1F('h_dEta_mu_hi_dPhi', 'dEta(segment, muon), high dPhi', dEta_bins[0], dEta_bins[1], dEta_bins[2])

h_phi_seg_vs_mu = TH2F('h_phi_seg_vs_mu', 'segment vs. muon phi', phi_bins[0], phi_bins[1], phi_bins[2], phi_bins[0], phi_bins[1], phi_bins[2])

h_dEta_LCT = TH1F('h_dEta_LCT', 'dEta(segment, LCT)', dEta_bins[0], dEta_bins[1], dEta_bins[2])
h_dPhi_LCT = TH1F('h_dPhi_LCT', 'dPhi(segment, LCT)', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2])

for iEvt in range(tree.GetEntries()):
    
    ## if iEvt > 300: break
    if iEvt % 100 is 0: print 'Event #', iEvt
    tree.GetEntry(iEvt)
    if ( tree.numRecoMuons == 0 and tree.numTrks == 0 ):
        continue

    # lctIDs = []
    # for iLCT in range(tree.numLCTs):
    #     lctIDs.append(iLCT)

    reco_lctIDs = []
    for iReco in range(tree.numRecoMuons):

        reco_endcap = -999
        isHalo = False
        hasHiDPhi = False
        for iSeg in range(tree.recoNumCscSegs[iReco]):
            if iSeg > 15 or tree.recoCscSeg_isMatched[iReco*16 + iSeg] != 1 or tree.recoCscSeg_lctId[iReco*16 + iSeg] == -999:
                continue
            recoID = tree.recoCscSeg_lctId[iReco*16 + iSeg]
            if iSeg > 0 and (tree.recoCscSeg_endcap[iReco*16 + iSeg] != reco_endcap or tree.lctEndcap.at(recoID) != reco_endcap ):
                isHalo = True
            reco_endcap = tree.recoCscSeg_endcap[iReco*16 + iSeg]
            if math.acos( math.cos( tree.recoCscSeg_glob_phi[iReco*16 + iSeg] - tree.recoPhi[iReco] ) ) > 1.5:
                hasHiDPhi = True

        if isHalo:
            continue

        # if hasHiDPhi:
        #     print ''
        #     print 'In event %d, RECO track pT = %.1f, eta = %.2f, phi = %.2f' % ( iEvt, tree.recoPt[iReco], tree.recoEta[iReco], tree.recoPhi[iReco] )
        #     for jReco in range(tree.numRecoMuons):
        #         if jReco != iReco:
        #             print 'Event has other RECO track pT = %.1f, eta = %.2f, phi = %.2f' % ( tree.recoPt[jReco], tree.recoEta[jReco], tree.recoPhi[jReco] )

        for iSeg in range(tree.recoNumCscSegs[iReco]):
            if iSeg > 15 or tree.recoCscSeg_isMatched[iReco*16 + iSeg] != 1 or tree.recoCscSeg_lctId[iReco*16 + iSeg] == -999:
                continue

            recoID = tree.recoCscSeg_lctId[iReco*16 + iSeg]
            reco_lctIDs.append( recoID )

            # if hasHiDPhi:
            #     print 'Station %d seg with eta = %.2f, phi = %.2f' % ( tree.recoCscSeg_station[iReco*16 + iSeg], tree.recoCscSeg_glob_eta[iReco*16 + iSeg], tree.recoCscSeg_glob_phi[iReco*16 + iSeg] )
            #     print 'Station %d hit with eta = %.2f, phi = %.2f' % ( tree.lctStation.at(recoID), tree.lctEta.at(recoID), tree.lctGlobalPhi.at(recoID) )
                
            dEta_mu = tree.recoCscSeg_glob_eta[iReco*16 + iSeg] - tree.recoEta[iReco]
            dPhi_mu = numpy.sign( math.sin( tree.recoCscSeg_glob_phi[iReco*16 + iSeg] - tree.recoPhi[iReco] ) ) * math.acos( math.cos( tree.recoCscSeg_glob_phi[iReco*16 + iSeg] - tree.recoPhi[iReco] ) )
            dEta_LCT = tree.recoCscSeg_glob_eta[iReco*16 + iSeg] - tree.lctEta.at(recoID)
            dPhi_LCT = numpy.sign( math.sin( tree.recoCscSeg_glob_phi[iReco*16 + iSeg] - tree.lctGlobalPhi.at(recoID) ) ) * math.acos( math.cos( tree.recoCscSeg_glob_phi[iReco*16 + iSeg] - tree.lctGlobalPhi.at(recoID) ) )
            
            h_dEta_mu.Fill( dEta_mu )
            h_dPhi_mu.Fill( dPhi_mu )
            h_phi_seg_vs_mu.Fill( tree.recoCscSeg_glob_phi[iReco*16 + iSeg], tree.recoPhi[iReco] )
            h_dEta_LCT.Fill( dEta_LCT )
            h_dPhi_LCT.Fill( dPhi_LCT )
            
            h_eta_mu.Fill( tree.recoEta[iReco] )
            h_phi_mu.Fill( tree.recoPhi[iReco] )
            h_pt_mu.Fill( min(tree.recoPt[iReco], pt_bins[2] - 0.01) )
            h_station.Fill( tree.recoCscSeg_station[iReco*16 + iSeg] )
            
            if abs(dPhi_mu) > 1.5:
                h_eta_mu_hi_dPhi.Fill( tree.recoEta[iReco] )
                h_phi_mu_hi_dPhi.Fill( tree.recoPhi[iReco] )
                h_pt_mu_hi_dPhi.Fill( min(tree.recoPt[iReco], pt_bins[2] - 0.01) )
                h_dEta_mu_hi_dPhi.Fill( dEta_mu )
                h_station_hi_dPhi.Fill( tree.recoCscSeg_station[iReco*16 + iSeg] )
                

    # trk_lctIDs = []
    # for iTrk in range(tree.numTrks):
    #     for iLCT in range(tree.numTrkLCTs[iTrk]):
    #         has_match = False
    #         for lctId in lctIDs:
    #             if ( (tree.trkLct_endcap[iTrk*4 + iLCT] == 1) == (tree.lctEndcap.at(lctId) == 1) and
    #                  tree.trkLct_station[iTrk*4 + iLCT] == tree.lctStation.at(lctId) and
    #                  tree.trkLct_chamber[iTrk*4 + iLCT] == tree.lctChamber.at(lctId) and
    #                  tree.trkLct_strip[iTrk*4 + iLCT] == tree.lctStrip.at(lctId) and
    #                  tree.trkLct_wire[iTrk*4 + iLCT] == tree.lctWire.at(lctId) and
    #                  not has_match ):
    #                 has_match = True
    #                 trk_lctIDs.append(lctId)

    # matched = []
    # unmatched = []
    # extra = []
    # for recoID in reco_lctIDs:
    #     if recoID in trk_lctIDs:
    #         matched.append(recoID)
    #     else:
    #         unmatched.append(recoID)

    # for trkID in trk_lctIDs:
    #     if not trkID in reco_lctIDs:
    #         extra.append(trkID)

    # print 'In event with %d RECO tracks and %d EMTF tracks' % ( tree.numRecoMuons, tree.numTrks )
    # print '%d LCTs, %d in RECO tracks, %d in EMTF tracks' % ( len(lctIDs), len(reco_lctIDs), len(trk_lctIDs) )
    # print '%d matched, %d unmatched, %d extra' % ( len(matched), len(unmatched), len(extra) )
    # print ''

## End loop: for iEvt in range(tree.GetEntries()):
    
out_file.cd()

h_eta_mu.Write()
h_phi_mu.Write()
h_pt_mu.Write()
h_station.Write()

h_eta_mu_hi_dPhi.Write()
h_phi_mu_hi_dPhi.Write()
h_pt_mu_hi_dPhi.Write()
h_station_hi_dPhi.Write()

h_dEta_mu.Write()
h_dPhi_mu.Write()
h_phi_seg_vs_mu.Write()
h_dEta_mu_hi_dPhi.Write()

h_dEta_LCT.Write()
h_dPhi_LCT.Write()

out_file.Close()
in_file.Close()
