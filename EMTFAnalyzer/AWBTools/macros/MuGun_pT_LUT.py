#! /usr/bin/env python

import sys
import math
from ROOT import *
import numpy as np
from array import *
from collections import OrderedDict
# from eff_modules import *

def main():

###################
## Initialize files
###################
    
    file_name = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_RPC_300k.root'

    in_file = TFile.Open(file_name)
    
    tree = in_file.Get('ntuple/tree')
    
    out_file = TFile('plots/MuGun_pT_LUT_CSC_10k.root', 'recreate')
    
#################
## Selection cuts
#################

    eta_cuts = {}
    eta_cuts['all']       = [1.20, 2.40, '1.2 < |#eta| < 2.4']
    # eta_cuts['1p2_1p85']  = [1.20, 1.85, '1.2 < |#eta| < 1.85']
    # eta_cuts['1p85_2p4']  = [1.85, 2.40, '1.85 < |#eta| < 2.4']
    eta_cuts['1p2_1p55']  = [1.20, 1.55, '1.2 < |#eta| < 1.55']
    eta_cuts['1p55_1p85'] = [1.55, 1.85, '1.55 < |#eta| < 1.85']
    eta_cuts['1p85_2p1']  = [1.85, 2.10, '1.85 < |#eta| < 2.1']
    eta_cuts['2p1_2p4']   = [2.10, 2.40, '2.1 < |#eta| < 2.4']
    
    pt_cuts = OrderedDict()
    pt_cuts['all']      = [  0, 1000, '1 < p_{T} < 1000 GeV']
    pt_cuts['1_4']     = [  1,    4, '1 < p_{T} < 4 GeV']
    pt_cuts['4_8']     = [  4,    8, '4 < p_{T} < 8 GeV']
    pt_cuts['8_15']    = [  8,   15, '8 < p_{T} < 15 GeV']
    pt_cuts['15_30']   = [ 15,   30, '15 < p_{T} < 30 GeV']
    pt_cuts['30_60']   = [ 30,   60, '30 < p_{T} < 60 GeV']
    # pt_cuts['60_120']  = [ 60,  120, '60 < p_{T} < 120 GeV']
    # pt_cuts['120_250'] = [120,  240, '120 < p_{T} < 250 GeV']
    # pt_cuts['250_up']  = [250, 1000, '250 < p_{T} < 1000 GeV']

    # pt_cuts['3_3p5']   = [  3,  3.5, '3 < p_{T} < 3.5 GeV']
    # pt_cuts['7_8']     = [  7,    8, '7 < p_{T} < 8 GeV']
    # pt_cuts['15_16']   = [ 15,   16, '15 < p_{T} < 16 GeV']
    # pt_cuts['30_31']   = [ 30,   31, '30 < p_{T} < 31 GeV']

    
    st_cuts = {}
    for iSt in range(1, 5):
        for jSt in range(iSt, 5):
            st_cuts['%d_%d' % (iSt, jSt)] = [iSt, jSt, '%d-%d' % (iSt, jSt)]

    det_cuts = {}
    # for iDet in ['CSC', 'RPC']:
    #     for jDet in ['CSC', 'RPC']:
    for iDet in ['CSC']:
        for jDet in ['CSC']:
            det_cuts['%s_%s' % (iDet, jDet)] = [iDet, jDet, '(%s-%s)' % (iDet, jDet)]
    
#############
## Histograms
#############

    # dPh_thin   = [121, -60.5*(1./60.), 60.5*(1./60.)]
    # dPh_bins   = [121, -60.5*(4./60.), 60.5*(4./60.)]
    dPh_thin   = [121, -60.5*(2./60.), 60.5*(2./60.)]
    dPh_bins   = [121, -60.5*(8./60.), 60.5*(8./60.)]
    dPh_wide   = [121, -60.5*(16./60.), 60.5*(16./60.)]

    dTh_bins = [33, -16.5*(36.5/128.), 16.5*(36.5/128.)] 
    dTh_wide = [33, -16.5*(36.5/32.), 16.5*(36.5/32.)] 

    sum4_dPh_thin = [121, -60.5*(1./60.), 60.5*(1./60.)]
    sum4_dPh_bins = [121, -60.5*(4./60.), 60.5*(4./60.)]
    sum4_dPh_wide = [121, -60.5*(16./60.), 60.5*(16./60.)]

    sum4A_dPh_thin = [63, -2.5*(1./60.), 60.5*(1./60.)]
    sum4A_dPh_bins = [63, -2.5*(4./60.), 60.5*(4./60.)]
    sum4A_dPh_wide = [63, -2.5*(16./60.), 60.5*(16./60.)]

    sum3_dPh_thin = [121, -60.5*(1./60.), 60.5*(1./60.)]
    sum3_dPh_bins = [121, -60.5*(4./60.), 60.5*(4./60.)]
    sum3_dPh_wide = [121, -60.5*(16./60.), 60.5*(16./60.)]

    sum3A_dPh_thin = [63, -2.5*(1./60.), 60.5*(1./60.)]
    sum3A_dPh_bins = [63, -2.5*(4./60.), 60.5*(4./60.)]
    sum3A_dPh_wide = [63, -2.5*(16./60.), 60.5*(16./60.)]

    frac_bins = [201, -1.005, 1.005]
    st_bins = [6, -0.5, 5.5]
    bend_bins = [11, -5.5, 5.5]

    dTheta_max = 16.5*(36.5/128.)


    h_dPhi_thin   = {}
    h_dPhi        = {}
    h_dPhi_wide   = {}
    h_dTheta      = {}
    h_dTheta_wide = {}
    h_bend        = {}

    h_sum4_dPhi_thin  = {}
    h_sum4_dPhi       = {}
    h_sum4_dPhi_wide  = {}
    h_sum4A_dPhi_thin = {}
    h_sum4A_dPhi      = {}
    h_sum4A_dPhi_wide = {}
    h_sum3_dPhi_thin  = {}
    h_sum3_dPhi       = {}
    h_sum3_dPhi_wide  = {}
    h_sum3A_dPhi_thin = {}
    h_sum3A_dPhi      = {}
    h_sum3A_dPhi_wide = {}
    h_sum4_dPhi_frac  = {}
    h_sum3_dPhi_frac  = {}
    h_outlier_st      = {}

    for iPt in pt_cuts.keys():
        pt_str = pt_cuts[iPt][2]
            
        for iEta in eta_cuts.keys():
            eta_str = eta_cuts[iEta][2]

            h_sum4_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4_dPhi_pt_%s_eta_%s_thin' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge, %s, %s' % (pt_str, eta_str),
                                                                  sum4_dPh_thin[0], sum4_dPh_thin[1], sum4_dPh_thin[2] )
            h_sum4_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4_dPhi_pt_%s_eta_%s' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge, %s, %s' % (pt_str, eta_str),
                                                                  sum4_dPh_bins[0], sum4_dPh_bins[1], sum4_dPh_bins[2] )
            h_sum4_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4_dPhi_pt_%s_eta_%s_wide' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge, %s, %s' % (pt_str, eta_str),
                                                                  sum4_dPh_wide[0], sum4_dPh_wide[1], sum4_dPh_wide[2] )
            
            h_sum4A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4A_dPhi_pt_%s_eta_%s_thin' % (iPt, iEta),
                                                                  '#Sigma(|d#phi|), %s, %s' % (pt_str, eta_str),
                                                                  sum4A_dPh_thin[0], sum4A_dPh_thin[1], sum4A_dPh_thin[2] )
            h_sum4A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4A_dPhi_pt_%s_eta_%s' % (iPt, iEta),
                                                                  '#Sigma(|d#phi|), %s, %s' % (pt_str, eta_str),
                                                                  sum4A_dPh_bins[0], sum4A_dPh_bins[1], sum4A_dPh_bins[2] )
            h_sum4A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4A_dPhi_pt_%s_eta_%s_wide' % (iPt, iEta),
                                                                  '#Sigma(|d#phi|), %s, %s' % (pt_str, eta_str),
                                                                  sum4A_dPh_wide[0], sum4A_dPh_wide[1], sum4A_dPh_wide[2] )

            h_sum3_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3_dPhi_pt_%s_eta_%s_thin' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  sum3_dPh_thin[0], sum3_dPh_thin[1], sum3_dPh_thin[2] )
            h_sum3_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3_dPhi_pt_%s_eta_%s' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  sum3_dPh_bins[0], sum3_dPh_bins[1], sum3_dPh_bins[2] )
            h_sum3_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3_dPhi_pt_%s_eta_%s_wide' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  sum3_dPh_wide[0], sum3_dPh_wide[1], sum3_dPh_wide[2] )
            
            h_sum3A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3A_dPhi_pt_%s_eta_%s_thin' % (iPt, iEta),
                                                                  '#Sigma(|d#phi|) x #mu charge (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  sum3A_dPh_thin[0], sum3A_dPh_thin[1], sum3A_dPh_thin[2] )
            h_sum3A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3A_dPhi_pt_%s_eta_%s' % (iPt, iEta),
                                                                  '#Sigma(|d#phi|) x #mu charge (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  sum3A_dPh_bins[0], sum3A_dPh_bins[1], sum3A_dPh_bins[2] )
            h_sum3A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3A_dPhi_pt_%s_eta_%s_wide' % (iPt, iEta),
                                                                  '#Sigma(|d#phi|) x #mu charge (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  sum3A_dPh_wide[0], sum3A_dPh_wide[1], sum3A_dPh_wide[2] )

            h_sum4_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum4_dPhi_frac_pt_%s_eta_%s' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge / #Sigma(|d#phi|), %s, %s' % (pt_str, eta_str),
                                                                  frac_bins[0], frac_bins[1], frac_bins[2] )
            h_sum3_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_sum3_dPhi_frac_pt_%s_eta_%s' % (iPt, iEta),
                                                                  '#Sigma(d#phi) x #mu charge / #Sigma(|d#phi|) (outlier removed), %s, %s' % (pt_str, eta_str),
                                                                  frac_bins[0], frac_bins[1], frac_bins[2] )
            h_outlier_st['pt_%s_eta_%s' % (iPt, iEta)] = TH1D( 'h_outlier_st_pt_%s_eta_%s' % (iPt, iEta),
                                                               'Station with largest #Sigma(|d#phi|), %s, %s' % (pt_str, eta_str),
                                                               st_bins[0], st_bins[1], st_bins[2] )

            for iSt in range(1, 5):
                h_sum4A_dPhi_thin['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)] = TH1D( 'h_sum4A_dPhi_pt_%s_eta_%s_outlier_st_%d_thin' % (iPt, iEta, iSt),
                                                                                   '#Sigma(|d#phi|), %s, %s, station %d outlier' % (pt_str, eta_str, iSt),
                                                                                   sum4A_dPh_thin[0], sum4A_dPh_thin[1], sum4A_dPh_thin[2] )
                h_sum4A_dPhi     ['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)] = TH1D( 'h_sum4A_dPhi_pt_%s_eta_%s_outlier_st_%d' % (iPt, iEta, iSt),
                                                                                   '#Sigma(|d#phi|), %s, %s, station %d outlier' % (pt_str, eta_str, iSt),
                                                                                   sum4A_dPh_bins[0], sum4A_dPh_bins[1], sum4A_dPh_bins[2] )
                h_sum4A_dPhi_wide['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)] = TH1D( 'h_sum4A_dPhi_pt_%s_eta_%s_outlier_st_%d_wide' % (iPt, iEta, iSt),
                                                                                   '#Sigma(|d#phi|), %s, %s, station %d outlier' % (pt_str, eta_str, iSt),
                                                                                   sum4A_dPh_wide[0], sum4A_dPh_wide[1], sum4A_dPh_wide[2] )
                h_bend['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)] = TH1D( 'h_bend_pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt),
                                                                        'LCT bend, %s, %s, station %d' % (iPt, iEta, iSt),
                                                                        bend_bins[0], bend_bins[1], bend_bins[2] )
                
            
            for iSt in st_cuts.keys():
                st_str = st_cuts[iSt][2]
            
                for iDet in det_cuts.keys():
                    det_str = det_cuts[iDet][2]
            
                    h_dPhi_thin['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)] = TH1D( 'h_dPhi_pt_%s_eta_%s_st_%s_%s_thin' % (iPt, iEta, iSt, iDet),
                                                                                          'd#phi %s %s x #mu charge, %s, %s' % (st_str, det_str, pt_str, eta_str),
                                                                                          dPh_thin[0], dPh_thin[1], dPh_thin[2] )
                    h_dPhi     ['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)] = TH1D( 'h_dPhi_pt_%s_eta_%s_st_%s_%s'      % (iPt, iEta, iSt, iDet),
                                                                                          'd#phi %s %s x #mu charge, %s, %s' % (st_str, det_str, pt_str, eta_str),
                                                                                          dPh_bins[0], dPh_bins[1], dPh_bins[2] )
                    h_dPhi_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)] = TH1D( 'h_dPhi_pt_%s_eta_%s_st_%s_%s_wide' % (iPt, iEta, iSt, iDet),
                                                                                          'd#phi %s %s x #mu charge, %s, %s' % (st_str, det_str, pt_str, eta_str),
                                                                                          dPh_wide[0], dPh_wide[1], dPh_wide[2] )
                    
                    h_dTheta     ['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)] = TH1D( 'h_dTheta_pt_%s_eta_%s_st_%s_%s'      % (iPt, iEta, iSt, iDet),
                                                                                            'd#theta %s %s, %s, %s' % (st_str, det_str, pt_str, eta_str),
                                                                                            dTh_bins[0], dTh_bins[1], dTh_bins[2] )
                    h_dTheta_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)] = TH1D( 'h_dTheta_pt_%s_eta_%s_st_%s_%s_wide' % (iPt, iEta, iSt, iDet),
                                                                                            'd#theta %s %s, %s, %s' % (st_str, det_str, pt_str, eta_str),
                                                                                            dTh_wide[0], dTh_wide[1], dTh_wide[2] )
                    
#############
## Event loop
#############
                
    for iEvt in range(tree.GetEntries()):
            
        if iEvt > 50000: break
        if iEvt % 1000 is 0: print 'Event #', iEvt

        tree.GetEntry(iEvt)

        muons = tree.GetBranch('muon')
        trks  = tree.GetBranch('track')
        hits  = tree.GetBranch('hit')
        
        nMuons = int(muons.GetLeaf('nMuons').GetValue())
        nTrks  = int(trks.GetLeaf('nTracks').GetValue())
        nHits  = int(hits.GetLeaf('nHits').GetValue())
        
        mu1_eta = muons.GetLeaf('eta').GetValue(0)
        if abs(mu1_eta) < 1.2 or abs(mu1_eta) > 2.4: continue

        for iMu in range(nMuons):
            mu_pt     = muons.GetLeaf('pt').GetValue(iMu)
            mu_eta    = muons.GetLeaf('eta').GetValue(iMu)
            mu_charge = muons.GetLeaf('charge').GetValue(iMu)

            ############################################################
            ## Build tracks manually out of hits, based on smallest dPhi
            ############################################################

            ## Get station and index of LCT(s) defining track location(s): station 2, if available, else 3 or 4
            key_st_idx = []
            considered_hits = []  ## All hits to consider at later stages (non-neighbor, correct endcap)
            for iHit in range(nHits):
                hit_isRPC = hits.GetLeaf('isRPC').GetValue(iHit)
                hit_eta   = hits.GetLeaf('eta').GetValue(iHit)
                hit_st    = int(hits.GetLeaf('station').GetValue(iHit))
                hit_sect  = int(hits.GetLeaf('sector').GetValue(iHit))
                hit_iSect = int(hits.GetLeaf('sector_index').GetValue(iHit))
                
                if hit_isRPC == 1: continue ## Skip everything with RPC
                
                hit_neigh = 0
                if (hit_isRPC == 1 and int(hits.GetLeaf('subsector').GetValue(iHit)) == 2): 
                    hit_neigh = ( (hit_sect % 6) == (hit_iSect % 6) )
                else:
                    hit_neigh = ( (hit_sect % 6) != (hit_iSect % 6) )

                if hit_isRPC != 0 and hit_isRPC != 1: continue  ## Only use valid hits (not -999)
                if hit_neigh: continue                          ## Don't use neighbor hits (duplicates)
                if (hit_eta > 0) != (mu_eta > 0): continue      ## Only use hits in the right endcap
                considered_hits.append(iHit)
                if hit_isRPC != 0: continue
                if hit_st == 1: continue

                if len(key_st_idx) == 0:         ## Add a key station if none exists
                    key_st_idx.append( [hit_st, iHit] )
                elif key_st_idx[0][0] > hit_st:  ## Replace the key station with better station
                    key_st_idx[0] = [hit_st, iHit]
                elif hit_st == 2:                ## Add a second key station if both are station 2
                    key_st_idx.append( [hit_st, iHit] )

            if len(key_st_idx) == 0: continue

            ## Get indices of hits best matched to tracks
            trk_hit_idxs = []  ## Indices of CSC LCTs and RPC hits in tracks
            sum_dPhi_CSC = []  ## Sum of LCT dPhis from track location
            sum_dEta_CSC = []  ## Sum of LCT dEtas from track location
            for iPair in range( len(key_st_idx) ):
                trk_hit_idxs.append([[],[]])
                sum_dPhi_CSC.append(0)
                sum_dEta_CSC.append(0)
                for iSt in range(5):
                    min_dPhi_CSC = 999
                    min_dEta_CSC = 999
                    min_dPhi_RPC = 999

                    skip_CSC = False
                    if iSt == key_st_idx[iPair][0]:
                        trk_hit_idxs[iPair][0].append(key_st_idx[iPair][1])
                        skip_CSC = True

                    ## for iHit in range(nHits):
                    for iHit in considered_hits:
                        hit_isRPC = hits.GetLeaf('isRPC').GetValue(iHit)
                        hit_eta   = hits.GetLeaf('eta').GetValue(iHit)
                        hit_st    = int(hits.GetLeaf('station').GetValue(iHit))
                        hit_ring  = int(hits.GetLeaf('ring').GetValue(iHit))
                        hit_phi   = hits.GetLeaf('phi').GetValue(iHit)
                        # hit_sect  = int(hits.GetLeaf('sector').GetValue(iHit))
                        # hit_iSect = int(hits.GetLeaf('sector_index').GetValue(iHit))
                
                        # hit_neigh = 0
                        # if (hit_isRPC == 1 and int(hits.GetLeaf('subsector').GetValue(iHit)) == 2): 
                        #     hit_neigh = ( (hit_sect % 6) == (hit_iSect % 6) )
                        # else:
                        #     hit_neigh = ( (hit_sect % 6) != (hit_iSect % 6) )

                        # if hit_isRPC != 0 and hit_isRPC != 1: continue
                        # if hit_neigh: continue
                        # if (hit_eta > 0) != (mu_eta > 0): continue
                        if (hit_st == 1 and (hit_ring % 3) == 1): hit_st = 0  ## Allow both ME1/1 and ME1/2 in same track
                        if hit_st != iSt: continue
                        if hit_isRPC == 0 and skip_CSC: continue

                        dPhi = math.acos(math.cos( hit_phi - hits.GetLeaf('phi').GetValue(key_st_idx[iPair][1]) ))
                        dEta = abs( hit_eta - hits.GetLeaf('eta').GetValue(key_st_idx[iPair][1]) )

                        if   (hit_isRPC == 0 and min_dPhi_CSC == 999):
                            trk_hit_idxs[iPair][0].append(iHit)
                            sum_dPhi_CSC[iPair] += dPhi
                            sum_dEta_CSC[iPair] += dEta
                            min_dPhi_CSC = dPhi
                        elif (hit_isRPC == 0 and min_dPhi_CSC > dPhi):
                            trk_hit_idxs[iPair][0][len(trk_hit_idxs[iPair][0]) - 1] = iHit
                            sum_dPhi_CSC[iPair] -= min_dPhi_CSC
                            sum_dEta_CSC[iPair] -= min_dEta_CSC
                            sum_dPhi_CSC[iPair] += dPhi
                            sum_dEta_CSC[iPair] += dEta
                            min_dPhi_CSC = dPhi
                        elif (hit_isRPC == 1 and min_dPhi_RPC == 999):
                            trk_hit_idxs[iPair][1].append(iHit)
                            min_dPhi_RPC = dPhi
                        elif (hit_isRPC == 1 and min_dPhi_RPC > dPhi):
                            trk_hit_idxs[iPair][1][len(trk_hit_idxs[iPair][1]) - 1] = iHit
                            min_dPhi_RPC = dPhi


            if len(trk_hit_idxs) != len(key_st_idx):
                print '\n****************************************************'
                print '*******   BIZZARE ERROR   *******'
                print 'len(trk_hit_idxs) = %d, but len(key_st_idx) = %d' % ( len(trk_hit_idxs), len(key_st_idx) )
                print key_st_idx
                print trk_hit_idxs
                print '****************************************************'

            if len(trk_hit_idxs) == 0: continue

            ## Get the track with the smallest sum dPhi (or dEta for a tie)
            minSumDPhi = 999
            minSumDEta = 999
            iMinSum    = -999
            for iPair in range( len(trk_hit_idxs) ):
                if len(trk_hit_idxs[iPair][0]) == 0: continue
                if sum_dPhi_CSC[iPair] < minSumDPhi: 
                    minSumDPhi = sum_dPhi_CSC[iPair]
                    minSumDEta = sum_dEta_CSC[iPair]
                    iMinSum = iPair
                elif sum_dPhi_CSC[iPair] == minSumDPhi and sum_dEta_CSC[iPair] < minSumDEta: 
                    minSumDPhi = sum_dPhi_CSC[iPair]
                    minSumDEta = sum_dEta_CSC[iPair]
                    iMinSum = iPair

            ## Store all the CSC and RPC hit indices for that track
            trk_hit_idx = trk_hit_idxs[iMinSum][0] + trk_hit_idxs[iMinSum][1]

            nHit_in_station = [[0,0], [0,0], [0,0], [0,0], [0,0]]
            for iHit in trk_hit_idx:
                hit_isRPC = int(hits.GetLeaf('isRPC').GetValue(iHit))
                hit_st    = int(hits.GetLeaf('station').GetValue(iHit))
                hit_ring  = int(hits.GetLeaf('ring').GetValue(iHit))
                if hit_st == 1 and (hit_ring % 3) == 1: hit_st = 0
                nHit_in_station[hit_st][hit_isRPC] += 1
                
            for iSt in range(5):
                for iDet in range(2):
                    if ( nHit_in_station[iSt][iDet] > 1 ):
                        print '\n****************************************************'
                        print '*******   BIZZARE ERROR   *******'
                        print nHit_in_station
                        print '\nFound track has %d hits' % len(trk_hit_idx)
                        for iHit in trk_hit_idx:
                            print 'Hit %d: RPC = %d, station %d, ring %d, eta %f, phi %f' % ( iHit, hits.GetLeaf('isRPC').GetValue(iHit),
                                                                                              hits.GetLeaf('station').GetValue(iHit),
                                                                                              hits.GetLeaf('ring').GetValue(iHit),
                                                                                              hits.GetLeaf('eta').GetValue(iHit),
                                                                                              hits.GetLeaf('phi').GetValue(iHit) )
                        print '****************************************************'
                        break
            
            ###############################
            ## Plot sums of dPhi quantities
            ###############################

            ## Properties of muons with LCTs in all 4 stations
            hit_idx = [[], [], [], []]
            ## for iHit in range(nHits):
            for iHit in trk_hit_idx:
                hit_isRPC = hits.GetLeaf('isRPC').GetValue(iHit)
                hit_st    = int(hits.GetLeaf('station').GetValue(iHit))
                hit_eta   = hits.GetLeaf('eta').GetValue(iHit)
                # hit_sect  = int(hits.GetLeaf('sector').GetValue(iHit))
                # hit_iSect = int(hits.GetLeaf('sector_index').GetValue(iHit))

                # hit_neigh = 0
                # if (hit_isRPC == 1 and int(hits.GetLeaf('subsector').GetValue(iHit)) == 2): 
                #     hit_neigh = ( (hit_sect % 6) == (hit_iSect % 6) )
                # else:
                #     hit_neigh = ( (hit_sect % 6) != (hit_iSect % 6) )

                # if hit_isRPC != 0 and hit_isRPC != 1: continue
                # if hit_neigh: continue
                # if (hit_eta > 0) != (mu_eta > 0): continue
                if hit_isRPC != 0: continue
                hit_idx[hit_st - 1].append(iHit)

            for iSt1 in hit_idx[0]:
                for iSt2 in hit_idx[1]:
                    for iSt3 in hit_idx[2]:
                        for iSt4 in hit_idx[3]:
                            
                            dPhis = [-999, -999, -999, -999, -999, -999]
                            for iSt in range(3):
                                if iSt == 0: iStX = iSt1
                                if iSt == 1: iStX = iSt2
                                if iSt == 2: iStX = iSt3
                                for jSt in range(iSt+1, 4):
                                    if jSt == 1: jStY = iSt2
                                    if jSt == 2: jStY = iSt3
                                    if jSt == 3: jStY = iSt4
                                    hit1_phi = math.radians( hits.GetLeaf('phi').GetValue(iStX) )
                                    hit2_phi = math.radians( hits.GetLeaf('phi').GetValue(jStY) )
                                    
                                    dPhi = math.acos(math.cos(hit2_phi - hit1_phi)) 
                                    if abs(hit2_phi - hit1_phi) > 0:
                                        dPhi *= math.sin(hit2_phi - hit1_phi) / abs(math.sin(hit2_phi - hit1_phi))
                                    if iSt == 0: dPhis[jSt - iSt - 1] = math.degrees(dPhi * mu_charge)
                                    if iSt == 1: dPhis[jSt - iSt + 2] = math.degrees(dPhi * mu_charge)
                                    if iSt == 2: dPhis[jSt - iSt + 4] = math.degrees(dPhi * mu_charge)
                                    
                            sum_dPhi_St1  = dPhis[0] + dPhis[1] + dPhis[2]
                            sumA_dPhi_St1 = abs(dPhis[0]) + abs(dPhis[1]) + abs(dPhis[2]) 
                            sum_dPhi_St2  = dPhis[0] + dPhis[3] + dPhis[4]
                            sumA_dPhi_St2 = abs(dPhis[0]) + abs(dPhis[3]) + abs(dPhis[4]) 
                            sum_dPhi_St3  = dPhis[1] + dPhis[3] + dPhis[5]
                            sumA_dPhi_St3 = abs(dPhis[1]) + abs(dPhis[3]) + abs(dPhis[5]) 
                            sum_dPhi_St4  = dPhis[2] + dPhis[4] + dPhis[5]
                            sumA_dPhi_St4 = abs(dPhis[2]) + abs(dPhis[4]) + abs(dPhis[5])
                            
                            sum_dPhi4  = dPhis[0] + dPhis[1] + dPhis[2] + dPhis[3] + dPhis[4] + dPhis[5]
                            sumA_dPhi4 = abs(dPhis[0]) + abs(dPhis[1]) + abs(dPhis[2]) + abs(dPhis[3]) + abs(dPhis[4]) + abs(dPhis[5])
                            sum_dPhi3  = sum_dPhi4
                            sumA_dPhi3 = sumA_dPhi4

                            out_station = -999
                            if   (sumA_dPhi_St1 >= sumA_dPhi_St2 and sumA_dPhi_St1 >= sumA_dPhi_St3 and sumA_dPhi_St1 >= sumA_dPhi_St4):
                                out_station = 1
                                sum_dPhi3  -= (dPhis[0] + dPhis[1] + dPhis[2])
                                sumA_dPhi3 -= (abs(dPhis[0]) + abs(dPhis[1]) + abs(dPhis[2]))
                            elif (sumA_dPhi_St2 >  sumA_dPhi_St1 and sumA_dPhi_St2 >= sumA_dPhi_St3 and sumA_dPhi_St2 >= sumA_dPhi_St4):
                                out_station = 2
                                sum_dPhi3  -= (dPhis[0] + dPhis[3] + dPhis[4])
                                sumA_dPhi3 -= (abs(dPhis[0]) + abs(dPhis[3]) + abs(dPhis[4]))
                            elif (sumA_dPhi_St3 >  sumA_dPhi_St1 and sumA_dPhi_St3 >  sumA_dPhi_St2 and sumA_dPhi_St3 >= sumA_dPhi_St4):
                                out_station = 3
                                sum_dPhi3  -= (dPhis[1] + dPhis[3] + dPhis[5])
                                sumA_dPhi3 -= (abs(dPhis[1]) + abs(dPhis[3]) + abs(dPhis[5]))
                            elif (sumA_dPhi_St4 >  sumA_dPhi_St1 and sumA_dPhi_St4 >  sumA_dPhi_St2 and sumA_dPhi_St4 >  sumA_dPhi_St3):
                                out_station = 4
                                sum_dPhi3  -= (dPhis[2] + dPhis[4] + dPhis[5])
                                sumA_dPhi3 -= (abs(dPhis[2]) + abs(dPhis[4]) + abs(dPhis[5]))
                                        
                            for iPt in pt_cuts.keys():
                                if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue
                                
                                for iEta in eta_cuts.keys():
                                    if (abs(mu_eta) < eta_cuts[iEta][0]) or (abs(mu_eta) > eta_cuts[iEta][1]): continue

                                    h_sum4_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sum_dPhi4, sum4_dPh_thin[2]-0.01), sum4_dPh_thin[1]+0.01) )
                                    h_sum4_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sum_dPhi4, sum4_dPh_bins[2]-0.01), sum4_dPh_bins[1]+0.01) )
                                    h_sum4_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sum_dPhi4, sum4_dPh_wide[2]-0.01), sum4_dPh_wide[1]+0.01) )
                                    
                                    h_sum4A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sumA_dPhi4, sum4A_dPh_thin[2]-0.01), sum4A_dPh_thin[1]+0.01) )
                                    h_sum4A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sumA_dPhi4, sum4A_dPh_bins[2]-0.01), sum4A_dPh_bins[1]+0.01) )
                                    h_sum4A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sumA_dPhi4, sum4A_dPh_wide[2]-0.01), sum4A_dPh_wide[1]+0.01) )
                                    
                                    h_sum3_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sum_dPhi3, sum3_dPh_thin[2]-0.01), sum3_dPh_thin[1]+0.01) )
                                    h_sum3_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sum_dPhi3, sum3_dPh_bins[2]-0.01), sum3_dPh_bins[1]+0.01) )
                                    h_sum3_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sum_dPhi3, sum3_dPh_wide[2]-0.01), sum3_dPh_wide[1]+0.01) )
                                    
                                    h_sum3A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sumA_dPhi3, sum3A_dPh_thin[2]-0.01), sum3A_dPh_thin[1]+0.01) )
                                    h_sum3A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sumA_dPhi3, sum3A_dPh_bins[2]-0.01), sum3A_dPh_bins[1]+0.01) )
                                    h_sum3A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( sumA_dPhi3, sum3A_dPh_wide[2]-0.01), sum3A_dPh_wide[1]+0.01) )

                                    if (sum_dPhi4 == 0 and sumA_dPhi4 == 0): h_sum4_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].Fill( 0 )
                                    else: h_sum4_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( (sum_dPhi4 / sumA_dPhi4), frac_bins[2]-0.01), frac_bins[1]+0.01) )
                                    if (sum_dPhi3 == 0 and sumA_dPhi3 == 0): h_sum3_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].Fill( 0 )
                                    else: h_sum3_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( (sum_dPhi3 / sumA_dPhi3), frac_bins[2]-0.01), frac_bins[1]+0.01) )
                                    h_outlier_st['pt_%s_eta_%s' % (iPt, iEta)].Fill( max( min( out_station, st_bins[2]-0.01), st_bins[1]+0.01) )

                                    h_sum4A_dPhi_thin['pt_%s_eta_%s_st_%d' % (iPt, iEta, out_station)].Fill( max( min( sumA_dPhi4, sum4A_dPh_thin[2]-0.01), sum4A_dPh_thin[1]+0.01) )
                                    h_sum4A_dPhi     ['pt_%s_eta_%s_st_%d' % (iPt, iEta, out_station)].Fill( max( min( sumA_dPhi4, sum4A_dPh_bins[2]-0.01), sum4A_dPh_bins[1]+0.01) )
                                    h_sum4A_dPhi_wide['pt_%s_eta_%s_st_%d' % (iPt, iEta, out_station)].Fill( max( min( sumA_dPhi4, sum4A_dPh_wide[2]-0.01), sum4A_dPh_wide[1]+0.01) )

                            

            #########################################
            ## dPhi / dTheta between any two stations
            #########################################

            for iSt in st_cuts.keys():

                ## for iHit in range(nHits):
                for iHit in trk_hit_idx:
                    hit1_isRPC = hits.GetLeaf('isRPC').GetValue(iHit)
                    hit1_st    = int(hits.GetLeaf('station').GetValue(iHit))
                    hit1_ring  = int(hits.GetLeaf('ring').GetValue(iHit))
                    hit1_eta   = hits.GetLeaf('eta').GetValue(iHit)
                    hit1_phi   = math.radians( hits.GetLeaf('phi').GetValue(iHit) )
                    hit1_theta = hits.GetLeaf('theta').GetValue(iHit)
                    hit1_patt  = int(hits.GetLeaf('pattern').GetValue(iHit))
                    # hit1_sect  = int(hits.GetLeaf('sector').GetValue(iHit))
                    # hit1_iSect = int(hits.GetLeaf('sector_index').GetValue(iHit))
                    
                    # hit1_neigh = 0
                    # if (hit1_isRPC == 1 and int(hits.GetLeaf('subsector').GetValue(iHit)) == 2): 
                    #     hit1_neigh = ( (hit1_sect % 6) == (hit1_iSect % 6) )
                    # else:
                    #     hit1_neigh = ( (hit1_sect % 6) != (hit1_iSect % 6) )

                    # if hit1_isRPC != 0 and hit1_isRPC != 1: continue
                    # if hit1_neigh: continue
                    # if (hit1_eta > 0) != (mu_eta > 0): continue
                    if hit1_st != st_cuts[iSt][0]: continue
                    
                    ## for jHit in range(nHits):

                    bend = -5;
                    if   (hit1_patt == 10):        bend = 0
                    elif ( (hit1_patt % 2) == 0 ): bend = (10 - hit1_patt) / 2
                    elif ( (hit1_patt % 2) == 1 ): bend = -1 * (11 - hit1_patt) / 2
                    if (hit1_eta > 0):            bend *= -1
                    if (mu_charge != 1):          bend *= -1
                    for xSt in range(1, 5):
                        if (hit1_st != xSt): continue
                        for iPt in pt_cuts.keys():
                            if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue
                            for iEta in eta_cuts.keys():
                                if (abs(mu_eta) < eta_cuts[iEta][0]) or (abs(mu_eta) > eta_cuts[iEta][1]): continue
                                h_bend['pt_%s_eta_%s_st_%d' % (iPt, iEta, xSt)].Fill( bend )

                    for jHit in trk_hit_idx:
                        if iHit == jHit: continue
                        
                        hit2_isRPC = hits.GetLeaf('isRPC').GetValue(jHit)
                        hit2_st    = hits.GetLeaf('station').GetValue(jHit)
                        hit2_ring  = hits.GetLeaf('ring').GetValue(jHit)
                        hit2_eta   = hits.GetLeaf('eta').GetValue(jHit)
                        hit2_phi   = math.radians( hits.GetLeaf('phi').GetValue(jHit) )
                        hit2_theta = hits.GetLeaf('theta').GetValue(jHit)
                        # hit2_sect  = int(hits.GetLeaf('sector').GetValue(jHit))
                        # hit2_iSect = int(hits.GetLeaf('sector_index').GetValue(jHit))
                                
                        # hit2_neigh = 0
                        # if (hit2_isRPC == 1 and int(hits.GetLeaf('subsector').GetValue(jHit)) == 2): 
                        #     hit2_neigh = ( (hit2_sect % 6) == hit2_iSect )
                        # else:
                        #     hit2_neigh = ( (hit2_sect % 6) != hit2_iSect )

                        # if hit2_isRPC != 0 and hit2_isRPC != 1: continue
                        # if hit2_neigh: continue
                        # if (hit2_eta > 0) != (mu_eta > 0): continue
                        if hit2_st != st_cuts[iSt][1]: continue
                        
                        dPhi = math.acos(math.cos(hit2_phi - hit1_phi)) 
                        if abs(hit2_phi - hit1_phi) > 0:
                            dPhi *= math.sin(hit2_phi - hit1_phi) / abs(math.sin(hit2_phi - hit1_phi))
                        dPhi = math.degrees(dPhi)

                        dTheta = hit2_theta - hit1_theta

                        if ( hit1_isRPC == 0 and hit2_isRPC == 0 and hit1_st == 1 and hit2_st == 1 ):
                            if ( (hit1_ring == 2) and (hit2_ring % 3) == 1 ):
                                dPhi *= -1.0
                                dTheta *= -1.0
                            elif not ( (hit2_ring == 2) and (hit1_ring % 3) == 1 ):
                                print '\n****************************************************'
                                print '*******   BIZZARE ERROR   *******'
                                print 'Hits not where they are supposed to be'
                                print 'Hit %d: RPC = %d, station %d, ring %d, eta %f, phi %f' % ( iHit, hits.GetLeaf('isRPC').GetValue(iHit),
                                                                                                  hits.GetLeaf('station').GetValue(iHit),
                                                                                                  hits.GetLeaf('ring').GetValue(iHit),
                                                                                                  hits.GetLeaf('eta').GetValue(iHit),
                                                                                                  hits.GetLeaf('phi').GetValue(iHit) )
                                print 'Hit %d: RPC = %d, station %d, ring %d, eta %f, phi %f' % ( jHit, hits.GetLeaf('isRPC').GetValue(jHit),
                                                                                                  hits.GetLeaf('station').GetValue(jHit),
                                                                                                  hits.GetLeaf('ring').GetValue(jHit),
                                                                                                  hits.GetLeaf('eta').GetValue(jHit),
                                                                                                  hits.GetLeaf('phi').GetValue(jHit) )
                                print '****************************************************'

                        
                        if hit1_isRPC == 1: iDet1 = 'RPC'
                        else:               iDet1 = 'CSC'
                        if hit2_isRPC == 1: iDet2 = 'RPC'
                        else:               iDet2 = 'CSC'
                        iDet = '%s_%s' % (iDet1, iDet2)
                        
                        for iPt in pt_cuts.keys():
                            if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue
                            
                            for iEta in eta_cuts.keys():
                                if (abs(mu_eta) < eta_cuts[iEta][0]) or (abs(mu_eta) > eta_cuts[iEta][1]): continue

                                h_dTheta_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Fill( max( min( dTheta, dTh_wide[2] - 0.0001), dTh_wide[1] + 0.0001 ) )
                                
                                if abs(dTheta) > dTheta_max: continue
                                h_dTheta     ['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Fill( max( min( dTheta, dTh_bins[2] - 0.0001), dTh_bins[1] + 0.0001 ) )
                                h_dPhi_thin  ['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Fill( max( min( dPhi * mu_charge, dPh_thin[2] - 0.0001), dPh_thin[1] + 0.0001 ) )
                                h_dPhi       ['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Fill( max( min( dPhi * mu_charge, dPh_bins[2] - 0.0001), dPh_bins[1] + 0.0001 ) )
                                h_dPhi_wide  ['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Fill( max( min( dPhi * mu_charge, dPh_wide[2] - 0.0001), dPh_wide[1] + 0.0001 ) )
                        



################
## Print results
################

# print '***********************************'
# print '*** %s_%d%s%s%s%s efficiency ***' % (trig_WP, pt_cut, dEta_str, BX0_str, uGMT_str, HLT_str)
# print '***********************************'
# print 'uGMT: %.1f +/- %.1f%%' % (100 * heta_trig.Integral() / heta.Integral(), 
#                                (100 * heta_trig.Integral() / heta.Integral()) * math.sqrt(heta.Integral())/heta.Integral() )
# print 'BMTF: %.1f +/- %.1f%%' % (100 * hpt_bmtf_trig.Integral() / hpt_bmtf.Integral(), 
#                                (100 * hpt_bmtf_trig.Integral() / hpt_bmtf.Integral()) * math.sqrt(hpt_bmtf.Integral())/hpt_bmtf.Integral() )
# print 'OMTF: %.1f +/- %.1f%%' % (100 * hpt_omtf_trig.Integral() / hpt_omtf.Integral(), 
#                                (100 * hpt_omtf_trig.Integral() / hpt_omtf.Integral()) * math.sqrt(hpt_omtf.Integral())/hpt_omtf.Integral() )
# print 'EMTF: %.1f +/- %.1f%%' % (100 * hpt_emtf_trig.Integral() / hpt_emtf.Integral(), 
#                                (100 * hpt_emtf_trig.Integral() / hpt_emtf.Integral()) * math.sqrt(hpt_emtf.Integral())/hpt_emtf.Integral() )

######################
## Save the histograms
######################

    out_file.cd()

    colors = [kMagenta, kRed, kOrange, kGreen, kBlue, kViolet-2, kViolet+2, kBlack]
    iColor = 0
    for iPt in pt_cuts.keys():
        color = colors[iColor]
        iColor += 1
        for iEta in eta_cuts.keys():

            h_sum4_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum4_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum4_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Write()
            
            h_sum4A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum4A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum4A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Write()
            
            h_sum3_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum3_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum3_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Write()
            
            h_sum3A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3A_dPhi_thin['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum3A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3A_dPhi     ['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum3A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3A_dPhi_wide['pt_%s_eta_%s' % (iPt, iEta)].Write()
            
            h_sum4_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum4_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum4_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_sum3_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_sum3_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_sum3_dPhi_frac['pt_%s_eta_%s' % (iPt, iEta)].Write()
            h_outlier_st['pt_%s_eta_%s' % (iPt, iEta)].SetLineWidth(2)
            h_outlier_st['pt_%s_eta_%s' % (iPt, iEta)].SetLineColor(color)
            h_outlier_st['pt_%s_eta_%s' % (iPt, iEta)].Write()

            for iSt in range(1, 5):
                h_sum4A_dPhi_thin['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].SetLineWidth(2)
                h_sum4A_dPhi_thin['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].SetLineColor(color)
                h_sum4A_dPhi_thin['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].Write()
                h_sum4A_dPhi     ['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].SetLineWidth(2)
                h_sum4A_dPhi     ['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].SetLineColor(color)
                h_sum4A_dPhi     ['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].Write()
                h_sum4A_dPhi_wide['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].SetLineWidth(2)
                h_sum4A_dPhi_wide['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].SetLineColor(color)
                h_sum4A_dPhi_wide['pt_%s_eta_%s_st_%d' % (iPt, iEta, iSt)].Write()

                h_bend['pt_%s_eta_%s_st_%s' % (iPt, iEta, iSt)].SetLineWidth(2)
                h_bend['pt_%s_eta_%s_st_%s' % (iPt, iEta, iSt)].SetLineColor(color)
                h_bend['pt_%s_eta_%s_st_%s' % (iPt, iEta, iSt)].Write()
            
            for iSt in st_cuts.keys():
                for iDet in det_cuts.keys():

                    h_dPhi_thin['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineWidth(2)
                    h_dPhi_thin['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineColor(color)
                    h_dPhi_thin['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Write()

                    h_dPhi['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineWidth(2)
                    h_dPhi['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineColor(color)
                    h_dPhi['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Write()

                    h_dPhi_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineWidth(2)
                    h_dPhi_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineColor(color)
                    h_dPhi_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Write()

                    h_dTheta['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineWidth(2)
                    h_dTheta['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineColor(color)
                    h_dTheta['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Write()

                    h_dTheta_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineWidth(2)
                    h_dTheta_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].SetLineColor(color)
                    h_dTheta_wide['pt_%s_eta_%s_st_%s_%s' % (iPt, iEta, iSt, iDet)].Write()

    del out_file


if __name__ == '__main__':
    main()

