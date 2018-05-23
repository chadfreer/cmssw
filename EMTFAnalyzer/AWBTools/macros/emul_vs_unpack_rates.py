#! /usr/bin/env python

## Compare rates coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside emul_vs_unpack_rates'

    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272012_files_12.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272775_10k.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272775_1k_ME1_fix.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/ABCD.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/272798_124.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/272936_123.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936_thetaCorr2.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936.root'
    file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936_May_24_fix.root'
    out_file = TFile('plots/emul_vs_unpack_rates.root','recreate')

    tree_name = 'Events'

    file = TFile.Open(file_name)
    tree = file.Get(tree_name)

    eta_restricted = True

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
    SingleMu7 = {}
    SingleMu12 = {}
    SingleMu16 = {}
    DoubleMuOpenLeg = {}
    DoubleMu_0_Leg = {}
    DoubleMu_3p5_Leg = {}
    DoubleMu_5_Leg = {}
    DoubleMu_10_Leg = {}
    DoubleMu_12_Leg = {}

    numHits[0] = 0
    numHitsUnm[0] = 0
    numHitsUnmExist[0] = 0
    numHitsUnmNonZeroWire[0] = 0
    numTrks[0] = 0
    numTrksUnm[0] = 0
    numTrksUnmExist[0] = 0
    SingleMu7[0] = 0
    SingleMu12[0] = 0
    SingleMu16[0] = 0
    DoubleMuOpenLeg[0] = 0
    DoubleMu_0_Leg[0] = 0
    DoubleMu_3p5_Leg[0] = 0
    DoubleMu_5_Leg[0] = 0
    DoubleMu_10_Leg[0] = 0
    DoubleMu_12_Leg[0] = 0

    numHits[1] = 0
    numHitsUnm[1] = 0
    numHitsUnmExist[1] = 0
    numHitsUnmNonZeroWire[1] = 0
    numTrks[1] = 0
    numTrksUnm[1] = 0
    numTrksUnmExist[1] = 0
    SingleMu7[1] = 0
    SingleMu12[1] = 0
    SingleMu16[1] = 0
    DoubleMuOpenLeg[1] = 0
    DoubleMu_0_Leg[1] = 0
    DoubleMu_3p5_Leg[1] = 0
    DoubleMu_5_Leg[1] = 0
    DoubleMu_10_Leg[1] = 0
    DoubleMu_12_Leg[1] = 0

    ###################
    ### Book histograms
    ###################

    phi_bins = [40, -200, 200]
    eta_bins = [120, -300, 300]
    mode_bins = [16, -0.5, 15.5]
    pT_bins = [521,-0.5,520.5]

    h_phi_SingleMu16_unp = TH1D('h_phi_SingleMu16_unp', 'Data phi, pass SingleMu16', phi_bins[0], phi_bins[1], phi_bins[2])
    h_phi_SingleMu16_emu = TH1D('h_phi_SingleMu16_emu', 'Emul phi, pass SingleMu16', phi_bins[0], phi_bins[1], phi_bins[2])
    h_eta_SingleMu16_unp = TH1D('h_eta_SingleMu16_unp', 'Data eta, pass SingleMu16', eta_bins[0], eta_bins[1], eta_bins[2])
    h_eta_SingleMu16_emu = TH1D('h_eta_SingleMu16_emu', 'Emul eta, pass SingleMu16', eta_bins[0], eta_bins[1], eta_bins[2])
    h_mode_SingleMu16_unp = TH1D('h_mode_SingleMu16_unp', 'Data mode, pass SingleMu16', mode_bins[0], mode_bins[1], mode_bins[2])
    h_mode_SingleMu16_emu = TH1D('h_mode_SingleMu16_emu', 'Emul mode, pass SingleMu16', mode_bins[0], mode_bins[1], mode_bins[2])
    h_pT_SingleMu16_unp = TH1D('h_pT_SingleMu16_unp', 'Data pT, pass SingleMu16', pT_bins[0], pT_bins[1], pT_bins[2])
    h_pT_SingleMu16_emu = TH1D('h_pT_SingleMu16_emu', 'Emul pT, pass SingleMu16', pT_bins[0], pT_bins[1], pT_bins[2])

    ## Main event loop    
    for iEvt in range(tree.GetEntries()):
        
        ## if (iEvt > 10000): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt
        tree.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = tree.EventAuxiliary
        Hits_1 = tree.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        Trks_1 = tree.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        Hits_2 = tree.l1tEMTFHitExtras_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_2 = tree.l1tEMTFTrackExtras_simEmtfDigis_EMTF_L1TMuonEmulation
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        if (nHits1 == 0 and nHits2 == 0): continue

        # ######################################
        # ### Print out every hit in every event
        # ######################################

        # print 'Unpacker: %d hits and %d tracks in event %d' % ( nHits1, nTrks1, Event.event() )
        # for iHit1 in range(nHits1):
        #     Hit1 = Hits_1.at(iHit1)
        #     PrintEMTFHit( Hit1 )
            
        # print 'Emulator: %d hits and %d tracks in event %d' % ( nHits2, nTrks2, Event.event() )
        # for iHit2 in range(nHits2):
        #     Hit2 = Hits_2.at(iHit2)
        #     PrintEMTFHit( Hit2 )
        # continue


        #####################################################################################
        ### Compare hits in emulator and unpacker
        ###   * Emulator outputs all hits it received, whether or not a track was formed
        ###   * Unpacker outputs hits only in sectors with tracks (zero-suppression)
        ###   * Unpacker ouputs neighbor hits twice, and may build duplicate tracks with them
        #####################################################################################

        ## Check that unpacker hits have match in emulator
        unmatched_hit_exists = False
        neighbor_hit_exists = False
        bx_m3_hit_exists = False
        bx_p3_hit_exists = False
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            if Hit1.Neighbor() == 1:
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
            HitPhiInChamber( Hit2 )

            # emu_trk_in_sector = False
            # for iTrk2 in range(nTrks2):
            #     Trk2 = Trks_2.at(iTrk2)
            #     if Hit2.Endcap() == Trk2.Endcap() and Hit2.Sector() == Trk2.Sector(): 
            #         emu_trk_in_sector = True       
            # if not emu_trk_in_sector:  ## Remove hits in sectors without a track
            #     continue               ## Matches zero-suppression in firmware (but not neighbor analysis?!? - AWB 14.04.16)

            numHits[1] += 1
            emu_hit_matched = False
            for iHit1 in range(nHits1):
                Hit1 = Hits_1.at(iHit1)
                # if Hit1.Neighbor() == 1:
                #     continue
                if HitsMatch( Hit1, Hit2 ):
                    emu_hit_matched = True

            if not emu_hit_matched:
                unmatched_hit_exists = True
                numHitsUnm[1] += 1
                if nHits1 > 0:
                    numHitsUnmExist[1] += 1
                    if Hit2.Wire() != 0:
                        numHitsUnmNonZeroWire[1] += 1

        # ########################################
        # ### Print out every track in every event
        # ########################################

        # if (nTrks1 == 0 and nTrks2 == 0): continue
        # print 'Unpacker: %d tracks in event %d' % ( nTrks1, Event.event() )
        # for iTrk1 in range(nTrks1):
        #     Trk1 = Trks_1.at(iTrk1)
        #     PrintEMTFTrack( Trk1 )

        # print 'Emulator: %d tracks in event %d' % ( nTrks2, Event.event() )
        # for iTrk2 in range(nTrks2):
        #     Trk2 = Trks_2.at(iTrk2)
        #     PrintEMTFTrack( Trk2 )
        # print ''
        # continue

        #####################################################################################
        ### Compare tracks in emulator and unpacker
        ###   * Only compare if emulator and unpacker hits are identical
        #####################################################################################

        if unmatched_hit_exists:
            continue
        # if neighbor_hit_exists:
        #     continue
        if ( nTrks1 == 0 and nTrks2 == 0 ):
            continue

        SingleMu7_pass = False
        SingleMu12_pass = False
        SingleMu16_pass = False
        DoubleMuOpenLeg_pass = False
        DoubleMu_0_Leg_pass = False
        DoubleMu_3p5_Leg_pass = False
        DoubleMu_5_Leg_pass = False
        DoubleMu_10_Leg_pass = False
        DoubleMu_12_Leg_pass = False

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
            # if abs(Trk1.Eta()) > 1.5:
            #     continue

            ## Eta restriction for some DoubleMu modes
            ER = True
            if eta_restricted and (Trk1.Mode() == 10 or Trk1.Mode() == 12):
                ER = False
                # if abs(Trk1.Eta_GMT()) < 161 or abs(Trk1.Eta_GMT()) > 169:
                #     if abs(Trk1.Eta_GMT()) < 199 or abs(Trk1.Eta_GMT()) > 202:
                #         ER = False

            if (Trk1.Quality() >= 12 and Trk1.Pt() >= 7): 
                if not SingleMu7_pass: SingleMu7[0] += 1
                SingleMu7_pass = True
            if (Trk1.Quality() >= 12 and Trk1.Pt() >= 12): 
                if not SingleMu12_pass: SingleMu12[0] += 1
                SingleMu12_pass = True
            if (Trk1.Quality() >= 12 and Trk1.Pt() >= 16): 
                if not SingleMu16_pass: SingleMu16[0] += 1
                SingleMu16_pass = True
                h_phi_SingleMu16_unp.Fill( Trk1.Phi_glob_deg() )
                h_eta_SingleMu16_unp.Fill( Trk1.Eta_GMT() )
                h_mode_SingleMu16_unp.Fill( Trk1.Mode() )
                h_pT_SingleMu16_unp.Fill( min(Trk1.Pt_GMT(), pT_bins[2]-0.01) )
            if (Trk1.Quality() >= 4) and ER: 
                if not DoubleMuOpenLeg_pass: DoubleMuOpenLeg[0] += 1
                DoubleMuOpenLeg_pass = True
            if (Trk1.Quality() >= 8 and Trk1.Pt() >= 0) and ER:
                if not DoubleMu_0_Leg_pass: DoubleMu_0_Leg[0] += 1
                DoubleMu_0_Leg_pass = True
            if (Trk1.Quality() >= 8 and Trk1.Pt() >= 3.5) and ER: 
                if not DoubleMu_3p5_Leg_pass: DoubleMu_3p5_Leg[0] += 1
                DoubleMu_3p5_Leg_pass = True
            if (Trk1.Quality() >= 8 and Trk1.Pt() >= 5) and ER: 
                if not DoubleMu_5_Leg_pass: DoubleMu_5_Leg[0] += 1
                DoubleMu_5_Leg_pass = True
            if (Trk1.Quality() >= 8 and Trk1.Pt() >= 10) and ER: 
                if not DoubleMu_10_Leg_pass: DoubleMu_10_Leg[0] += 1
                DoubleMu_10_Leg_pass = True
            if (Trk1.Quality() >= 8 and Trk1.Pt() >= 12) and ER: 
                if not DoubleMu_12_Leg_pass: DoubleMu_12_Leg[0] += 1
                DoubleMu_12_Leg_pass = True

            numTrks[0] += 1
            unp_trk_matched = False
            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)

                if TracksMatch( Trk1, Trk2 ):
                    unp_trk_matched = True

            if not unp_trk_matched:
                numTrksUnm[0] += 1
                if (nTrks2 > 0):
                    numTrksUnmExist[0] += 1

                    
        Unp_SingleMu16_pass = False
        if SingleMu16_pass:
            Unp_SingleMu16_pass = True

        SingleMu7_pass = False
        SingleMu12_pass = False
        SingleMu16_pass = False
        DoubleMuOpenLeg_pass = False
        DoubleMu_0_Leg_pass = False
        DoubleMu_3p5_Leg_pass = False
        DoubleMu_5_Leg_pass = False
        DoubleMu_10_Leg_pass = False
        DoubleMu_12_Leg_pass = False

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
            # if abs(Trk2.Eta()) > 1.5:
            #     continue

            ## Eta restriction for some DoubleMu modes
            ER = True
            if eta_restricted and (Trk2.Mode() == 10 or Trk2.Mode() == 12):
                ER = False
                # if abs(Trk2.Eta_GMT()) < 161 or abs(Trk2.Eta_GMT()) > 169:
                #     if abs(Trk2.Eta_GMT()) < 199 or abs(Trk2.Eta_GMT()) > 202:
                #         ER = False

            if (Trk2.Quality() >= 12 and Trk2.Pt() >= 7): 
                if not SingleMu7_pass: SingleMu7[1] += 1
                SingleMu7_pass = True
            if (Trk2.Quality() >= 12 and Trk2.Pt() >= 12): 
                if not SingleMu12_pass: SingleMu12[1] += 1
                SingleMu12_pass = True
            if (Trk2.Quality() >= 12 and Trk2.Pt() >= 16): 
                if not SingleMu16_pass: SingleMu16[1] += 1
                SingleMu16_pass = True
                h_phi_SingleMu16_emu.Fill( Trk2.Phi_glob_deg() )
                h_eta_SingleMu16_emu.Fill( Trk2.Eta_GMT() )
                h_mode_SingleMu16_emu.Fill( Trk2.Mode() )
                h_pT_SingleMu16_emu.Fill( min(Trk2.Pt_GMT(), pT_bins[2]-0.01) )
            if (Trk2.Quality() >= 4): 
                if not DoubleMuOpenLeg_pass: DoubleMuOpenLeg[1] += 1
                DoubleMuOpenLeg_pass = True
            if (Trk2.Quality() >= 8 and Trk2.Pt() >= 0) and ER: 
                if not DoubleMu_0_Leg_pass: DoubleMu_0_Leg[1] += 1
                DoubleMu_0_Leg_pass = True
            if (Trk2.Quality() >= 8 and Trk2.Pt() >= 3.5) and ER: 
                if not DoubleMu_3p5_Leg_pass: DoubleMu_3p5_Leg[1] += 1
                DoubleMu_3p5_Leg_pass = True
            if (Trk2.Quality() >= 8 and Trk2.Pt() >= 5) and ER: 
                if not DoubleMu_5_Leg_pass: DoubleMu_5_Leg[1] += 1
                DoubleMu_5_Leg_pass = True
            if (Trk2.Quality() >= 8 and Trk2.Pt() >= 10) and ER: 
                if not DoubleMu_10_Leg_pass: DoubleMu_10_Leg[1] += 1
                DoubleMu_10_Leg_pass = True
            if (Trk2.Quality() >= 8 and Trk2.Pt() >= 12) and ER: 
                if not DoubleMu_12_Leg_pass: DoubleMu_12_Leg[1] += 1
                DoubleMu_12_Leg_pass = True

            numTrks[1] += 1
            emu_trk_matched = False
            for iTrk1 in range(nTrks1):
                Trk1 = Trks_1.at(iTrk1)
                if TracksMatch( Trk1, Trk2 ):
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


    print '***************************************************************************'
    print '*******                   EMTF rates: run 272936                    *******'
    print '***************************************************************************'
    print '                  Unpacker   -   Emulator - Unp. frac. x 1000000 - Unp./Emu. ratio'
    print 'Number of events   %7d        %7d          %7d            %.2f'  % (iEvt, iEvt, 1000000, 1)
    print 'SingleMu7          %7d        %7d          %7d            %.2f'  % (SingleMu7[0], SingleMu7[1], 1000000*SingleMu7[0]/iEvt, 1.0*SingleMu7[0]/SingleMu7[1]) 
    print 'SingleMu12         %7d        %7d          %7d            %.2f'  % (SingleMu12[0], SingleMu12[1], 1000000*SingleMu12[0]/iEvt, 1.0*SingleMu12[0]/SingleMu12[1]) 
    print 'SingleMu16         %7d        %7d          %7d            %.2f'  % (SingleMu16[0], SingleMu16[1], 1000000*SingleMu16[0]/iEvt, 1.0*SingleMu16[0]/SingleMu16[1]) 
    print 'DoubleMuOpen       %7d        %7d          %7d            %.2f'  % (DoubleMuOpenLeg[0], DoubleMuOpenLeg[1], 1000000*DoubleMuOpenLeg[0]/iEvt, 1.0*DoubleMuOpenLeg[0]/DoubleMuOpenLeg[1]) 
    print 'DoubleMu0          %7d        %7d          %7d            %.2f'  % (DoubleMu_0_Leg[0], DoubleMu_0_Leg[1], 1000000*DoubleMu_0_Leg[0]/iEvt, 1.0*DoubleMu_0_Leg[0]/DoubleMu_0_Leg[1]) 
    print 'DoubleMu_3p5_Leg    %7d        %7d          %7d            %.2f'  % (DoubleMu_3p5_Leg[0], DoubleMu_3p5_Leg[1], 1000000*DoubleMu_3p5_Leg[0]/iEvt, 1.0*DoubleMu_3p5_Leg[0]/DoubleMu_3p5_Leg[1]) 
    print 'DoubleMu_5_Leg      %7d        %7d          %7d            %.2f'  % (DoubleMu_5_Leg[0], DoubleMu_5_Leg[1], 1000000*DoubleMu_5_Leg[0]/iEvt, 1.0*DoubleMu_5_Leg[0]/DoubleMu_5_Leg[1]) 
    print 'DoubleMu_10_Leg   %7d        %7d          %7d            %.2f'  % (DoubleMu_10_Leg[0], DoubleMu_10_Leg[1], 1000000*DoubleMu_10_Leg[0]/iEvt, 1.0*DoubleMu_10_Leg[0]/DoubleMu_10_Leg[1]) 
    print 'DoubleMu_12_Leg   %7d        %7d          %7d            %.2f'  % (DoubleMu_12_Leg[0], DoubleMu_12_Leg[1], 1000000*DoubleMu_12_Leg[0]/iEvt, 1.0*DoubleMu_12_Leg[0]/DoubleMu_12_Leg[1]) 


    out_file.cd()

    h_phi_SingleMu16_unp.SetLineWidth(2)
    h_phi_SingleMu16_unp.SetLineColor(kBlack)
    h_phi_SingleMu16_unp.Write()
    h_phi_SingleMu16_emu.SetLineWidth(2)
    h_phi_SingleMu16_emu.SetLineColor(kRed)
    h_phi_SingleMu16_emu.Write()
    h_eta_SingleMu16_unp.SetLineWidth(2)
    h_eta_SingleMu16_unp.SetLineColor(kBlack)
    h_eta_SingleMu16_unp.Write()
    h_eta_SingleMu16_emu.SetLineWidth(2)
    h_eta_SingleMu16_emu.SetLineColor(kRed)
    h_eta_SingleMu16_emu.Write()
    h_mode_SingleMu16_unp.SetLineWidth(2)
    h_mode_SingleMu16_unp.SetLineColor(kBlack)
    h_mode_SingleMu16_unp.Write()
    h_mode_SingleMu16_emu.SetLineWidth(2)
    h_mode_SingleMu16_emu.SetLineColor(kRed)
    h_mode_SingleMu16_emu.Write()
    h_pT_SingleMu16_unp.SetLineWidth(2)
    h_pT_SingleMu16_unp.SetLineColor(kBlack)
    h_pT_SingleMu16_unp.Write()
    h_pT_SingleMu16_emu.SetLineWidth(2)
    h_pT_SingleMu16_emu.SetLineColor(kRed)
    h_pT_SingleMu16_emu.Write()

    out_file.Close()
    del tree
    file.Close()

if __name__ == '__main__':
    main()
