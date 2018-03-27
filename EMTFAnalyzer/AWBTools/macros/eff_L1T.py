#! /usr/bin/env python

########################################################
## eff_L1T.py   
## A script to find L1T efficiency from L1Ntuples
## By David Curry
##
########################################################

print '------> Setting Environment'

import sys
import math
import subprocess
from ROOT import *
import numpy as np
from array import *
from eff_modules import *

print '------> Importing Root File'

## Configuration settings
USE_EMUL = False
MAX_EVT  = 10000000
REP_EVT  = 10000

REQ_BX0     = True
REQ_uGMT    = True
REQ_L1_dEta = True
REQ_HLT     = True
TAG_ISO = 0.1
TAG_PT  = 26
PRB_PT  = 16
TRG_PT  = 12


## L1NTuple branches
evt_tree  = TChain('l1EventTree/L1EventTree')
reco_tree = TChain('l1MuonRecoTree/Muon2RecoTree')
if not USE_EMUL:
    L1_tree = TChain('l1UpgradeTree/L1UpgradeTree')
    tf_tree = TChain('l1UpgradeTfMuonTree/L1UpgradeTfMuonTree')
else:
    L1_tree = TChain('l1UpgradeEmuTree/L1UpgradeTree')
    tf_tree = TChain('l1UpgradeTfMuonEmuTree/L1UpgradeTfMuonTree')

## Input file names
eos_cmd = '/afs/cern.ch/project/eos/installation/pro/bin/eos.select'
prefix = 'root://eoscms//eos/cms'

# dir1 = '/store/group/dpg_trigger/comm_trigger/L1Trigger/safarzad/2017/Collision2017-wRECO-l1t-integration-v96p2_updatedHFSF/'
# dir2 = 'SingleMuon/crab_Collision2017-wRECO-l1t-integration-v96p2_updatedHFSF__SingleMuon/170628_124037/0001/'
# run_str = '_297606'

dir1 = '/store/user/treis/data/i96p0/SingleMuon/crab_20170622_184540/170622_164616/0000/'
dir2 = ''
run_str = '_2017B'


## Load input files
print prefix+dir1+dir2
for in_file_name in subprocess.check_output([eos_cmd, 'ls', prefix+dir1+dir2]).splitlines():
    if not '.root' in in_file_name: continue
    file_name = '%s%s%s%s' % (prefix, dir1, dir2, in_file_name)
    # print 'Loading file %s' % in_file_name
    evt_tree.Add(file_name)
    reco_tree.Add(file_name)
    L1_tree.Add(file_name)
    tf_tree.Add(file_name)


## Trigger settings
trig_WP = {}
trig_WP['SingleMu']  = [12, 13, 14, 15]
trig_WP['SingleMu7'] = [11, 12, 13, 14, 15]
trig_WP['DoubleMu']  = [8, 9, 10, 11, 12, 13, 14, 15]
trig_WP['MuOpen']    = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

trig_TF = {}
trig_TF['uGMT'] = [0.00, 2.40]
trig_TF['BMTF'] = [0.00, 0.83]
trig_TF['OMTF'] = [0.83, 1.24]
trig_TF['EMTF'] = [1.24, 2.40]


## Choose level of probe matching

## L1Upgrade__tfMuon.tfMuon.Bx == 0
if REQ_BX0: BX0_str = '_BX0'
else: BX0_str = ''

## L1Upgrade__tfMuon matches L1Upgrade.muon (Bx, HwQual <--> Qual, HwEta <--> lEta, HwPt <--> lEt) 
if REQ_uGMT: uGMT_str = '_uGMT'
else: uGMT_str = ''

## abs( (L1Upgrade__tfMuon.tfMuonHwEta*0.010875) - Muon.eta ) < 0.2
if REQ_L1_dEta: dEta_str = '_dEta'
else: dEta_str = ''

## Muon.hlt_isomu == 1 && Muon.hlt_isoDeltaR < 0.1 for probe.  And Muon.iso < 0.1 && Muon.pt < TAG_PT in denom.
if REQ_HLT: HLT_str = '_HLT'
else: HLT_str = ''

## Histogram filename
out_file = TFile('plots/L1T_eff_Pt%d%s%s%s%s%s_sectM6.root' % (TRG_PT, run_str, dEta_str, BX0_str, uGMT_str, HLT_str), 'recreate')


## ================ Histograms ======================
scale_pt_temp = [0, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 25, 30, 35, 45, 60, 75, 100, 140, 150]
scale_pt  = array('f', scale_pt_temp)
max_pt = scale_pt_temp[len(scale_pt_temp) - 1] - 0.01

eta_bins = [100, -2.5, 2.5]
phi_bins = [72, -180, 180]

h_pt  = {}
h_eta = {}
h_phi = {}
h_pt_trg  = {}
h_eta_trg = {}
h_phi_trg = {}
for TF in trig_TF.keys():
    h_pt [TF] = TH1D('h_pt_%s' % TF,  '', len(scale_pt_temp)-1,  scale_pt)
    h_eta[TF] = TH1D('h_eta_%s' % TF, '', eta_bins[0], eta_bins[1], eta_bins[2])
    h_phi[TF] = TH1D('h_phi_%s' % TF, '', phi_bins[0], phi_bins[1], phi_bins[2])

    for WP in trig_WP.keys():
        key = '%s_%s' % (TF, WP)
        h_pt_trg [key] = TH1D('h_pt_%s' % key,  '', len(scale_pt_temp)-1,  scale_pt)
        h_eta_trg[key] = TH1D('h_eta_%s' % key, '', eta_bins[0], eta_bins[1], eta_bins[2])
        h_phi_trg[key] = TH1D('h_phi_%s' % key, '', phi_bins[0], phi_bins[1], phi_bins[2])


## ================================================

# Loop over over events in TFile
for iEvt in range(evt_tree.GetEntries()):
    if iEvt > MAX_EVT: break
    if iEvt % REP_EVT is 0: print 'Event #', iEvt
    
    evt_tree.GetEntry(iEvt)
    # if not (evt_tree.Event.run == 273725 or evt_tree.Event.run == 273730):
    #     continue
    L1_tree.GetEntry(iEvt)
    tf_tree.GetEntry(iEvt)
    reco_tree.GetEntry(iEvt)

    uGMT_tree = L1_tree.L1Upgrade
    bmtf_tree = tf_tree.L1UpgradeBmtfMuon
    omtf_tree = tf_tree.L1UpgradeOmtfMuon
    emtf_tree = tf_tree.L1UpgradeEmtfMuon

    if reco_tree.Muon.nMuons < 2: continue

    ## === Look for a tag muon ===
    isTag, isProbe = False, False
    isBMTFtag, isOMTFtagIn, isOMTFtagOut, isEMTFtag = False, False, False, False
    isBMTFprobe, isOMTFprobeIn, isOMTFprobeOut, isEMTFprobe = False, False, False, False
    isTrigger_emtf, isTrigger_omtfIn, isTrigger_omtfOut, isTrigger_bmtf = False, False, False, False

    for iTag in range(reco_tree.Muon.nMuons):

        recoAbsEta = abs(reco_tree.Muon.eta[iTag])
        recoIsMed = np.array([-99], dtype=np.bool)
        recoIsMed = reco_tree.Muon.isMediumMuon[iTag]
        
        if REQ_HLT and reco_tree.Muon.hlt_isomu[iTag] != 1: continue
        if REQ_HLT and reco_tree.Muon.hlt_isoDeltaR[iTag] > 0.1: continue
        if not recoIsMed: continue
        if reco_tree.Muon.pt[iTag] < TAG_PT: continue
        if reco_tree.Muon.iso[iTag] > TAG_ISO: continue

        if recoAbsEta > 1.0: 
            
            ## Did the tag trigger
            for iTrk in range(emtf_tree.nTfMuons):
                if not emtf_tree.tfMuonHwQual[iTrk] in trig_WP['SingleMu']: continue
                if (emtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TAG_PT - 5.01: continue
                isBMTFtag = True
                bmtf_iTag = iTag
                
        if recoAbsEta < 1.0: 
            
            for iTrk in range(bmtf_tree.nTfMuons):
                if not bmtf_tree.tfMuonHwQual[iTrk] in trig_WP['SingleMu']: continue
                if (bmtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TAG_PT - 5.01: continue
                isEMTFtag = True
                emtf_iTag = iTag
                
        if recoAbsEta > 1.4: 
            
            for iTrk in range(emtf_tree.nTfMuons):
                if not emtf_tree.tfMuonHwQual[iTrk] in trig_WP['SingleMu']: continue
                if (emtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TAG_PT - 5.01: continue
                isOMTFtagIn = True
                omtfIn_iTag = iTag

        if recoAbsEta < 0.6: 
            
            for iTrk in range(bmtf_tree.nTfMuons):
                if not bmtf_tree.tfMuonHwQual[iTrk] in trig_WP['SingleMu']: continue
                if (bmtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TAG_PT - 5.01: continue
                isOMTFtagOut = True
                omtfOut_iTag = iTag

    for iProbe in range(reco_tree.Muon.nMuons):

        recoEta = reco_tree.Muon.eta[iProbe]
        recoPhi = reco_tree.Muon.phi[iProbe] * 180. / 3.14159
        recoAbsEta = abs(recoEta)
        recoPt = min(reco_tree.Muon.pt[iProbe], max_pt)
        recoIsMed = np.array([-99], dtype=np.bool)
        recoIsMed = reco_tree.Muon.isMediumMuon[iProbe]

        if recoPt < PRB_PT: continue
        if not recoIsMed: continue

## L1Upgrade__tfMuon matches L1Upgrade.muon (Bx, HwQual <--> Qual, HwEta <--> lEta, HwPt <--> lEt) 

        if isBMTFtag and recoAbsEta < trig_TF['BMTF'][1]:
            if isBMTFprobe: continue
            isBMTFprobe = True
            if iProbe == bmtf_iTag: print 'Weird error in isBMTFtag: iTag = %d, iProbe = %d' % (chosen_iTag, iProbe)

            h_pt ['uGMT'].Fill(recoPt)
            h_eta['uGMT'].Fill(recoEta)
            h_phi['uGMT'].Fill(recoPhi)
            h_pt ['BMTF'].Fill(recoPt)
            h_eta['BMTF'].Fill(recoEta)
            h_phi['BMTF'].Fill(recoPhi)
            h_eta['OMTF'].Fill(recoEta)

            for WP in trig_WP.keys():
                isTrigger_bmtf = False
                # If TandP exist look for trigger (fill numerator) 
                for iTrk in range(bmtf_tree.nTfMuons):
                    if not bmtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if (bmtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(bmtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if REQ_BX0 and bmtf_tree.tfMuonBx[iTrk] != 0: continue
                
                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (bmtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and
                            bmtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            bmtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                    h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                    h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                    h_pt_trg['BMTF_%s' % WP].Fill(recoPt)
                    h_eta_trg['BMTF_%s' % WP].Fill(recoEta)
                    h_phi_trg['BMTF_%s' % WP].Fill(recoPhi)
                    isTrigger_bmtf = True
                    break
                
                ## Also check for OMTFIn tracks
                for iTrk in range(omtf_tree.nTfMuons):
                    if not omtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if (omtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(omtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if abs(omtf_tree.tfMuonHwEta[iTrk]*0.010875) > 1.0: continue
                    if REQ_BX0 and omtf_tree.tfMuonBx[iTrk] != 0: continue
                
                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (omtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and 
                            omtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            omtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_eta_trg['OMTF_%s' % WP].Fill(recoEta)

                    if not isTrigger_bmtf: 
                        h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                        h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                        h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                        isTrigger_bmtf = True
                    break


        if isEMTFtag and recoAbsEta > trig_TF['EMTF'][0] and recoAbsEta < trig_TF['EMTF'][1]: 
            if isEMTFprobe: continue
            isEMTFprobe = True
            if iProbe == emtf_iTag: print 'Weird error in isEMTFtag: iTag = %d, iProbe = %d' % (chosen_iTag, iProbe)

            h_pt ['uGMT'].Fill(recoPt)
            h_eta['uGMT'].Fill(recoEta)
            h_phi['uGMT'].Fill(recoPhi)
            h_pt ['EMTF'].Fill(recoPt)
            h_eta['EMTF'].Fill(recoEta)
            h_phi['EMTF'].Fill(recoPhi)
            h_eta['OMTF'].Fill(recoEta)

            for WP in trig_WP.keys():
                isTrigger_emtf = False
                for iTrk in range(emtf_tree.nTfMuons):
                    if not emtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if WP == 'SingleMu7' and emtf_tree.tfMuonHwQual[iTrk] == 11 and emtf_tree.tfMuonLink[iTrk] != 71: continue
                    if (emtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(emtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if REQ_BX0 and emtf_tree.tfMuonBx[iTrk] != 0: continue

                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (emtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and
                            emtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            emtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                    h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                    h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                    h_pt_trg['EMTF_%s' % WP].Fill(recoPt)
                    h_eta_trg['EMTF_%s' % WP].Fill(recoEta)
                    h_phi_trg['EMTF_%s' % WP].Fill(recoPhi)
                    isTrigger_emtf = True
                    break

                ## Also check for OMTFOut tracks
                for iTrk in range(omtf_tree.nTfMuons):
                    if not omtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if (omtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(omtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if abs(omtf_tree.tfMuonHwEta[iTrk]*0.010875) < 1.0: continue
                    if REQ_BX0 and omtf_tree.tfMuonBx[iTrk] != 0: continue

                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (omtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and 
                            omtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            omtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                        if REQ_uGMT and not uGMT_match: continue

                    h_eta_trg['OMTF_%s' % WP].Fill(recoEta)

                    if not isTrigger_emtf:
                        h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                        h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                        h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                        isTrigger_emtf = True
                    break


        if isOMTFtagIn and recoAbsEta > trig_TF['OMTF'][0] and recoAbsEta < 1.0: 
            if isOMTFprobeIn: continue
            isOMTFprobeIn = True
            if iProbe == omtfIn_iTag: print 'Weird error in isOMTFtagIn: iTag = %d, iProbe = %d' % (chosen_iTag, iProbe)

            h_pt ['uGMT'].Fill(recoPt)
            h_eta['uGMT'].Fill(recoEta)
            h_phi['uGMT'].Fill(recoPhi)
            h_pt ['OMTF'].Fill(recoPt)
            h_eta['OMTF'].Fill(recoEta)
            h_phi['OMTF'].Fill(recoPhi)
            h_eta['BMTF'].Fill(recoEta)

            for WP in trig_WP.keys():
                isTrigger_omtfIn = False
                for iTrk in range(omtf_tree.nTfMuons):
                    if not omtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if (omtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(omtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if REQ_BX0 and omtf_tree.tfMuonBx[iTrk] != 0: continue
                
                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (omtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and 
                            omtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            omtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                    h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                    h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                    h_pt_trg['OMTF_%s' % WP].Fill(recoPt)
                    h_eta_trg['OMTF_%s' % WP].Fill(recoEta)
                    h_phi_trg['OMTF_%s' % WP].Fill(recoPhi)
                    isTrigger_omtfIn = True
                    break

                ## Also check for BMTF tracks
                for iTrk in range(bmtf_tree.nTfMuons):
                    if not bmtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if (bmtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(bmtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if REQ_BX0 and bmtf_tree.tfMuonBx[iTrk] != 0: continue
                    
                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (bmtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and 
                            bmtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            bmtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_eta_trg['BMTF_%s' % WP].Fill(recoEta)
                    
                    if not isTrigger_omtfIn:
                        h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                        h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                        h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                        isTrigger_omtfIn = True
                    break

        if isOMTFtagOut and recoAbsEta > 1.0 and recoAbsEta < trig_TF['OMTF'][1]: 
            if isOMTFprobeOut: continue
            isOMTFprobeOut = True
            if iProbe == omtfOut_iTag: print 'Weird error in isOMTFtagOut: iTag = %d, iProbe = %d' % (chosen_iTag, iProbe)

            h_pt ['uGMT'].Fill(recoPt)
            h_eta['uGMT'].Fill(recoEta)
            h_phi['uGMT'].Fill(recoPhi)
            h_pt ['OMTF'].Fill(recoPt)
            h_eta['OMTF'].Fill(recoEta)
            h_phi['OMTF'].Fill(recoPhi)
            h_eta['EMTF'].Fill(recoEta)

            for WP in trig_WP.keys():
                isTrigger_omtfOut = False
                for iTrk in range(omtf_tree.nTfMuons):
                    if not omtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if (omtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(omtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if REQ_BX0 and omtf_tree.tfMuonBx[iTrk] != 0: continue
                
                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (omtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and 
                            omtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            omtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                    h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                    h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                    h_pt_trg['OMTF_%s' % WP].Fill(recoPt)
                    h_eta_trg['OMTF_%s' % WP].Fill(recoEta)
                    h_phi_trg['OMTF_%s' % WP].Fill(recoPhi)
                    isTrigger_omtfOut = True
                    break

                ## Also check for EMTF tracks
                for iTrk in range(emtf_tree.nTfMuons):
                    if not emtf_tree.tfMuonHwQual[iTrk] in trig_WP[WP]: continue
                    if WP == 'SingleMu7' and emtf_tree.tfMuonHwQual[iTrk] == 11 and emtf_tree.tfMuonLink[iTrk] != 71: continue
                    if (emtf_tree.tfMuonHwPt[iTrk] - 1)*0.5 < TRG_PT - 0.01: continue
                    if REQ_L1_dEta and abs(emtf_tree.tfMuonHwEta[iTrk]*0.010875 - recoEta) > 0.2: continue
                    if REQ_BX0 and emtf_tree.tfMuonBx[iTrk] != 0: continue
                    
                    uGMT_match = False
                    for jTrk in range(uGMT_tree.nMuons):
                        if (emtf_tree.tfMuonBx[iTrk] == uGMT_tree.muonBx[jTrk] and 
                            emtf_tree.tfMuonHwEta[iTrk] == uGMT_tree.muonIEta[jTrk] and 
                            emtf_tree.tfMuonHwPt[iTrk] == uGMT_tree.muonIEt[jTrk]): uGMT_match = True
                    if REQ_uGMT and not uGMT_match: continue

                    h_eta_trg['EMTF_%s' % WP].Fill(recoEta)

                    if not isTrigger_omtfOut:
                        h_pt_trg['uGMT_%s' % WP].Fill(recoPt)
                        h_eta_trg['uGMT_%s' % WP].Fill(recoEta)
                        h_phi_trg['uGMT_%s' % WP].Fill(recoPhi)
                        isTrigger_omtfOut = True
                    break


# Save the Hists


#c1 = TCanvas('c1')
#c1.cd()
#heta.Draw('AP')

#c2 = TCanvas('c2')
#c2.cd()
#heta_trigger.Draw()

#c3 = TCanvas('c3')
#c3.cd()
#tg_eta = TGraphAsymmErrors(heta_trigger, heta, '')
#tg_eta.Draw()

out_file.cd()

nWP = 0
for WP in trig_WP.keys():
    nWP += 1
    print '\n***********************************'
    print '*** %s_%d%s%s%s%s efficiency ***' % (WP, TRG_PT, dEta_str, BX0_str, uGMT_str, HLT_str)
    print '***********************************'
    for TF in trig_TF.keys():
        key = '%s_%s' % (TF, WP)
        print '%s: %.1f +/- %.1f%%' % ( TF, 100 * h_phi_trg[key].Integral() / h_phi[TF].Integral(), 
                                        (100 * h_phi_trg[key].Integral() / h_phi[TF].Integral()) * 
                                        math.sqrt(h_phi[TF].Integral()) / h_phi[TF].Integral() )

        if nWP == 1: h_pt[TF].Write() 
        h_pt_trg[key].Write() 
        h_pt_trg[key].Divide(h_pt[TF])
        h_pt_trg[key].SetName(h_pt_trg[key].GetName()+'_eff')
        h_pt_trg[key].Write()

        if nWP == 1: h_eta[TF].Write() 
        h_eta_trg[key].Write() 
        h_eta_trg[key].Divide(h_eta[TF])
        h_eta_trg[key].SetName(h_eta_trg[key].GetName()+'_eff')
        h_eta_trg[key].Write()

        if nWP == 1: h_phi[TF].Write() 
        h_phi_trg[key].Write() 
        h_phi_trg[key].Divide(h_phi[TF])
        h_phi_trg[key].SetName(h_phi_trg[key].GetName()+'_eff')
        h_phi_trg[key].Write()


del out_file


#raw_input('Press return to continue...')
