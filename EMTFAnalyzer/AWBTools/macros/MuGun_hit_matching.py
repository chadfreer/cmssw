#! /usr/bin/env python

import sys
import math
from ROOT import *
import numpy as np
from array import *
# from eff_modules import *

def main():

    print 'Inside MuGun_hit_matching.py'

###################
## Initialize files
###################

    file_name_1 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_noRPC_300k.root'
    file_name_2 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_RPC_300k.root'

    file_1 = TFile.Open(file_name_1)
    file_2 = TFile.Open(file_name_2)
    
    tree_1 = file_1.Get('ntuple/tree')
    tree_2 = file_2.Get('ntuple/tree')
    
    out_file = TFile('plots/MuGun_hit_matching_v3.root', 'recreate')
    
#################
## Selection cuts
#################

    eta_cuts = {}
    # eta_cuts['wide']      = [0.80, 2.70, '0.8 < |#eta| < 2.7']  ## Input sample only covers 1.2 - 2.4
    eta_cuts['all']       = [1.20, 2.40, '1.2 < |#eta| < 2.4']
    eta_cuts['1p2_1p85']  = [1.20, 1.85, '1.2 < |#eta| < 1.85']
    eta_cuts['1p85_2p4']  = [1.85, 2.40, '1.85 < |#eta| < 2.4']
    eta_cuts['1p2_1p55']  = [1.20, 1.55, '1.2 < |#eta| < 1.55']
    eta_cuts['1p55_1p85'] = [1.55, 1.85, '1.55 < |#eta| < 1.85']
    eta_cuts['1p85_2p1']  = [1.85, 2.10, '1.85 < |#eta| < 2.1']
    eta_cuts['2p1_2p4']   = [2.10, 2.40, '2.1 < |#eta| < 2.4']
    
    pt_cuts = {}
    # pt_cuts['all']      = [  0, 1000]
    # pt_cuts['10_up']  = [ 10, 1000, 'p_{T} > 10 GeV']
    # pt_cuts['1_5']      = [  0,    5, '1 < p_{T} < 5 GeV']
    # pt_cuts['5_15']     = [  5,   15, '5 < p_{T} < 15 GeV']
    # pt_cuts['15_40']    = [ 15,   40, '15 < p_{T} < 40 GeV']
    # pt_cuts['40_100']   = [ 40,  100]
    # pt_cuts['100_250']  = [100,  250]
    # pt_cuts['250_up']   = [250, 1000]  
    # pt_cuts['20_200']   = [  20,   200, '20 < p_{T} < 200 GeV']
    # pt_cuts['100_up']   = [ 100,  1000, '100 < p_{T} < 1000 GeV']
    pt_cuts['20_up']    = [  20,  1000, '20 < p_{T} < 1000 GeV']
    
    qual_cuts = {}
    # qual_cuts['MuOpen']       = [[3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15], 'MuOpen tracks']
    # qual_cuts['DoubleMu']     = [[7, 10, 11, 12, 13, 14, 15], 'DoubleMu tracks']
    # qual_cuts['SingleMu']     = [[11, 13, 14, 15], 'SingleMu tracks']
    # qual_cuts['DoubleMuOnly'] = [[7, 10, 12], 'DoubleMu-only tracks']
    # qual_cuts['MuOpenOnly']   = [[3, 5, 6, 9], 'MuOpen-only tracks']
    # qual_cuts['ge3_hit']      = [[[7, 11, 13, 14, 15], '3-/4-station tracks']
    # qual_cuts['eq2_hit']      = [[3, 5, 6, 9, 10, 12], '2-station tracks']
    # qual_cuts['eq3_hit']      = [[7, 11, 13, 14], '3-station tracks']
    # qual_cuts['eq4_hit']      = [[15], '4-station tracks']
    # qual_cuts['mode_7']       = [[7], 'station 1-3-4 tracks']
    # qual_cuts['mode_10']      = [[10], 'station 1-3-4 tracks']
    # qual_cuts['mode_12']      = [[12], 'station 1-3-4 tracks']
    # qual_cuts['mode_11']      = [[11], 'station 1-3-4 tracks']
    # qual_cuts['mode_13']      = [[13], 'station 1-3-4 tracks']
    # qual_cuts['mode_14']      = [[14], 'station 1-3-4 tracks']
    # qual_cuts['mode_15']      = [[15], '4-station tracks']

    st_cuts = {}
    st_cuts['St1'] = [[1], 'Station 1']
    st_cuts['St2'] = [[2], 'Station 2']
    st_cuts['St3'] = [[3], 'Station 3']
    st_cuts['St4'] = [[4], 'Station 4']
    
#############
## Histograms
#############
    
    eta_bins = [150, 1.0, 2.5]
    th_bins  = [270, 8, 35]
    phi_bins = [30, 0, 60]
    
    h_eta       = {}
    h_eta_hit   = {}
    h_eta_trk   = {}
    h_phi       = {}
    h_phi_hit   = {}
    h_phi_trk   = {}
    h_th_hit_Fn = {}
    h_th_hit_Fd = {}
    h_th_hit_Rn = {}
    h_th_hit_Rd = {}

    for iDet in ['CSC', 'RPC']:
        if iDet == 'CSC': det_str = 'CSC'
        if iDet == 'RPC': det_str = 'RPC'

        for iPt in pt_cuts.keys():
            pt_str = pt_cuts[iPt][2]
            
            h_eta['pt_%s_%s' % (iPt, iDet)] = TH1D('h_eta_pt_%s_%s' % (iPt, iDet), 
                                                   'GEN muon |#eta|, %s' % (pt_str),
                                                   eta_bins[0], eta_bins[1], eta_bins[2])
            h_phi['pt_%s_%s' % (iPt, iDet)] = TH1D('h_phi_pt_%s_%s' % (iPt, iDet), 
                                                   'GEN muon |#phi|, %s' % (pt_str),
                                                   phi_bins[0], phi_bins[1], phi_bins[2])
                
            h_eta['pt_%s_%s' % (iPt, iDet)].GetXaxis().SetTitle('GEN muon |#eta|')
            h_phi['pt_%s_%s' % (iPt, iDet)].GetXaxis().SetTitle('GEN muon #phi')

            for iSt in st_cuts.keys():
                st_str = st_cuts[iSt][1]
                
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] = TH1D('h_eta_pt_%s_%s_hit_%s' % (iPt, iDet, iSt), 
                                                                       'GEN muon |#eta|, %s, %s in %s' % (pt_str, st_str, det_str),
                                                                       eta_bins[0], eta_bins[1], eta_bins[2])

                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)] = TH1D('h_eta_pt_%s_%s_trk_%s' % (iPt, iDet, iSt), 
                                                                       'GEN muon |#eta|, %s, %s in track in %s' % (pt_str, st_str, det_str),
                                                                       eta_bins[0], eta_bins[1], eta_bins[2])
                
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] = TH1D('h_phi_pt_%s_%s_hit_%s' % (iPt, iDet, iSt), 
                                                                       'GEN muon |#phi|, %s, %s in %s' % (pt_str, st_str, det_str),
                                                                       phi_bins[0], phi_bins[1], phi_bins[2])
                
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)] = TH1D('h_phi_pt_%s_%s_trk_%s' % (iPt, iDet, iSt), 
                                                                       'GEN muon |#phi|, %s, %s in track in %s' % (pt_str, st_str, det_str),
                                                                       phi_bins[0], phi_bins[1], phi_bins[2])
                
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] = TH1D('h_eta_pt_%s_%s_hit_%s_Fn' % (iPt, iDet, iSt), 
                                                                         # 'GEN muon |#theta|, %s, %s in front %s' % (pt_str, st_str, det_str),
                                                                         'GEN muon |#theta|, %s, %s in %s' % (pt_str, st_str, det_str),
                                                                         th_bins[0], th_bins[1], th_bins[2])
                h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] = TH1D('h_eta_pt_%s_%s_hit_%s_Fd' % (iPt, iDet, iSt), 
                                                                         # 'GEN muon |#theta|, %s, %s in front %s' % (pt_str, st_str, det_str),
                                                                         'GEN muon |#theta|, %s, %s in %s' % (pt_str, st_str, det_str),
                                                                         th_bins[0], th_bins[1], th_bins[2])
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] = TH1D('h_eta_pt_%s_%s_hit_%s_Rn' % (iPt, iDet, iSt), 
                                                                         # 'GEN muon |#theta|, %s, %s in rear %s' % (pt_str, st_str, det_str),
                                                                         'GEN muon |#theta|, %s, %s in %s' % (pt_str, st_str, det_str),
                                                                         th_bins[0], th_bins[1], th_bins[2])
                h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] = TH1D('h_eta_pt_%s_%s_hit_%s_Rd' % (iPt, iDet, iSt), 
                                                                         # 'GEN muon |#theta|, %s, %s in rear %s' % (pt_str, st_str, det_str),
                                                                         'GEN muon |#theta|, %s, %s in %s' % (pt_str, st_str, det_str),
                                                                         th_bins[0], th_bins[1], th_bins[2])

                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon |#eta|')
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon |#eta|')
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon #phi')
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon #phi')
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon |#theta|')
                h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon |#theta|')
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon |#theta|')
                h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetXaxis().SetTitle('GEN muon |#theta|')

#############
## Event loop
#############
                
    # for iDet in ['CSC', 'RPC']:
    for iDet in ['CSC']:
        if iDet == 'CSC':
            tree = tree_1
        if iDet == 'RPC':
            tree = tree_2
        
        for iEvt in range(tree.GetEntries()):
            
            # if iEvt > 100000: break
            if iEvt % 10000 is 0: print 'Event #', iEvt

            tree.GetEntry(iEvt)

            muons = tree.GetBranch('muon')
            trks  = tree.GetBranch('track')
            hits  = tree.GetBranch('hit')

            nMuons = int(muons.GetLeaf('nMuons').GetValue())
            nTrks  = int(trks.GetLeaf('nTracks').GetValue())
            nHits  = int(hits.GetLeaf('nHits').GetValue())

            mu1_eta = muons.GetLeaf('eta').GetValue(0)
            if abs(mu1_eta) < 1.0: continue

            for iMu in range(nMuons):
                mu_pt     = muons.GetLeaf('pt').GetValue(iMu)
                mu_eta    = muons.GetLeaf('eta').GetValue(iMu)
                mu_theta  = muons.GetLeaf('theta').GetValue(iMu) ## In degrees
                mu_phi    = muons.GetLeaf('phi').GetValue(iMu)   ## In degrees
                mu_charge = int(muons.GetLeaf('charge').GetValue(iMu))

                ## Correct for muon propagation - see macros/MuGun_propagation.py
                mu_phi = mu_phi + (mu_charge / mu_pt) * (10.23 - (5.1155 * abs(mu_theta)) + (0.02259 * pow(mu_theta, 2)))
                ## Shift phi into [0, 360] range
                if mu_phi < 0: mu_phi += 360.
                ## Shift phi into [0, 60] range
                mu_phi_sxt = (mu_phi % 60)
                ## Only fill plots vs. phi in full-coverage eta range
                fill_phi = (abs(mu_eta) > 1.25 and abs(mu_eta) < 2.35)


                for iPt in pt_cuts.keys():
                    if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue

                    h_eta['pt_%s_%s' % (iPt, iDet)].Fill( abs(mu_eta) )
                    if fill_phi: h_phi['pt_%s_%s' % (iPt, iDet)].Fill( abs(mu_phi_sxt) )

                    num_hits = {}
                    num_trk_hits = {}
                    for iSt in st_cuts.keys():
                        num_hits[iSt] = {}
                        num_trk_hits[iSt] = {}
                        for jSt in st_cuts[iSt][0]:
                            num_hits[iSt][jSt] = 0
                            num_trk_hits[iSt][jSt] = 0

                    ## print '\nMuon pT = %f, eta = %f, phi = %f' % ( mu_pt, mu_eta, muons.GetLeaf('phi').GetValue(iMu) )
                    for iHit in range(nHits):
                        hit_isRPC = hits.GetLeaf('isRPC').GetValue(iHit)
                        hit_st    = int(hits.GetLeaf('station').GetValue(iHit))
                        hit_eta   = hits.GetLeaf('eta').GetValue(iHit)
                        hit_phi   = hits.GetLeaf('phi').GetValue(iHit)
                        hit_sect  = int(hits.GetLeaf('sector').GetValue(iHit))
                        hit_iSect = int(hits.GetLeaf('sector_index').GetValue(iHit))

                        hit_neigh = 0
                        if (hit_isRPC == 1 and int(hits.GetLeaf('subsector').GetValue(iHit)) == 2):
                            hit_neigh = ( (hit_sect % 6) == (hit_iSect % 6) )
                        else:
                            hit_neigh = ( (hit_sect % 6) != (hit_iSect % 6) )

                        # if hit_neigh: continue
                        if hit_isRPC != (iDet == 'RPC'):  continue
                        if (hit_eta > 0) != (mu_eta > 0): continue
                        for iSt in st_cuts.keys():
                            for jSt in st_cuts[iSt][0]:
                                if hit_st == jSt: num_hits[iSt][jSt] += 1

                    for iTrk in range(nTrks):
                        for jSt in range(1, 5):
                            trk_hit_isRPC = trks.GetLeaf('hit_isRPC').GetValue(iTrk*4 + (jSt - 1))
                            trk_hit_st    = int(trks.GetLeaf('hit_station').GetValue(iTrk*4 + (jSt - 1)))
                            trk_hit_eta   = trks.GetLeaf('hit_eta').GetValue(iTrk*4 + (jSt - 1))
                        
                            if trk_hit_isRPC != (iDet == 'RPC'):  continue
                            if (trk_hit_eta > 0) != (mu_eta > 0): continue
                            for iSt in st_cuts.keys():
                                for jSt in st_cuts[iSt][0]:
                                    if trk_hit_st == jSt: num_trk_hits[iSt][jSt] += 1
                                    if iTrk == 0 and num_trk_hits[iSt][jSt] > 1:
                                        print '\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                                        print '!!!!!!!   CRAZY ISSUE   !!!!!!!'
                                        print 'In track %d, num_trk_hits[%s][%d] = %d' % ( iTrk, iSt, jSt, num_trk_hits[iSt][jSt] )
                                        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'


                    for iSt in st_cuts.keys():
                        st_str = st_cuts[iSt][1]                        

                        iTh = abs(mu_theta)
                        ## Compute whether muon will pass through front or rear CSC stations
                        if ( iSt == 'St1' or (iSt == 'St2' and iTh > 23.0) or (iSt == 'St3' and iTh > 20.6) or (iSt == 'St4' and iTh > 18.9) ):
                            if (iSt == 'St1' or iSt == 'St2'): 
                                front_CSC = ((mu_phi + 345.) % 20) < 10.
                            else:
                                front_CSC = ((mu_phi + 345.) % 20) > 10.
                        else:
                            if (iSt == 'St2'):
                                front_CSC = ((mu_phi + 345.) % 40) > 20.
                            else:
                                front_CSC = ((mu_phi + 345.) % 40) < 20.

                        if front_CSC: h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Fill( abs(mu_theta) )
                        else:         h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Fill( abs(mu_theta) )

                        hit_pass = True
                        trk_hit_pass = True
                        for jSt in st_cuts[iSt][0]:
                            if num_hits[iSt][jSt] < 1: hit_pass = False
                            if num_trk_hits[iSt][jSt] < 1: trk_hit_pass = False

                        if hit_pass:
                            h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Fill( abs(mu_eta) )
                            if fill_phi: h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Fill( mu_phi_sxt )
                            if front_CSC: h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Fill( abs(mu_theta) )
                            else:         h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Fill( abs(mu_theta) )

                        if trk_hit_pass:
                            h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Fill( abs(mu_eta) )
                            if fill_phi: h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Fill( mu_phi_sxt )



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

    # for key in h_eta.keys():
    #     h_eta[key].SetLineWidth(2)
    #     h_eta[key].GetXaxis().SetTitle('GEN muon |#eta|')
    #     h_eta[key].GetYaxis().SetTitle('Events')
    # for key in h_eta_trg.keys():
    #     h_eta_trg[key].SetLineWidth(2)
    #     h_eta_trg[key].GetXaxis().SetTitle('GEN muon |#eta|')
    #     h_eta_trg[key].GetYaxis().SetTitle('Events')
    # for key in h_pt.keys():
    #     h_pt[key].SetLineWidth(2)
    #     h_pt[key].GetXaxis().SetTitle('GEN muon p_{T}')
    #     h_pt[key].GetYaxis().SetTitle('Events')
    # for key in h_pt_trg.keys():
    #     h_pt_trg[key].SetLineWidth(2)
    #     h_pt_trg[key].GetXaxis().SetTitle('GEN muon p_{T}')
    #     h_pt_trg[key].GetYaxis().SetTitle('Events')
    # for key in h_dPt.keys():
    #     h_dPt[key].SetLineWidth(2)
    #     h_dPt[key].GetXaxis().SetTitle('log_{2}(track p_{T}/GEN p_{T}')
    #     h_dPt[key].Scale( 100.0 / max(h_dPt[key].Integral(), 1.0) )
    #     h_dPt[key].GetYaxis().SetTitle('% of events')


    for iDet in ['CSC', 'RPC']:
        for iPt in pt_cuts.keys():
            
            h_eta['pt_%s_%s' % (iPt, iDet)].SetLineWidth(2)
            h_eta['pt_%s_%s' % (iPt, iDet)].SetLineColor(kBlack)
            h_eta['pt_%s_%s' % (iPt, iDet)].Write()
            h_phi['pt_%s_%s' % (iPt, iDet)].SetLineWidth(2)
            h_phi['pt_%s_%s' % (iPt, iDet)].SetLineColor(kBlack)
            h_phi['pt_%s_%s' % (iPt, iDet)].Write()

            for iSt in st_cuts.keys():
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kBlue)
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kBlue)
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()
                h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kBlack)
                h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kBlue)
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()
                h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kBlack)
                h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].SetLineColor(kRed)
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Write()

                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Divide( h_eta['pt_%s_%s' % (iPt, iDet)] )
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetName ( 'h_eta_pt_%s_%s_hit_%s_eff' % (iPt, iDet, iSt) )
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetYaxis().SetTitle('Efficiency')
                h_eta_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()

                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Divide( h_th_hit_Fd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] )
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetName ( 'h_theta_pt_%s_%s_hit_%s_F_eff' % (iPt, iDet, iSt) )
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetYaxis().SetTitle('Efficiency')
                h_th_hit_Fn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()

                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Divide( h_th_hit_Rd['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)] )
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetName ( 'h_theta_pt_%s_%s_hit_%s_R_eff' % (iPt, iDet, iSt) )
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetYaxis().SetTitle('Efficiency')
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kRed)
                h_th_hit_Rn['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()

                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Divide( h_eta['pt_%s_%s' % (iPt, iDet)] )
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].SetName ( 'h_eta_pt_%s_%s_trk_%s_eff' % (iPt, iDet, iSt) )
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].GetYaxis().SetTitle('Efficiency')
                h_eta_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Write()

                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetLineColor(kBlue)
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].SetLineWidth(2)
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].SetLineColor(kRed)
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Write()

                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Divide( h_phi['pt_%s_%s' % (iPt, iDet)] )
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].SetName ( 'h_phi_pt_%s_%s_hit_%s_eff' % (iPt, iDet, iSt) )
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].GetYaxis().SetTitle('Efficiency')
                h_phi_hit['pt_%s_%s_hit_%s' % (iPt, iDet, iSt)].Write()

                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Divide( h_phi['pt_%s_%s' % (iPt, iDet)] )
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].SetName ( 'h_phi_pt_%s_%s_trk_%s_eff' % (iPt, iDet, iSt) )
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].GetYaxis().SetTitle('Efficiency')
                h_phi_trk['pt_%s_%s_trk_%s' % (iPt, iDet, iSt)].Write()


    del out_file
    
    print 'Exiting MuGun_hit_matching.py'


if __name__ == '__main__':
    main()

