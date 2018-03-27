#! /usr/bin/env python

import sys
import math
from ROOT import *
import numpy as np
from array import *
# from eff_modules import *

MAX_EVT =  2000000
PRT_EVT =    10000

def main():

###################
## Initialize files
###################

    # file_name_1 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_noRPC_300k.root'
    # file_name_2 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_RPC_300k.root'

    # file_1 = TFile.Open(file_name_1)
    # file_2 = TFile.Open(file_name_2)
    
    # tree_1 = file_1.Get('ntuple/tree')
    # tree_2 = file_2.Get('ntuple/tree')
    
    file_names_1 = []
    store = 'root://eoscms.cern.ch//store/user/abrinke1/EMTF/Emulator/ntuples/'
    in_dir = 'SingleMu_Pt1To1000_FlatRandomOneOverPt/EMTF_MuGun/170113_165434/0000/'
    for i in range(1,99):
        file_names_1.append(store+in_dir+'EMTF_MC_NTuple_SingleMu_noRPC_%d.root' % i)
        print 'Opening file: '+store+in_dir+'EMTF_MC_NTuple_SingleMu_noRPC_%d.root' % i
        if (i*100000 > MAX_EVT): break  ## ~100k events per file
    file_names_2 = ['/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/EMTF_MC_NTuple_SingleMu_RPC_300k.root']
        
    chains_1 = []
    for i in range(len(file_names_1)):
        chains_1.append( TChain('ntuple/tree') )
        chains_1[i].Add( file_names_1[i] )
        
    chains_2 = []
    for i in range(len(file_names_2)):
        chains_2.append( TChain('ntuple/tree') )
        chains_2[i].Add( file_names_2[i] )

    out_file = TFile('plots/MuGun_propagation_lin.root', 'recreate')
    
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
    for j in range(12):
        eta_str = '%dp%s_%sp%s' % ( ((12+j) - ((12+j) % 10)) / 10, ((12+j) % 10), ((13+j) - ((13+j) % 10)) / 10, ((13+j) % 10) )
        eta_cuts[eta_str]   = [1.2+(j*0.1), 1.2+((j+1)*0.1), eta_str]
    
    pt_cuts = {}
    # pt_cuts['all']      = [  0, 1000, '1 < p_{T} < 1000 GeV']
    pt_cuts['5_200']    = [  5,  200, '5 < p_{T} < 200 GeV']
    # pt_cuts['10_up']  = [ 10, 1000, 'p_{T} > 10 GeV']
    # pt_cuts['1_5']      = [  0,    5, '1 < p_{T} < 5 GeV']
    # pt_cuts['5_15']     = [  5,   15, '5 < p_{T} < 15 GeV']
    # pt_cuts['15_40']    = [ 15,   40, '15 < p_{T} < 40 GeV']
    # pt_cuts['40_100']   = [ 40,  100]
    # pt_cuts['100_250']  = [100,  250]
    # pt_cuts['250_up']   = [250, 1000]  
    # pt_cuts['20_200']   = [  20,   200, '20 < p_{T} < 200 GeV']
    # pt_cuts['100_up']   = [ 100,  1000, '100 < p_{T} < 1000 GeV']
    
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
    # qual_cuts['mode_15']      = [[15], '4-station tracks']

    # st_cuts = {}
    # st_cuts['St1'] = [[1], 'Station 1']
    # st_cuts['St2'] = [[2], 'Station 2']
    # st_cuts['St3'] = [[3], 'Station 3']
    # st_cuts['St4'] = [[4], 'Station 4']
    
#############
## Histograms
#############
    
    # dPhi_bins = [120, -50, 10]
    # curv_bins = [30, 0, 3]
    
    dPhi_bins = []
    for i in range(301):
        dPhi_bins.append(-55. + i*0.2)
    dPhi_bins = array('d', dPhi_bins)

    curv_bins = [0, 1./500, 1./300, 1./200, 1./150, 1./120, 1./100, 1./80, 1./70, 1./60, 1./50, 1./40, 1./35, 1./30, 1./25, 1./20,
                 1./18, 1./16, 1./14, 1./12, 1./10, 1./9, 1./8, 1./7, 1./6, 1./5, 1./4.5, 1./4, 1./3.5, 1./3, 1./2.5, 1./2, 1./1.5, 1./1]
    curv_bins = array('d', curv_bins)

    dPred_bins = []
    for i in range(101):
        dPred_bins.append(-5. + i*0.1)
    dPred_bins = array('d', dPred_bins)

    h_dPhi_vs_curv = {}
    p_dPhi_vs_curv = {}
    f_dPhi_vs_curv = {}
    h_dPred_vs_curv = {}

    # for iDet in ['CSC', 'RPC']:
    for iDet in ['CSC']:
        if iDet == 'CSC': det_str = 'CSC LCT'
        if iDet == 'RPC': det_str = 'RPC hit'

        for iPt in pt_cuts.keys():
            pt_str = pt_cuts[iPt][2]
            
            for iEta in eta_cuts.keys():
                eta_str = eta_cuts[iEta][2]
            
                for iQual in qual_cuts.keys():
                    qual_str = qual_cuts[iQual][1]

                    h_str = 'pt_%s_eta_%s_%s_%s' % (iPt, iEta, iQual, iDet)

                    h_dPhi_vs_curv[h_str] = TH2D( 'h_dPhi_vs_curv_%s' % h_str, '',
                                                  # curv_bins[0], curv_bins[1], curv_bins[2],
                                                  # dPhi_bins[0], dPhi_bins[1], dPhi_bins[2] )
                                                  len(curv_bins) - 1, curv_bins,
                                                  len(dPhi_bins) - 1, dPhi_bins )

                    p_dPhi_vs_curv[h_str] = TProfile( 'p_dPhi_vs_curv_%s' % h_str, '',
                                                      # curv_bins[0], curv_bins[1], curv_bins[2],
                                                      len(curv_bins) - 1, curv_bins )

                    h_dPred_vs_curv[h_str] = TH2D( 'h_dPred_vs_curv_%s' % h_str, '',
                                                  # curv_bins[0], curv_bins[1], curv_bins[2],
                                                  # dPred_bins[0], dPred_bins[1], dPred_bins[2] )
                                                  len(curv_bins) - 1, curv_bins,
                                                  len(dPred_bins) - 1, dPred_bins )

                    
#############
## Event loop
#############
                
    # for iDet in ['CSC', 'RPC']:
    for iDet in ['CSC']:
        if iDet == 'CSC':
            # tree = tree_1
            chains = chains_1
        if iDet == 'RPC':
            # tree = tree_2
            chains = chains_2

        iEvt = -1
        for chain in chains:
        
            muons = chain.GetBranch('muon')
            trks  = chain.GetBranch('track')
            hits  = chain.GetBranch('hit')
                
            for jEvt in range(chain.GetEntries()):
                iEvt += 1
            
                if iEvt > MAX_EVT: break
                if iEvt % PRT_EVT is 0: print 'Event #', iEvt

                chain.GetEntry(jEvt)
                
                nMuons = int(muons.GetLeaf('nMuons').GetValue())
                nTrks  = int(trks.GetLeaf('nTracks').GetValue())
                nHits  = int(hits.GetLeaf('nHits').GetValue())
                
                mu1_eta = muons.GetLeaf('eta').GetValue(0)
                if abs(mu1_eta) < 1.0: continue
                
                for iMu in range(nMuons):
                    mu_pt     = muons.GetLeaf('pt').GetValue(iMu)
                    mu_eta    = muons.GetLeaf('eta').GetValue(iMu)
                    mu_phi    = muons.GetLeaf('phi').GetValue(iMu)
                    mu_charge = int(muons.GetLeaf('charge').GetValue(iMu))
                    mu_theta  = 2*math.atan(math.exp(-1*abs(mu_eta))) * (180/3.14159)

                    for iPt in pt_cuts.keys():
                        if (mu_pt < pt_cuts[iPt][0]) or (mu_pt > pt_cuts[iPt][1]): continue

                        for iEta in eta_cuts.keys():
                            if (abs(mu_eta) < eta_cuts[iEta][0]) or (abs(mu_eta) > eta_cuts[iEta][1]): continue

                            for iTrk in range(nTrks):
                                trk_pt   = trks.GetLeaf('pt').GetValue(iTrk)
                                trk_eta  = trks.GetLeaf('eta').GetValue(iTrk)
                                trk_phi  = trks.GetLeaf('phi').GetValue(iTrk)
                                trk_mode = int(trks.GetLeaf('mode').GetValue(iTrk))
                                
                                if ((trk_eta > 0) != (mu_eta > 0)): continue
                                
                                for iQual in qual_cuts.keys():
                                    if not trk_mode in qual_cuts[iQual][0]: continue

                                    dPhi0 = (math.radians(trk_phi) - math.radians(mu_phi))*mu_charge
                                    dPhi = math.acos( math.cos( dPhi0 ) )
                                    dPhi *= ( math.sin(dPhi0) / abs(math.sin(dPhi0)) )
                                    
                                    dPhi = math.degrees(dPhi)

                                    h_str = 'pt_%s_eta_%s_%s_%s' % (iPt, iEta, iQual, iDet)
                                    # h_dPhi_vs_curv[h_str].Fill( math.log10(mu_pt), dPhi )
                                    h_dPhi_vs_curv[h_str].Fill( 1./mu_pt, dPhi )

                                    pred_dPhi = (1./mu_pt) * (10.23 - 5.1155*mu_theta + 0.02259*mu_theta*mu_theta)
                                    h_dPred_vs_curv[h_str].Fill( 1./mu_pt, pred_dPhi - dPhi )
                                
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
    par_vs_eta = []

    # for iDet in ['CSC', 'RPC']:
    for iDet in ['CSC']:
        for iPt in pt_cuts.keys():
            
            pt_str = pt_cuts[iPt][2]
            
            for iEta in eta_cuts.keys():
                eta_str = eta_cuts[iEta][2]
            
                for iQual in qual_cuts.keys():
                    qual_str = qual_cuts[iQual][1]
                    
                    h_str = 'pt_%s_eta_%s_%s_%s' % (iPt, iEta, iQual, iDet)

                    h_dPhi_vs_curv[h_str].Write()
                    h_dPred_vs_curv[h_str].Write()

                    p_dPhi_vs_curv[h_str] = h_dPhi_vs_curv[h_str].ProfileX()
                    p_dPhi_vs_curv[h_str].SetName('p_dPhi_vs_curv_%s' % h_str)
                    p_dPhi_vs_curv[h_str].Write()

                    f_dPhi_vs_curv[h_str] = TF1( 'f_dPhi_vs_curv_%s' % h_str, 'pol1' )
                    # f_dPhi_vs_curv[h_str] = TF1( 'f_dPhi_vs_curv_%s' % h_str, 'pol2' )
                    f_dPhi_vs_curv[h_str].SetParameter(0, 0)
                    f_dPhi_vs_curv[h_str].FixParameter(0, 0)
                    f_dPhi_vs_curv[h_str].SetParameter(1, -60.)
                    # f_dPhi_vs_curv[h_str].SetParameter(2, 0)
                    p_dPhi_vs_curv[h_str].Fit( 'f_dPhi_vs_curv_%s' % h_str )

                    if iEta == 'all': continue
                    avg_eta   = (eta_cuts[iEta][0] + eta_cuts[iEta][1]) / 2
                    avg_theta = 2*math.atan(math.exp(-1*avg_eta)) * (180/3.14159)
                    
                    par_vs_eta.append( [ avg_eta, avg_theta,
                                         f_dPhi_vs_curv[h_str].GetParameter(0), 
                                         f_dPhi_vs_curv[h_str].GetParameter(1) ] )
                                         # f_dPhi_vs_curv[h_str].GetParameter(2) ] )

    print '\n*****************************************'
    print '*******   Fit parameter vs. eta   *******'
    print '*****************************************'
    print 'Eta    theta  interecept  slope  curve  dSlope  dSlope/dTheta'
    prev_slope = 0
    prev_theta = 999
    slopes = []
    thetas = []
    dSlopes = []
    dThetas = []
    for iPar in sorted(par_vs_eta):
        print '%.3f    %.2f    %.3f    %.2f   %.3f   %.3f' % ( iPar[0], iPar[1], iPar[2], iPar[3], iPar[3] - prev_slope, (iPar[3] - prev_slope)/(prev_theta-iPar[1]) )
        slopes.append(iPar[3])
        thetas.append(iPar[1])
        if len(slopes) > 1:
            dSlopes.append( (iPar[3] - prev_slope) / (prev_theta-iPar[1]) )
            dThetas.append(iPar[1])
        prev_slope = iPar[3]
        prev_theta = iPar[1]

    g_slope_vs_theta = TGraph( len(thetas), array('d', thetas), array('d', slopes) )
    g_slope_vs_theta.SetName('g_slope_vs_theta')
    g_slope_vs_theta.Write()

    g_dSlope_vs_theta = TGraph( len(dThetas), array('d', dThetas), array('d', dSlopes) )
    g_dSlope_vs_theta.SetName('g_dSlope_vs_theta')
    g_dSlope_vs_theta.Write()

    del out_file


if __name__ == '__main__':
    main()

