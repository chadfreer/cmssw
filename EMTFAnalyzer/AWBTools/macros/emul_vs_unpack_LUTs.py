#! /usr/bin/env python

## Compare tracks coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside emul_vs_unpack_LUTs'

    file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936_May_24_fix.root'
    out_file = TFile('plots/emul_vs_unpack_LUTs.root','recreate')

    tree_name = 'Events'

    file = TFile.Open(file_name)
    tree = file.Get(tree_name)

    #################
    ### Book counters
    #################

    numHits = {}
    numHitsUnm = {}
    numHitsUnmExist = {}
    numHitsUnmNonZeroWire = {}
    numTrks = {}
    numTrksUnm = {}
    numTrksUnmExist = {}

    numHits[0] = 0
    numHitsUnm[0] = 0
    numHitsUnmExist[0] = 0
    numHitsUnmNonZeroWire[0] = 0
    numTrks[0] = 0
    numTrksUnm[0] = 0
    numTrksUnmExist[0] = 0

    numHits[1] = 0
    numHitsUnm[1] = 0
    numHitsUnmExist[1] = 0
    numHitsUnmNonZeroWire[1] = 0
    numTrks[1] = 0
    numTrksUnm[1] = 0
    numTrksUnmExist[1] = 0

    numTrksMatched = {}
    numAddrCorr = {}
    numDPhi = {}
    numDTheta = {}
    numCLCT = {}
    numFR = {}
    numDPhiCorr = {}
    numDThetaCorr = {}
    numCLCTCorr = {}
    numFRCorr = {}
    numDPhiIncorr = {}
    numDThetaIncorr = {}
    numCLCTIncorr = {}
    numFRIncorr = {}
    numDPhiFlip = {}
    numDThetaFlip = {}
    numCLCTFlip = {}
    numFRFlip = {}

    for iMode in range(16):
        numTrksMatched[iMode] = 0
        numAddrCorr[iMode] = 0
        numDPhi[iMode] = 0
        numDTheta[iMode] = 0
        numCLCT[iMode] = 0
        numFR[iMode] = 0
        numDPhiCorr[iMode] = 0
        numDThetaCorr[iMode] = 0
        numCLCTCorr[iMode] = 0
        numFRCorr[iMode] = 0
        numDPhiIncorr[iMode] = 0
        numDThetaIncorr[iMode] = 0
        numCLCTIncorr[iMode] = 0
        numFRIncorr[iMode] = 0
        numDPhiFlip[iMode] = 0
        numDThetaFlip[iMode] = 0
        numCLCTFlip[iMode] = 0
        numFRFlip[iMode] = 0

    numFr = {}
    numFrCorr = {}
    numFrIncorr = {}
    numFrFlip = {}

    for iSt in range(4):
        numFr[iSt+1] = 0
        numFrCorr[iSt+1] = 0
        numFrIncorr[iSt+1] = 0
        numFrFlip[iSt+1] = 0

    numDphi = {}
    numDphiCorr = {}
    numDphiIncorr = {}
    numDphiFlip = {}

    for iPhi in range(6):
        numDphi[iPhi] = 0
        numDphiCorr[iPhi] = 0
        numDphiIncorr[iPhi] = 0
        numDphiFlip[iPhi] = 0
        
        
    ###################
    ### Book histograms
    ###################
        
    dPhi_bins = [301, -150.5, 150.5]
    diff_dPhi_bins = [21, -10.5, 10.5]
    dTheta_bins = [17, -8.5, 8.5]
    eta_bins = [50, -2.5, 2.5]
    mode_bins = [18, -1.5, 16.5]
    pT_bins = [32, -1.5, 30.5]

    h_diff_dPhi_12 = TH1D('h_diff_dPhi_12', 'Emulator - Unpacker dPhi_12', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_12_lowEtaP = TH1D('h_diff_dPhi_12_lowEtaP', 'Emulator - Unpacker dPhi_12', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_12_lowEtaM = TH1D('h_diff_dPhi_12_lowEtaM', 'Emulator - Unpacker dPhi_12', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_12_hiEtaP = TH1D('h_diff_dPhi_12_hiEtaP', 'Emulator - Unpacker dPhi_12', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_12_hiEtaM = TH1D('h_diff_dPhi_12_hiEtaM', 'Emulator - Unpacker dPhi_12', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13 = TH1D('h_diff_dPhi_13', 'Emulator - Unpacker dPhi_13', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13_lowEtaP = TH1D('h_diff_dPhi_13_lowEtaP', 'Emulator - Unpacker dPhi_13', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13_lowEtaM = TH1D('h_diff_dPhi_13_lowEtaM', 'Emulator - Unpacker dPhi_13', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13_hiEtaP = TH1D('h_diff_dPhi_13_hiEtaP', 'Emulator - Unpacker dPhi_13', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13_hiEtaM = TH1D('h_diff_dPhi_13_hiEtaM', 'Emulator - Unpacker dPhi_13', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_14 = TH1D('h_diff_dPhi_14', 'Emulator - Unpacker dPhi_14', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_23 = TH1D('h_diff_dPhi_23', 'Emulator - Unpacker dPhi_23', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_24 = TH1D('h_diff_dPhi_24', 'Emulator - Unpacker dPhi_24', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_34 = TH1D('h_diff_dPhi_34', 'Emulator - Unpacker dPhi_34', diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])

    h_diff_dTheta_12 = TH1D('h_diff_dTheta_12', 'Emulator - Unpacker dTheta_12', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_13 = TH1D('h_diff_dTheta_13', 'Emulator - Unpacker dTheta_13', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_14 = TH1D('h_diff_dTheta_14', 'Emulator - Unpacker dTheta_14', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_23 = TH1D('h_diff_dTheta_23', 'Emulator - Unpacker dTheta_23', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_24 = TH1D('h_diff_dTheta_24', 'Emulator - Unpacker dTheta_24', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_34 = TH1D('h_diff_dTheta_34', 'Emulator - Unpacker dTheta_34', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])

    h_Emu_vs_Unp_dPhi_12 = TH2D('h_Emu_vs_Unp_dPhi_12', 'Emulator vs. Unpacker dPhi_12', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], dPhi_bins[0], dPhi_bins[1], dPhi_bins[2]) 
    h_Emu_vs_Unp_dPhi_13 = TH2D('h_Emu_vs_Unp_dPhi_13', 'Emulator vs. Unpacker dPhi_13', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], dPhi_bins[0], dPhi_bins[1], dPhi_bins[2]) 
    h_Emu_vs_Unp_dPhi_14 = TH2D('h_Emu_vs_Unp_dPhi_14', 'Emulator vs. Unpacker dPhi_14', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], dPhi_bins[0], dPhi_bins[1], dPhi_bins[2]) 
    h_Emu_vs_Unp_dPhi_23 = TH2D('h_Emu_vs_Unp_dPhi_23', 'Emulator vs. Unpacker dPhi_23', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], dPhi_bins[0], dPhi_bins[1], dPhi_bins[2]) 
    h_Emu_vs_Unp_dPhi_24 = TH2D('h_Emu_vs_Unp_dPhi_24', 'Emulator vs. Unpacker dPhi_24', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], dPhi_bins[0], dPhi_bins[1], dPhi_bins[2]) 
    h_Emu_vs_Unp_dPhi_34 = TH2D('h_Emu_vs_Unp_dPhi_34', 'Emulator vs. Unpacker dPhi_34', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], dPhi_bins[0], dPhi_bins[1], dPhi_bins[2]) 

    h_Emu_vs_Unp_dTheta_12 = TH2D('h_Emu_vs_Unp_dTheta_12', 'Emulator vs. Unpacker dTheta_12', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2]) 
    h_Emu_vs_Unp_dTheta_13 = TH2D('h_Emu_vs_Unp_dTheta_13', 'Emulator vs. Unpacker dTheta_13', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2]) 
    h_Emu_vs_Unp_dTheta_14 = TH2D('h_Emu_vs_Unp_dTheta_14', 'Emulator vs. Unpacker dTheta_14', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2]) 
    h_Emu_vs_Unp_dTheta_23 = TH2D('h_Emu_vs_Unp_dTheta_23', 'Emulator vs. Unpacker dTheta_23', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2]) 
    h_Emu_vs_Unp_dTheta_24 = TH2D('h_Emu_vs_Unp_dTheta_24', 'Emulator vs. Unpacker dTheta_24', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2]) 
    h_Emu_vs_Unp_dTheta_34 = TH2D('h_Emu_vs_Unp_dTheta_34', 'Emulator vs. Unpacker dTheta_34', dTheta_bins[0], dTheta_bins[1], dTheta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2]) 

    h_diff_dPhi_12_vs_mode = TH2D('h_diff_dPhi_12_vs_mode', 'Emulator - Unpacker dPhi_12', mode_bins[0], mode_bins[1], mode_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13_vs_mode = TH2D('h_diff_dPhi_13_vs_mode', 'Emulator - Unpacker dPhi_13', mode_bins[0], mode_bins[1], mode_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_14_vs_mode = TH2D('h_diff_dPhi_14_vs_mode', 'Emulator - Unpacker dPhi_14', mode_bins[0], mode_bins[1], mode_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_23_vs_mode = TH2D('h_diff_dPhi_23_vs_mode', 'Emulator - Unpacker dPhi_23', mode_bins[0], mode_bins[1], mode_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_24_vs_mode = TH2D('h_diff_dPhi_24_vs_mode', 'Emulator - Unpacker dPhi_24', mode_bins[0], mode_bins[1], mode_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_34_vs_mode = TH2D('h_diff_dPhi_34_vs_mode', 'Emulator - Unpacker dPhi_34', mode_bins[0], mode_bins[1], mode_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])

    h_diff_dTheta_12_vs_mode = TH2D('h_diff_dTheta_12_vs_mode', 'Emulator - Unpacker dTheta_12', mode_bins[0], mode_bins[1], mode_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_13_vs_mode = TH2D('h_diff_dTheta_13_vs_mode', 'Emulator - Unpacker dTheta_13', mode_bins[0], mode_bins[1], mode_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_14_vs_mode = TH2D('h_diff_dTheta_14_vs_mode', 'Emulator - Unpacker dTheta_14', mode_bins[0], mode_bins[1], mode_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])

    h_diff_dPhi_12_vs_eta = TH2D('h_diff_dPhi_12_vs_eta', 'Emulator - Unpacker dPhi_12', eta_bins[0], eta_bins[1], eta_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_13_vs_eta = TH2D('h_diff_dPhi_13_vs_eta', 'Emulator - Unpacker dPhi_13', eta_bins[0], eta_bins[1], eta_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_14_vs_eta = TH2D('h_diff_dPhi_14_vs_eta', 'Emulator - Unpacker dPhi_14', eta_bins[0], eta_bins[1], eta_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_23_vs_eta = TH2D('h_diff_dPhi_23_vs_eta', 'Emulator - Unpacker dPhi_23', eta_bins[0], eta_bins[1], eta_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_24_vs_eta = TH2D('h_diff_dPhi_24_vs_eta', 'Emulator - Unpacker dPhi_24', eta_bins[0], eta_bins[1], eta_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])
    h_diff_dPhi_34_vs_eta = TH2D('h_diff_dPhi_34_vs_eta', 'Emulator - Unpacker dPhi_34', eta_bins[0], eta_bins[1], eta_bins[2], diff_dPhi_bins[0], diff_dPhi_bins[1], diff_dPhi_bins[2])

    h_diff_dTheta_12_vs_eta = TH2D('h_diff_dTheta_12_vs_eta', 'Emulator - Unpacker dTheta_12', eta_bins[0], eta_bins[1], eta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_13_vs_eta = TH2D('h_diff_dTheta_13_vs_eta', 'Emulator - Unpacker dTheta_13', eta_bins[0], eta_bins[1], eta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])
    h_diff_dTheta_14_vs_eta = TH2D('h_diff_dTheta_14_vs_eta', 'Emulator - Unpacker dTheta_14', eta_bins[0], eta_bins[1], eta_bins[2], dTheta_bins[0], dTheta_bins[1], dTheta_bins[2])

    h_Emu_vs_Unp_pT_same_addr = TH2D('h_Emu_vs_Unp_pT_same_addr', 'Emulator vs. Unpacker pT, same LUT address', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_Emu_vs_Unp_pT_diff_addr = TH2D('h_Emu_vs_Unp_pT_diff_addr', 'Emulator vs. Unpacker pT, mode 15, different LUT address', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])

    ## Main event loop    
    for iEvt in range(tree.GetEntries()):
        
        if (iEvt > 100000): continue
        # if iEvt % 1000 is 0: print 'Event #', iEvt
        tree.GetEntry(iEvt)

        ## Get branches from the trees
        Event = tree.EventAuxiliary
        Hits_1 = tree.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        Trks_1 = tree.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        Hits_2 = tree.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_2 = tree.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation

        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        if (nHits1 == 0 and nHits2 == 0): continue

        #####################################################################################
        ### Compare hits in emulator and unpacker
        ###   * Emulator outputs all hits it received, and always duplicates neighbor hits
        ###   * Unpacker usually outputs neighbor hits twice, but sometimes it misses one
        #####################################################################################

        ## Check that unpacker hits have match in emulator                                                                                                                 
        unmatched_hit_exists = False
        neighbor_hit_exists = False
        bx_m3_hit_exists = False
        bx_p3_hit_exists = False
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            if Hit1.Neighbor() == 1:  ## Don't remove neighbor hits (even though they should appear twice)                                                                 
                neighbor_hit_exists = True
                ## continue                                                                                                                                                
            if Hit1.BX() < -2:
                bx_m3_hit_exists = True
            if Hit1.BX() > 2:
                bx_p3_hit_exists = True

            numHits[0] += 1
            unp_hit_matched = False
            for iHit2 in range(nHits2):
                Hit2 = Hits_2.at(iHit2)
                if HitsMatch( Hit1, Hit2 ):
                    unp_hit_matched = True

            if not unp_hit_matched:
                unmatched_hit_exists = True
                numHitsUnm[0] += 1
                if nHits2 > 0:
                    numHitsUnmExist[0] += 1
                    if Hit1.Wire() != 0:
                        numHitsUnmNonZeroWire[0] += 1

        ## Check that emulator hits have match in unpacker                                                                                                                 
        for iHit2 in range(nHits2):
            Hit2 = Hits_2.at(iHit2)

            numHits[1] += 1
            emu_hit_matched = False
            for iHit1 in range(nHits1):
                Hit1 = Hits_1.at(iHit1)
                if HitsMatch( Hit1, Hit2 ):
                    emu_hit_matched = True

            if not emu_hit_matched:
                ## unmatched_hit_exists = True                                                                                                                             
                numHitsUnm[1] += 1
                if nHits1 > 0:
                    numHitsUnmExist[1] += 1
                    if Hit2.Wire() != 0:
                        numHitsUnmNonZeroWire[1] += 1

        #####################################################################################
        ### Compare tracks in emulator and unpacker
        ###   * Only compare if emulator and unpacker hits are identical
        #####################################################################################

        if unmatched_hit_exists:
            continue
        if ( nTrks1 == 0 and nTrks2 == 0 ):
            continue

        ## Check that unpacker tracks have match in emulator                                                                                                               
        for iTrk1 in range(nTrks1):
            Trk1 = Trks_1.at(iTrk1)
            if Trk1.BX() < -1 or Trk1.BX() > 1:
                continue
            if Trk1.BX() < 0 and bx_m3_hit_exists:
                continue
            if Trk1.BX() > 0 and bx_p3_hit_exists:
                continue
            if Trk1.Pt_GMT() == 0:
                continue

            if nTrks2 == 0:
                print '******* Event %d *******' % Event.event()
                print('Data:'),
                PrintEMTFTrack( Trk1 )

                print 'Hits'
                for iHit2 in range(nHits2):
                    Hit2 = Hits_2.at(iHit2)
                    PrintEMTFHitExtra( Hit2 )
                PrintSimulatorHitHeader()
                for iHit2 in range(nHits2):
                    Hit2 = Hits_2.at(iHit2)
                    PrintSimulatorHit( Hit2 )
                print '***********************'
                print ''

            numTrks[0] += 1
            unp_trk_matched = False
            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)
                if TracksMatch( Trk1, Trk2 ):
                    # if Trk1.Eta_GMT() == Trk2.Eta_GMT() and Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.Mode() == Trk2.Mode():
                    if True:
                        unp_trk_matched = True
                        numTrksMatched[Trk1.Mode()] += 1
                        
                        # if ( Trk1.BX() == Trk2.BX() and Trk1.Mode() and Trk1.Sector() == Trk2.Sector() and 
                        #      Trk1.Eta_GMT() == Trk2.Eta_GMT() and Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.Mode() != Trk2.Mode() ):
                        # # if ( Trk1.BX() == Trk2.BX() and Trk1.Mode() == Trk2.Mode() and Trk1.Sector() == Trk2.Sector() and 
                        # #      ( abs(Trk1.Phi_GMT() - Trk2.Phi_GMT()) > 0 or abs(Trk1.Eta_GMT() - Trk2.Eta_GMT()) > 2 ) ):
                        # # if (Trk1.Quality() > 7 and abs(Trk1.Pt() - Trk2.Pt()) > 10 and min(Trk1.Pt(), Trk2.Pt()) < 10 ):

                            # print '******* Event %d *******' % Event.event()
                            # print('Data:'),
                            # PrintEMTFTrack( Trk1 )
                            # # PrintPtLUT( Trk1 )
                            # print('Emul:'),
                            # PrintEMTFTrack( Trk2 )
                            # # PrintPtLUT( Trk2 )
                            # print 'Hits'
                            # for iHit2 in range(nHits2):
                            #     Hit2 = Hits_2.at(iHit2)
                            #     PrintEMTFHitExtra( Hit2 )
                            # PrintSimulatorHitHeader()
                            # for iHit2 in range(nHits2):
                            #     Hit2 = Hits_2.at(iHit2)
                            #     PrintSimulatorHit( Hit2 )
                            # print '***********************'
                            # print ''
                            
                        if PtLutAddrMatch( Trk1, Trk2 ):
                            numAddrCorr[Trk1.Mode()] += 1
                            h_Emu_vs_Unp_pT_same_addr.Fill( Trk1.Pt(), Trk2.Pt() )
                        else:
                            if (Trk1.Mode() == 15): h_Emu_vs_Unp_pT_diff_addr.Fill( Trk1.Pt(), Trk2.Pt() )
                        if ( Trk1.DPhi_12() != -999 or Trk1.DPhi_13() != -999 or Trk1.DPhi_14() != -999 or
                             Trk1.DPhi_23() != -999 or Trk1.DPhi_24() != -999 or Trk1.DPhi_34() != -999 ):
                            numDPhi[Trk1.Mode()] += 1
                        if ( Trk1.DTheta_12() != -999 or Trk1.DTheta_13() != -999 or Trk1.DTheta_14() != -999 or
                             Trk1.DTheta_23() != -999 or Trk1.DTheta_24() != -999 or Trk1.DTheta_34() != -999 ):
                            numDTheta[Trk1.Mode()] += 1
                        if ( Trk1.CLCT_1() != -999 or Trk1.CLCT_2() != -999 or Trk1.CLCT_3() != -999 or Trk1.CLCT_4() != -999 ):
                            numCLCT[Trk1.Mode()] += 1
                        if ( Trk1.FR_1() != -999 or Trk1.FR_2() != -999 or Trk1.FR_3() != -999 or Trk1.FR_4() != -999 ):
                            numFR[Trk1.Mode()] += 1
                        if ( (Trk1.DPhi_12() == Trk2.DPhi_12() and Trk1.DPhi_12() != -999) or (Trk1.DPhi_13() == Trk2.DPhi_13() and Trk1.DPhi_13() != -999) 
                             or (Trk1.DPhi_14() == Trk2.DPhi_14() and Trk1.DPhi_14() != -999) or (Trk1.DPhi_23() == Trk2.DPhi_23() and Trk1.DPhi_23() != -999) 
                             or (Trk1.DPhi_24() == Trk2.DPhi_24() and Trk1.DPhi_24() != -999) or (Trk1.DPhi_34() == Trk2.DPhi_34() and Trk1.DPhi_34() != -999) ):
                            numDPhiCorr[Trk1.Mode()] += 1
                        if ( (Trk1.DTheta_12() == Trk2.DTheta_12() and Trk1.DTheta_12() != -999) or (Trk1.DTheta_13() == Trk2.DTheta_13() and Trk1.DTheta_13() != -999) 
                             or (Trk1.DTheta_14() == Trk2.DTheta_14() and Trk1.DTheta_14() != -999) or (Trk1.DTheta_23() == Trk2.DTheta_23() and Trk1.DTheta_23() != -999) 
                             or (Trk1.DTheta_24() == Trk2.DTheta_24() and Trk1.DTheta_24() != -999) or (Trk1.DTheta_34() == Trk2.DTheta_34() and Trk1.DTheta_34() != -999) ):
                            numDThetaCorr[Trk1.Mode()] += 1
                        if ( (Trk1.CLCT_1() == Trk2.CLCT_1() and Trk1.CLCT_1() != -999) or (Trk1.CLCT_2() == Trk2.CLCT_2() and Trk1.CLCT_2() != -999) 
                             or (Trk1.CLCT_3() == Trk2.CLCT_3() and Trk1.CLCT_3() != -999) or (Trk1.CLCT_4() == Trk2.CLCT_4() and Trk1.CLCT_4() != -999) ):
                            numCLCTCorr[Trk1.Mode()] += 1
                        if ( (Trk1.FR_1() == Trk2.FR_1() and Trk1.FR_1() != -999) or (Trk1.FR_2() == Trk2.FR_2() and Trk1.FR_2() != -999) 
                             or (Trk1.FR_3() == Trk2.FR_3() and Trk1.FR_3() != -999) or (Trk1.FR_4() == Trk2.FR_4() and Trk1.FR_4() != -999) ):
                            numFRCorr[Trk1.Mode()] += 1
                        if ( (Trk1.DPhi_12() != Trk2.DPhi_12() and Trk1.DPhi_12() != -999) or (Trk1.DPhi_13() != Trk2.DPhi_13() and Trk1.DPhi_13() != -999) 
                             or (Trk1.DPhi_14() != Trk2.DPhi_14() and Trk1.DPhi_14() != -999) or (Trk1.DPhi_23() != Trk2.DPhi_23() and Trk1.DPhi_23() != -999) 
                             or (Trk1.DPhi_24() != Trk2.DPhi_24() and Trk1.DPhi_24() != -999) or (Trk1.DPhi_34() != Trk2.DPhi_34() and Trk1.DPhi_34() != -999) ):
                            numDPhiIncorr[Trk1.Mode()] += 1
                        if ( (Trk1.DTheta_12() != Trk2.DTheta_12() and Trk1.DTheta_12() != -999) or (Trk1.DTheta_13() != Trk2.DTheta_13() and Trk1.DTheta_13() != -999) 
                             or (Trk1.DTheta_14() != Trk2.DTheta_14() and Trk1.DTheta_14() != -999) or (Trk1.DTheta_23() != Trk2.DTheta_23() and Trk1.DTheta_23() != -999) 
                             or (Trk1.DTheta_24() != Trk2.DTheta_24() and Trk1.DTheta_24() != -999) or (Trk1.DTheta_34() != Trk2.DTheta_34() and Trk1.DTheta_34() != -999) ):
                            numDThetaIncorr[Trk1.Mode()] += 1
                        if ( (Trk1.CLCT_1() != Trk2.CLCT_1() and Trk1.CLCT_1() != -999) or (Trk1.CLCT_2() != Trk2.CLCT_2() and Trk1.CLCT_2() != -999) 
                             or (Trk1.CLCT_3() != Trk2.CLCT_3() and Trk1.CLCT_3() != -999) or (Trk1.CLCT_4() != Trk2.CLCT_4() and Trk1.CLCT_4() != -999) ):
                            numCLCTIncorr[Trk1.Mode()] += 1
                        if ( (Trk1.FR_1() != Trk2.FR_1() and Trk1.FR_1() != -999) or (Trk1.FR_2() != Trk2.FR_2() and Trk1.FR_2() != -999) 
                             or (Trk1.FR_3() != Trk2.FR_3() and Trk1.FR_3() != -999) or (Trk1.FR_4() != Trk2.FR_4() and Trk1.FR_4() != -999) ):
                            numFRIncorr[Trk1.Mode()] += 1
                        if ( (Trk1.DPhi_12() == -1*Trk2.DPhi_12() and Trk1.DPhi_12() != 0) or (Trk1.DPhi_13() == -1*Trk2.DPhi_13() and Trk1.DPhi_13() != 0) 
                             or (Trk1.DPhi_14() == -1*Trk2.DPhi_14() and Trk1.DPhi_14() != 0) or (Trk1.DPhi_23() == -1*Trk2.DPhi_23() and Trk1.DPhi_23() != 0) 
                             or (Trk1.DPhi_24() == -1*Trk2.DPhi_24() and Trk1.DPhi_24() != 0) or (Trk1.DPhi_34() == -1*Trk2.DPhi_34() and Trk1.DPhi_34() != 0) ):
                            numDPhiFlip[Trk1.Mode()] += 1
                        if ( (Trk1.DTheta_12() == -1*Trk2.DTheta_12() and Trk1.DTheta_12() != 0) or (Trk1.DTheta_13() == -1*Trk2.DTheta_13() and Trk1.DTheta_13() != 0) 
                             or (Trk1.DTheta_14() == -1*Trk2.DTheta_14() and Trk1.DTheta_14() != 0) or (Trk1.DTheta_23() == -1*Trk2.DTheta_23() and Trk1.DTheta_23() != 0) 
                             or (Trk1.DTheta_24() == -1*Trk2.DTheta_24() and Trk1.DTheta_24() != 0) or (Trk1.DTheta_34() == -1*Trk2.DTheta_34() and Trk1.DTheta_34() != 0) ):
                            numDThetaFlip[Trk1.Mode()] += 1
                        if ( (Trk1.CLCT_1() == -1*Trk2.CLCT_1() and Trk1.CLCT_1() != 0) or (Trk1.CLCT_2() == -1*Trk2.CLCT_2() and Trk1.CLCT_2() != 0) 
                             or (Trk1.CLCT_3() == -1*Trk2.CLCT_3() and Trk1.CLCT_3() != 0) or (Trk1.CLCT_4() == -1*Trk2.CLCT_4() and Trk1.CLCT_4() != 0) ):
                            numCLCTFlip[Trk1.Mode()] += 1
                        if ( (Trk1.FR_1() == -1*Trk2.FR_1() and Trk1.FR_1() != 0) or (Trk1.FR_2() == -1*Trk2.FR_2() and Trk1.FR_2() != 0) 
                             or (Trk1.FR_3() == -1*Trk2.FR_3() and Trk1.FR_3() != 0) or (Trk1.FR_4() == -1*Trk2.FR_4() and Trk1.FR_4() != 0) ):
                            numFRFlip[Trk1.Mode()] += 1

                        if ( Trk1.FR_1() != -999 ):
                            numFr[1] += 1
                        if ( Trk1.FR_2() != -999 ):
                            numFr[2] += 1
                        if ( Trk1.FR_3() != -999 ):
                            numFr[3] += 1
                        if ( Trk1.FR_4() != -999 ):
                            numFr[4] += 1

                        if ( Trk1.FR_1() != -999 and Trk1.FR_1() == Trk2.FR_1() ):
                            numFrCorr[1] += 1
                        if ( Trk1.FR_2() != -999 and Trk1.FR_2() == Trk2.FR_2() ):
                            numFrCorr[2] += 1
                        if ( Trk1.FR_3() != -999 and Trk1.FR_3() == Trk2.FR_3() ):
                            numFrCorr[3] += 1
                        if ( Trk1.FR_4() != -999 and Trk1.FR_4() == Trk2.FR_4() ):
                            numFrCorr[4] += 1

                        if ( Trk1.FR_1() != -999 and Trk1.FR_1() != Trk2.FR_1() ):
                            numFrIncorr[1] += 1
                        if ( Trk1.FR_2() != -999 and Trk1.FR_2() != Trk2.FR_2() ):
                            numFrIncorr[2] += 1
                        if ( Trk1.FR_3() != -999 and Trk1.FR_3() != Trk2.FR_3() ):
                            numFrIncorr[3] += 1
                        if ( Trk1.FR_4() != -999 and Trk1.FR_4() != Trk2.FR_4() ):
                            numFrIncorr[4] += 1

                        if ( Trk1.FR_1() != 0 and Trk1.FR_1() == -1*Trk2.FR_1() ):
                            numFrFlip[1] += 1
                        if ( Trk1.FR_2() != 0 and Trk1.FR_2() == -1*Trk2.FR_2() ):
                            numFrFlip[2] += 1
                        if ( Trk1.FR_3() != 0 and Trk1.FR_3() == -1*Trk2.FR_3() ):
                            numFrFlip[3] += 1
                        if ( Trk1.FR_4() != 0 and Trk1.FR_4() == -1*Trk2.FR_4() ):
                            numFrFlip[4] += 1

                        if ( Trk1.DPhi_12() != -999 ):
                            numDphi[0] += 1
                            if ( Trk1.DPhi_12() == Trk2.DPhi_12() ): numDphiCorr[0] += 1
                            else: numDphiIncorr[0] += 1
                            if ( Trk1.DPhi_12() != 0  and Trk1.DPhi_12() == -1*Trk2.DPhi_12() ): numDphiFlip[0] += 1
                        if ( Trk1.DPhi_13() != -999 ):
                            numDphi[1] += 1
                            if ( Trk1.DPhi_13() == Trk2.DPhi_13() ): numDphiCorr[1] += 1
                            else: numDphiIncorr[1] += 1
                            if ( Trk1.DPhi_13() != 0  and Trk1.DPhi_13() == -1*Trk2.DPhi_13() ): numDphiFlip[1] += 1
                        if ( Trk1.DPhi_14() != -999 ):
                            numDphi[2] += 1
                            if ( Trk1.DPhi_14() == Trk2.DPhi_14() ): numDphiCorr[2] += 1
                            else: numDphiIncorr[2] += 1
                            if ( Trk1.DPhi_14() != 0  and Trk1.DPhi_14() == -1*Trk2.DPhi_14() ): numDphiFlip[2] += 1
                        if ( Trk1.DPhi_23() != -999 ):
                            numDphi[3] += 1
                            if ( Trk1.DPhi_23() == Trk2.DPhi_23() ): numDphiCorr[3] += 1
                            else: numDphiIncorr[3] += 1
                            if ( Trk1.DPhi_23() != 0  and Trk1.DPhi_23() == -1*Trk2.DPhi_23() ): numDphiFlip[3] += 1
                        if ( Trk1.DPhi_24() != -999 ):
                            numDphi[4] += 1
                            if ( Trk1.DPhi_24() == Trk2.DPhi_24() ): numDphiCorr[4] += 1
                            else: numDphiIncorr[4] += 1
                            if ( Trk1.DPhi_24() != 0  and Trk1.DPhi_24() == -1*Trk2.DPhi_24() ): numDphiFlip[4] += 1
                        if ( Trk1.DPhi_34() != -999 ):
                            numDphi[5] += 1
                            if ( Trk1.DPhi_34() == Trk2.DPhi_34() ): numDphiCorr[5] += 1
                            else: numDphiIncorr[5] += 1
                            if ( Trk1.DPhi_34() != 0  and Trk1.DPhi_34() == -1*Trk2.DPhi_34() ): numDphiFlip[5] += 1


                        if (Trk1.DPhi_12() != -999): 
                            h_Emu_vs_Unp_dPhi_12.Fill( Trk1.DPhi_12(), Trk2.DPhi_12() )
                            h_diff_dPhi_12.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                            if   (Trk1.Eta() < -1.6): h_diff_dPhi_12_hiEtaM.Fill ( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                            elif (Trk1.Eta() <    0): h_diff_dPhi_12_lowEtaM.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                            elif (Trk1.Eta() <  1.6): h_diff_dPhi_12_lowEtaP.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                            else                    : h_diff_dPhi_12_hiEtaP.Fill ( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                            h_diff_dPhi_12_vs_mode.Fill( Trk1.Mode(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                            h_diff_dPhi_12_vs_eta.Fill( Trk1.Eta(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_12() - Trk1.DPhi_12()) ) )
                        if (Trk1.DPhi_13() != -999): 
                            h_Emu_vs_Unp_dPhi_13.Fill( Trk1.DPhi_13(), Trk2.DPhi_13() )
                            if   (Trk1.Eta() < -1.6): h_diff_dPhi_13_hiEtaM.Fill ( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                            elif (Trk1.Eta() <    0): h_diff_dPhi_13_lowEtaM.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                            elif (Trk1.Eta() <  1.6): h_diff_dPhi_13_lowEtaP.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                            else                    : h_diff_dPhi_13_hiEtaP.Fill ( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                            h_diff_dPhi_13.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                            h_diff_dPhi_13_vs_mode.Fill( Trk1.Mode(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                            h_diff_dPhi_13_vs_eta.Fill( Trk1.Eta(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_13() - Trk1.DPhi_13()) ) )
                        if (Trk1.DPhi_14() != -999): 
                            h_Emu_vs_Unp_dPhi_14.Fill( Trk1.DPhi_14(), Trk2.DPhi_14() )
                            h_diff_dPhi_14.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_14() - Trk1.DPhi_14()) ) )
                            h_diff_dPhi_14_vs_mode.Fill( Trk1.Mode(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_14() - Trk1.DPhi_14()) ) )
                            h_diff_dPhi_14_vs_eta.Fill( Trk1.Eta(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_14() - Trk1.DPhi_14()) ) )
                        if (Trk1.DPhi_23() != -999): 
                            h_Emu_vs_Unp_dPhi_23.Fill( Trk1.DPhi_23(), Trk2.DPhi_23() )
                            h_diff_dPhi_23.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_23() - Trk1.DPhi_23()) ) )
                            h_diff_dPhi_23_vs_mode.Fill( Trk1.Mode(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_23() - Trk1.DPhi_23()) ) )
                            h_diff_dPhi_23_vs_eta.Fill( Trk1.Eta(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_23() - Trk1.DPhi_23()) ) )
                        if (Trk1.DPhi_24() != -999): 
                            h_Emu_vs_Unp_dPhi_24.Fill( Trk1.DPhi_24(), Trk2.DPhi_24() )
                            h_diff_dPhi_24.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_24() - Trk1.DPhi_24()) ) )
                            h_diff_dPhi_24_vs_mode.Fill( Trk1.Mode(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_24() - Trk1.DPhi_24()) ) )
                            h_diff_dPhi_24_vs_eta.Fill( Trk1.Eta(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_24() - Trk1.DPhi_24()) ) )
                        if (Trk1.DPhi_34() != -999): 
                            h_Emu_vs_Unp_dPhi_34.Fill( Trk1.DPhi_34(), Trk2.DPhi_34() )
                            h_diff_dPhi_34.Fill( max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_34() - Trk1.DPhi_34()) ) )
                            h_diff_dPhi_34_vs_mode.Fill( Trk1.Mode(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_34() - Trk1.DPhi_34()) ) )
                            h_diff_dPhi_34_vs_eta.Fill( Trk1.Eta(), max(diff_dPhi_bins[1]+0.01, min(diff_dPhi_bins[2]-0.01, Trk2.DPhi_34() - Trk1.DPhi_34()) ) )
                        
                        if (Trk1.DTheta_12() != -999): 
                            h_Emu_vs_Unp_dTheta_12.Fill( Trk1.DTheta_12(), Trk2.DTheta_12() )
                            h_diff_dTheta_12.Fill( max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_12() - Trk1.DTheta_12()) ) )
                            h_diff_dTheta_12_vs_mode.Fill( Trk1.Mode(), max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_12() - Trk1.DTheta_12()) ) )
                            h_diff_dTheta_12_vs_eta.Fill( Trk1.Eta(), max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_12() - Trk1.DTheta_12()) ) )
                        if (Trk1.DTheta_13() != -999): 
                            h_Emu_vs_Unp_dTheta_13.Fill( Trk1.DTheta_13(), Trk2.DTheta_13() )
                            h_diff_dTheta_13.Fill( max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_13() - Trk1.DTheta_13()) ) )
                            h_diff_dTheta_13_vs_mode.Fill( Trk1.Mode(), max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_13() - Trk1.DTheta_13()) ) )
                            h_diff_dTheta_13_vs_eta.Fill( Trk1.Eta(), max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_13() - Trk1.DTheta_13()) ) )
                        if (Trk1.DTheta_14() != -999): 
                            h_Emu_vs_Unp_dTheta_14.Fill( Trk1.DTheta_14(), Trk2.DTheta_14() )
                            h_diff_dTheta_14.Fill( max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_14() - Trk1.DTheta_14()) ) )
                            h_diff_dTheta_14_vs_mode.Fill( Trk1.Mode(), max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_14() - Trk1.DTheta_14()) ) )
                            h_diff_dTheta_14_vs_eta.Fill( Trk1.Eta(), max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_14() - Trk1.DTheta_14()) ) )
                        if (Trk1.DTheta_23() != -999): 
                            h_Emu_vs_Unp_dTheta_23.Fill( Trk1.DTheta_23(), Trk2.DTheta_23() )
                            h_diff_dTheta_23.Fill( max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_23() - Trk1.DTheta_23()) ) )
                        if (Trk1.DTheta_24() != -999): 
                            h_Emu_vs_Unp_dTheta_24.Fill( Trk1.DTheta_24(), Trk2.DTheta_24() )
                            h_diff_dTheta_24.Fill( max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_24() - Trk1.DTheta_24()) ) )
                        if (Trk1.DTheta_34() != -999): 
                            h_Emu_vs_Unp_dTheta_34.Fill( Trk1.DTheta_34(), Trk2.DTheta_34() )
                            h_diff_dTheta_34.Fill( max(dTheta_bins[1]+0.01, min(dTheta_bins[2]-0.01, Trk2.DTheta_34() - Trk1.DTheta_34()) ) )


            if not unp_trk_matched:
                numTrksUnm[0] += 1
                if (nTrks2 > 0):
                    numTrksUnmExist[0] += 1
                    
       ## Check that emulator tracks have match in unpacker                                                                                                               
        for iTrk2 in range(nTrks2):
            Trk2 = Trks_2.at(iTrk2)
            if Trk2.BX() < -1 or Trk2.BX() > 1:
                continue
            if Trk2.BX() < 0 and bx_m3_hit_exists:
                continue
            if Trk2.BX() > 0 and bx_p3_hit_exists:
                continue
            if Trk2.Pt_GMT() == 0:
                continue

            numTrks[1] += 1
            emu_trk_matched = False
            for iTrk1 in range(nTrks1):
                Trk1 = Trks_1.at(iTrk1)
                if TracksMatch( Trk1, Trk2):
                    if Trk1.Eta_GMT() == Trk2.Eta_GMT() and Trk1.Phi_loc_int() == Trk2.Phi_loc_int() and Trk1.Mode() == Trk2.Mode():
                        emu_trk_matched = True

            if not emu_trk_matched:
                numTrksUnm[1] += 1
                if (nTrks1 > 0):
                    numTrksUnmExist[1] += 1


    print '*******************************************************'
    print '*******            The BIG picture              *******'
    print '*******************************************************'
    print '                       Unpacker    -  Emulator'
    print 'numHits:                %6d %11d' % (numHits[0], numHits[1]) 
    print 'numHitsUnm:             %6d %11d' % (numHitsUnm[0], numHitsUnm[1]) 
    print 'numHitsUnmExist:        %6d %11d' % (numHitsUnmExist[0], numHitsUnmExist[1]) 
    print 'numHitsUnmNonZeroWire:  %6d %11d' % (numHitsUnmNonZeroWire[0], numHitsUnmNonZeroWire[1]) 
    print 'numTrks:                %6d %11d' % (numTrks[0], numTrks[1]) 
    print 'numTrksUnm:             %6d %11d' % (numTrksUnm[0], numTrksUnm[1]) 
    print 'numTrksUnmExist:        %6d %11d' % (numTrksUnmExist[0], numTrksUnmExist[1]) 

    for iMode in range(16):
        if numTrksMatched[iMode] < 100:
            continue
        print ''
        print '*** Mode %d ***' % iMode
        print 'Variable   Exists   Corr.  Incorr.  Flipped'
        print 'LUT addr.  %4d    %4d    %4d    %4d' % ( numTrksMatched[iMode], numAddrCorr[iMode], numTrksMatched[iMode] - numAddrCorr[iMode], 0 )  
        print '  dPhi     %4d    %4d    %4d    %4d' % ( numDPhi[iMode], numDPhiCorr[iMode], numDPhiIncorr[iMode], numDPhiFlip[iMode] )  
        print ' dTheta    %4d    %4d    %4d    %4d' % ( numDTheta[iMode], numDThetaCorr[iMode], numDThetaIncorr[iMode], numDThetaFlip[iMode] )  
        print '  CLCT     %4d    %4d    %4d    %4d' % ( numCLCT[iMode], numCLCTCorr[iMode], numCLCTIncorr[iMode], numCLCTFlip[iMode] )  
        ## print '   FR      %4d    %4d    %4d    %4d' % ( numFR[iMode], numFRCorr[iMode], numFRIncorr[iMode], numFRFlip[iMode] )  

    print ''
    print '*** dPhi variables ***'
    for iPhi in range(6):
        if (iPhi == 0): dPhi_str = '1-2'
        if (iPhi == 1): dPhi_str = '1-3'
        if (iPhi == 2): dPhi_str = '1-4'
        if (iPhi == 3): dPhi_str = '2-3'
        if (iPhi == 4): dPhi_str = '2-4'
        if (iPhi == 5): dPhi_str = '3-4'
        print 'Stat.   Exists   Corr.  Incorr.  Flipped'
        print ' %s     %4d    %4d    %4d    %4d' % ( dPhi_str, numDphi[iPhi], numDphiCorr[iPhi], numDphiIncorr[iPhi], numDphiFlip[iPhi] )
        
    # print ''
    # print '*** FR variables ***'
    # for iSt in range(4):
    #     print 'Station   Exists   Corr.  Incorr.  Flipped'
    #     print '  %4d      %4d    %4d    %4d    %4d' % ( iSt+1, numFr[iSt+1], numFrCorr[iSt+1], numFrIncorr[iSt+1], numFrFlip[iSt+1] )
        

    out_file.cd()

    h_Emu_vs_Unp_dPhi_12.Write()  
    h_Emu_vs_Unp_dPhi_13.Write()  
    h_Emu_vs_Unp_dPhi_14.Write()  
    h_Emu_vs_Unp_dPhi_23.Write()  
    h_Emu_vs_Unp_dPhi_24.Write()  
    h_Emu_vs_Unp_dPhi_34.Write()  
    h_Emu_vs_Unp_dTheta_12.Write()  
    h_Emu_vs_Unp_dTheta_13.Write()  
    h_Emu_vs_Unp_dTheta_14.Write()  
    h_Emu_vs_Unp_dTheta_23.Write()  
    h_Emu_vs_Unp_dTheta_24.Write()  
    h_Emu_vs_Unp_dTheta_34.Write()  

    h_diff_dPhi_12.Write()  
    h_diff_dPhi_12_lowEtaP.Write()
    h_diff_dPhi_12_lowEtaM.Write()
    h_diff_dPhi_12_hiEtaP.Write()
    h_diff_dPhi_12_hiEtaM.Write()
    h_diff_dPhi_13.Write()  
    h_diff_dPhi_13_lowEtaP.Write()
    h_diff_dPhi_13_lowEtaM.Write()
    h_diff_dPhi_13_hiEtaP.Write()
    h_diff_dPhi_13_hiEtaM.Write()
    h_diff_dPhi_14.Write()  
    h_diff_dPhi_23.Write()  
    h_diff_dPhi_24.Write()  
    h_diff_dPhi_34.Write()  
    h_diff_dTheta_12.Write()  
    h_diff_dTheta_13.Write()  
    h_diff_dTheta_14.Write()  
    h_diff_dTheta_23.Write()  
    h_diff_dTheta_24.Write()  
    h_diff_dTheta_34.Write()  

    h_diff_dPhi_12_vs_mode.Write()  
    h_diff_dPhi_13_vs_mode.Write()  
    h_diff_dPhi_14_vs_mode.Write()  
    h_diff_dPhi_23_vs_mode.Write()  
    h_diff_dPhi_24_vs_mode.Write()  
    h_diff_dPhi_34_vs_mode.Write()  
    h_diff_dTheta_12_vs_mode.Write()  
    h_diff_dTheta_13_vs_mode.Write()  
    h_diff_dTheta_14_vs_mode.Write()  

    h_diff_dPhi_12_vs_eta.Write()  
    h_diff_dPhi_13_vs_eta.Write()  
    h_diff_dPhi_14_vs_eta.Write()  
    h_diff_dPhi_23_vs_eta.Write()  
    h_diff_dPhi_24_vs_eta.Write()  
    h_diff_dPhi_34_vs_eta.Write()  
    h_diff_dTheta_12_vs_eta.Write()  
    h_diff_dTheta_13_vs_eta.Write()  
    h_diff_dTheta_14_vs_eta.Write()  

    h_Emu_vs_Unp_pT_same_addr.Write()
    h_Emu_vs_Unp_pT_diff_addr.Write()

    out_file.Close()
    del tree
    file.Close()

if __name__ == '__main__':
    main()
