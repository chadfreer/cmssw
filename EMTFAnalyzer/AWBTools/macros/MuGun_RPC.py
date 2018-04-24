#! /usr/bin/env python

import sys
import math
from ROOT import *
import numpy as np
from array import *
# from eff_modules import *

def main():

###################
## Initialize files
###################
    
    # file_name_1 = '../NTupleMaker/EMTF_MC_NTuple_SingleMu_noRPC_200k.root'
    # file_name_2 = '../NTupleMaker/EMTF_MC_NTuple_SingleMu_RPC_200k.root'
    file_name_1 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_noRPC_300k.root'
    file_name_2 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_RPC_300k.root'

    file_1 = TFile.Open(file_name_1)
    file_2 = TFile.Open(file_name_2)
    
    tree_1 = file_1.Get('ntuple/tree')
    tree_2 = file_2.Get('ntuple/tree')
    
    # out_file = TFile('plots/MuGun_RPC.root', 'recreate')
    out_file = TFile('plots/MuGun_RPC_SingleMu_eff.root', 'recreate')
    
#################
## Selection cuts
#################

    eta_cuts = {}
    eta_cuts['all']       = [1.20, 2.40, '1.2 < |#eta| < 2.4']
    # eta_cuts['1p2_1p85']  = [1.20, 1.85, '1.2 < |#eta| < 1.85']
    # eta_cuts['1p85_2p4']  = [1.85, 2.40, '1.85 < |#eta| < 2.4']
    # eta_cuts['1p2_1p55']  = [1.20, 1.55, '1.2 < |#eta| < 1.55']
    # eta_cuts['1p55_1p85'] = [1.55, 1.85, '1.55 < |#eta| < 1.85']
    # eta_cuts['1p85_2p1']  = [1.85, 2.10, '1.85 < |#eta| < 2.1']
    # eta_cuts['2p1_2p4']   = [2.10, 2.40, '2.1 < |#eta| < 2.4']
    
    pt_cuts = {}
    # pt_cuts['all']      = [  0, 1000]
    # pt_cuts['10_up']  = [ 10, 1000, 'p_{T} > 10 GeV']
    # pt_cuts['1_5']      = [  0,    5, '1 < p_{T} < 5 GeV']
    # pt_cuts['5_15']     = [  5,   15, '5 < p_{T} < 15 GeV']
    # pt_cuts['15_40']    = [ 15,   40, '15 < p_{T} < 40 GeV']
    # pt_cuts['40_100']   = [ 40,  100]
    # pt_cuts['100_250']  = [100,  250]
    # pt_cuts['250_up']   = [250, 1000]  
    pt_cuts['10_200']     = [ 10,  200, '10 < p_{T} < 200 GeV']
    
    qual_cuts = {}
    # qual_cuts['MuOpen']       = [[3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15], 'MuOpen tracks']
    # qual_cuts['DoubleMu']     = [[7, 10, 11, 12, 13, 14, 15], 'DoubleMu tracks']
    qual_cuts['SingleMu']     = [[11, 13, 14, 15], 'SingleMu tracks']
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
    qual_cuts['mode_15']      = [[15], '4-station tracks']

    st_cuts = {}
    st_cuts['any'] = [[], 'RPC in #geq1 station'] 
    st_cuts['St1'] = [[1], 'RPC in station 1']
    st_cuts['St2'] = [[2], 'RPC in station 2']
    st_cuts['St3'] = [[3], 'RPC in station 3']
    st_cuts['St4'] = [[4], 'RPC in station 4']
    
#############
## Histograms
#############
    
    pt_bins_temp = [0, 2, 3.5, 5, 8, 12, 17, 22, 30, 50, 100, 250, 500, 1000]
    pt_bins  = array('f', pt_bins_temp)
    max_pt = pt_bins_temp[len(pt_bins_temp) - 1] - 0.01
    
    # eta_bins = [75, 1.0, 2.5]
    eta_bins = [30, 1.0, 2.5]

    dPt_bins = [60, -3.0, 3.0]
    
    h_eta     = {}
    h_eta_trg = {}
    h_pt      = {}
    h_pt_trg  = {}
    h_dPt     = {}

    for iDet in ['noRPC', 'RPC']:
        if iDet == 'noRPC': det_str = 'no RPC'
        if iDet == 'RPC'  : det_str = 'with RPC'

        for iQual in qual_cuts.keys():
            qual_str = qual_cuts[iQual][1]

            for iPt in pt_cuts.keys():
                pt_str = pt_cuts[iPt][2]

                h_eta    ['%s_pt_%s_%s' % (iQual, iPt, iDet)] = TH1D('h_eta_%s_pt_%s_%s'    % (iQual, iPt, iDet), 
                                                                  'GEN muon |#eta|, %s, %s' % (qual_str, pt_str),
                                                                  eta_bins[0], eta_bins[1], eta_bins[2])
                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)] = TH1D('h_eta_trg_%s_pt_%s_%s' % (iQual, iPt, iDet), 
                                                                  'h_eta_trg_%s_pt_%s_%s'    % (iQual, iPt, iDet),
                                                                  eta_bins[0], eta_bins[1], eta_bins[2])
                h_eta    ['%s_pt_%s_%s' % (iQual, iPt, iDet)].Sumw2()
                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].Sumw2()
                
            for iEta in eta_cuts.keys():
                h_pt    ['%s_eta_%s_%s' % (iQual, iEta, iDet)] = TH1D('h_pt_%s_eta_%s_%s' % (iQual, iEta, iDet),
                                                                   'h_pt_%s_eta_%s_%s'    % (iQual, iEta, iDet),
                                                                   len(pt_bins) - 1, pt_bins)
                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)] = TH1D('h_pt_trg_%s_eta_%s_%s' % (iQual, iEta, iDet),
                                                                   'h_pt_trg_%s_eta_%s_%s'    % (iQual, iEta, iDet),
                                                                   len(pt_bins) - 1, pt_bins)
                h_pt    ['%s_eta_%s_%s' % (iQual, iEta, iDet)].Sumw2()
                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].Sumw2()

    for iDet in ['noRPC', 'RPC']:
        if iDet == 'noRPC': det_str = 'no RPC'
        if iDet == 'RPC'  : det_str = 'with RPC'

        for iPt in pt_cuts.keys():
            pt_str = pt_cuts[iPt][2]
        
            for iEta in eta_cuts.keys():
                eta_str = eta_cuts[iEta][2]

                for iQual in qual_cuts.keys():
                    qual_str = qual_cuts[iQual][1]

                    h_dPt['%s_pt_%s_eta_%s_%s' % (iQual, iPt, iEta, iDet)] = TH1D('h_dPt_%s_pt_%s_eta_%s_%s' % (iQual, iPt, iEta, iDet),
                                                                                  'log_{2}(track p_{T}/GEN p_{T}), %s, %s, %s, %s' % (pt_str, eta_str, qual_str, det_str),
                                                                                  dPt_bins[0], dPt_bins[1], dPt_bins[2])
                    h_dPt['%s_pt_%s_eta_%s_%s' % (iQual, iPt, iEta, iDet)].Sumw2()
                    
                for iSt in st_cuts.keys():
                    if iDet != 'RPC': continue
                    st_str = st_cuts[iSt][1]
                    qual_str = qual_cuts['mode_15'][1]
                    
                    h_dPt['mode_15_pt_%s_eta_%s_RPC_%s' % (iPt, iEta, iSt)] = TH1D('h_dPt_mode_15_pt_%s_eta_%s_RPC_%s' % (iPt, iEta, iSt),
                                                                                   'log_{2}(track p_{T}/GEN p_{T}), %s, %s, %s, %s' % (pt_str, eta_str, qual_str, st_str),
                                                                                   dPt_bins[0], dPt_bins[1], dPt_bins[2])
                    h_dPt['mode_15_pt_%s_eta_%s_RPC_%s' % (iPt, iEta, iSt)].Sumw2()
            
#############
## Event loop
#############
                
    for iDet in ['noRPC', 'RPC']:
        if iDet == 'noRPC':
            tree = tree_1
        if iDet == 'RPC':
            tree = tree_2
        
        for iEvt in range(tree.GetEntries()):
            
            # if iEvt > 10000: break
            if iEvt % 1000 is 0: print 'Event #', iEvt

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
                mu_pt  = muons.GetLeaf('pt').GetValue(iMu)
                mu_eta = muons.GetLeaf('eta').GetValue(iMu)

                for iQual in qual_cuts.keys():

                    for iPt in pt_cuts.keys():
                        if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue

                        pass_trg = False
                        for iTrk in range(nTrks):
                            trk_pt   = trks.GetLeaf('pt').GetValue(iTrk)
                            trk_eta  = trks.GetLeaf('eta').GetValue(iTrk)
                            trk_mode = int(trks.GetLeaf('mode').GetValue(iTrk))

                            if (trk_eta > 0) != (mu_eta > 0):    continue
                            if not trk_mode in qual_cuts[iQual][0]: continue
                            pass_trg = True
                            break

                        h_eta['%s_pt_%s_%s' % (iQual, iPt, iDet)].Fill( abs(mu_eta) )
                        if pass_trg:
                            h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].Fill( abs(mu_eta) )

                    for iEta in eta_cuts.keys():
                        if (abs(mu_eta) < eta_cuts[iEta][0]) or (abs(mu_eta) > eta_cuts[iEta][1]): continue

                        pass_trg = False
                        for iTrk in range(nTrks):
                            trk_pt   = trks.GetLeaf('pt').GetValue(iTrk)
                            trk_eta  = trks.GetLeaf('eta').GetValue(iTrk)
                            trk_mode = int(trks.GetLeaf('mode').GetValue(iTrk))

                            if (trk_eta > 0) != (mu_eta > 0):   continue
                            if not trk_mode in qual_cuts[iQual][0]: continue
                            pass_trg = True
                            break

                        h_pt['%s_eta_%s_%s' % (iQual, iEta, iDet)].Fill( mu_pt )
                        if pass_trg:
                            h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].Fill( mu_pt )
                    

                for iPt in pt_cuts.keys():
                    if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue

                    for iEta in eta_cuts.keys():
                        if (abs(mu_eta) < eta_cuts[iEta][0]) or (abs(mu_eta) > eta_cuts[iEta][1]): continue

                        for iTrk in range(nTrks):
                            trk_nRPC = trks.GetLeaf('nRPC').GetValue(iTrk)
                            trk_pt   = trks.GetLeaf('pt').GetValue(iTrk)
                            trk_eta  = trks.GetLeaf('eta').GetValue(iTrk)
                            trk_mode = int(trks.GetLeaf('mode').GetValue(iTrk))
                            if (trk_eta > 0) != (mu_eta > 0): continue

                            for iQual in qual_cuts.keys():
                                if not trk_mode in qual_cuts[iQual][0]: continue
                                fill_dPt = max( min( math.log(trk_pt/mu_pt, 2), dPt_bins[2] - 0.01), dPt_bins[1] + 0.01)
                                h_dPt['%s_pt_%s_eta_%s_%s' % (iQual, iPt, iEta, iDet)].Fill( fill_dPt )

                            for iSt in st_cuts.keys():
                                if iDet != 'RPC':  continue
                                if trk_nRPC < 1:   continue
                                if trk_mode != 15: continue
                                has_RPC = True
                                for jSt in st_cuts[iSt][0]:
                                    if trks.GetLeaf('hit_isRPC').GetValue(iTrk*4 + (jSt - 1)) != 1:
                                        has_RPC = False

                                if not has_RPC: continue
                                fill_dPt = max( min( math.log(trk_pt/mu_pt, 2), dPt_bins[2] - 0.01), dPt_bins[1] + 0.01)
                                h_dPt['mode_15_pt_%s_eta_%s_RPC_%s' % (iPt, iEta, iSt)].Fill( fill_dPt )


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

    for key in h_eta.keys():
        h_eta[key].SetLineWidth(2)
        h_eta[key].GetXaxis().SetTitle('GEN muon |#eta|')
        h_eta[key].GetYaxis().SetTitle('Events')
    for key in h_eta_trg.keys():
        h_eta_trg[key].SetLineWidth(2)
        h_eta_trg[key].GetXaxis().SetTitle('GEN muon |#eta|')
        h_eta_trg[key].GetYaxis().SetTitle('Events')
    for key in h_pt.keys():
        h_pt[key].SetLineWidth(2)
        h_pt[key].GetXaxis().SetTitle('GEN muon p_{T}')
        h_pt[key].GetYaxis().SetTitle('Events')
    for key in h_pt_trg.keys():
        h_pt_trg[key].SetLineWidth(2)
        h_pt_trg[key].GetXaxis().SetTitle('GEN muon p_{T}')
        h_pt_trg[key].GetYaxis().SetTitle('Events')
    for key in h_dPt.keys():
        h_dPt[key].SetLineWidth(2)
        h_dPt[key].GetXaxis().SetTitle('log_{2}(track p_{T}/GEN p_{T}')
        h_dPt[key].Scale( 100.0 / max(h_dPt[key].Integral(), 1.0) )
        h_dPt[key].GetYaxis().SetTitle('% of events')

    for iDet in ['noRPC', 'RPC']:
        for iQual in qual_cuts.keys():
            
            for iPt in pt_cuts.keys():
                h_eta    ['%s_pt_%s_%s' % (iQual, iPt, iDet)].Write()
                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].Write()

                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].Divide( h_eta['%s_pt_%s_%s' % (iQual, iPt, iDet)] )
                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].SetName ( 'h_eta_eff_%s_pt_%s_%s' % (iQual, iPt, iDet) )
                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].SetTitle( 'h_eta_eff_%s_pt_%s_%s' % (iQual, iPt, iDet) )
                h_eta_trg['%s_pt_%s_%s' % (iQual, iPt, iDet)].Write()
                
            for iEta in eta_cuts.keys():
                h_pt    ['%s_eta_%s_%s' % (iQual, iEta, iDet)].Write()
                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].Write()

                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].Divide( h_pt['%s_eta_%s_%s' % (iQual, iEta, iDet)] )
                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].SetName ( 'h_pt_eff_%s_eta_%s_%s' % (iQual, iEta, iDet) )
                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].SetTitle( 'h_pt_eff_%s_eta_%s_%s' % (iQual, iEta, iDet) )
                h_pt_trg['%s_eta_%s_%s' % (iQual, iEta, iDet)].Write()

    for iDet in ['noRPC', 'RPC']:
        for iPt in pt_cuts.keys():
            for iEta in eta_cuts.keys():
                for iQual in qual_cuts.keys():
                    h_dPt['%s_pt_%s_eta_%s_%s' % (iQual, iPt, iEta, iDet)].Write()
                for iSt in st_cuts.keys():
                    if iDet != 'RPC': continue
                    h_dPt['mode_15_pt_%s_eta_%s_RPC_%s' % (iPt, iEta, iSt)].Write()

            
    del out_file


if __name__ == '__main__':
    main()

