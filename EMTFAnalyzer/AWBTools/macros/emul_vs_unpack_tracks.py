#! /usr/bin/env python

## Compare tracks coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside emul_vs_unpack_tracks'

    # # file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936.root'
    # file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936_May_24_fix.root'
    file_name_1 = '/afs/cern.ch/user/a/abrinke1/EmuPull_809/CMSSW_8_0_9/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_274157_10k_git.root'
    file_name_2 = '/afs/cern.ch/user/a/abrinke1/EmuPull_809/CMSSW_8_0_9/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_274157_10k_theta_fix.root'

    out_file = TFile('plots/emul_vs_unpack_tracks.root','recreate')

    tree_name = 'Events'

    # file = TFile.Open(file_name)
    # tree = file.Get(tree_name)
    file_1 = TFile.Open(file_name_1)
    tree_1 = file_1.Get(tree_name)
    file_2 = TFile.Open(file_name_2)
    tree_2 = file_2.Get(tree_name)

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

    ###################
    ### Book histograms
    ###################

    BX_bins = [6, -3.5, 2.5]
    pT_bins = [32, -1.5, 30.5]
    dPt_bins = [81, -20.25, 20.25]
    phi_bins = [100, -200, 200]
    eta_bins = [60, -3.0, 3.0]
    ## phi_GMT_bins = [102, -1.5, 100.5]
    ## eta_GMT_bins = [501, -250.5, 250.5]
    mode_bins = [18, -1.5, 16.5]
    ## evt_bins = [10001,-0.5,10000.5]

    h_BX = TH1D('h_BX', 'Emu. & Unp. BX', BX_bins[0], BX_bins[1], BX_bins[2])
    ## h_pT = TH1D('h_pT', 'Emu. & Unp. pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_phi = TH1D('h_phi', 'Emu. & Unp. phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_eta = TH1D('h_eta', 'Emu. & Unp. eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_mode = TH1D('h_mode', 'Emu. & Unp. mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_evt = TH1D('h_evt', 'Emu. & Unp. evt', evt_bins[0], evt_bins[1], evt_bins[2])
    h_dPt_same_mode = TH1D('h_dPt_same_mode', 'Emu. - Unp. pT, same mode', dPt_bins[0], dPt_bins[1], dPt_bins[2])
    h_dPt_diff_mode = TH1D('h_dPt_diff_mode', 'Emu. - Unp. pT, diff. mode', dPt_bins[0], dPt_bins[1], dPt_bins[2])

    h_Unp_BX = TH1D('h_Unp_BX', 'Unpacker BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_Unp_pT = TH1D('h_Unp_pT', 'Unpacker pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_Unp_phi = TH1D('h_Unp_phi', 'Unpacker phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_Unp_eta = TH1D('h_Unp_eta', 'Unpacker eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_Unp_mode = TH1D('h_Unp_mode', 'Unpacker mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_Unp_evt = TH1D('h_Unp_evt', 'Unpacker evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_Unp_only_BX = TH1D('h_Unp_only_BX', 'Unpacker-only BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_Unp_only_pT = TH1D('h_Unp_only_pT', 'Unpacker-only pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_Unp_only_phi = TH1D('h_Unp_only_phi', 'Unpacker-only phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_Unp_only_eta = TH1D('h_Unp_only_eta', 'Unpacker-only eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_Unp_only_mode = TH1D('h_Unp_only_mode', 'Unpacker-only mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_Unp_only_evt = TH1D('h_Unp_only_evt', 'Unpacker-only evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_Emu_BX = TH1D('h_Emu_BX', 'Emulator BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_Emu_pT = TH1D('h_Emu_pT', 'Emulator pT', pT_bins[0], pT_bins[1], pT_bins[2]) 
    h_Emu_phi = TH1D('h_Emu_phi', 'Emulator phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_Emu_eta = TH1D('h_Emu_eta', 'Emulator eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_Emu_mode = TH1D('h_Emu_mode', 'Emulator mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_Emu_evt = TH1D('h_Emu_evt', 'Emulator evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_Emu_only_BX = TH1D('h_Emu_only_BX', 'Emulator-only BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_Emu_only_pT = TH1D('h_Emu_only_pT', 'Emulator-only pT', pT_bins[0], pT_bins[1], pT_bins[2]) 
    h_Emu_only_phi = TH1D('h_Emu_only_phi', 'Emulator-only phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_Emu_only_eta = TH1D('h_Emu_only_eta', 'Emulator-only eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_Emu_only_mode = TH1D('h_Emu_only_mode', 'Emulator-only mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_Emu_only_evt = TH1D('h_Emu_only_evt', 'Emulator-only evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_Emu_vs_Unp_BX = TH2D('h_Emu_vs_Unp_BX', 'Emulator vs. Unpacker BX', BX_bins[0], BX_bins[1], BX_bins[2], BX_bins[0], BX_bins[1], BX_bins[2])
    h_Emu_vs_Unp_pT = TH2D('h_Emu_vs_Unp_pT', 'Emulator vs. Unpacker pT', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_Emu_vs_Unp_mode = TH2D('h_Emu_vs_Unp_mode', 'Emulator vs. Unpacker mode', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_dEta_vs_dPhi = TH2D('h_dEta_vs_dPhi', 'Emulator - Unpacker dEta vs. dPhi', 19, -9.5, 9.5, 19, -9.5, 9.5)
    h_dEta_vs_eta = TH2D('h_dEta_vs_eta', 'Emulator - Unpacker dEta vs. Eta', eta_bins[0], eta_bins[1], eta_bins[2], 19, -9.5, 9.5)
    h_dEta_vs_mode = TH2D('h_dEta_vs_mode', 'Emulator - Unpacker dEta vs. Mode', mode_bins[0], mode_bins[1], mode_bins[2], 19, -9.5, 9.5)

    h_Emu_vs_Unp_pT_lowEta = TH2D('h_Emu_vs_Unp_pT_lowEta', 'Emulator vs. Unpacker pT, |eta| < 1.5', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_Emu_vs_Unp_mode_lowEta = TH2D('h_Emu_vs_Unp_mode_lowEta', 'Emulator vs. Unpacker mode, |eta| < 1.5', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_dEta_vs_dPhi_lowEta = TH2D('h_dEta_vs_dPhi_lowEta', 'Emulator - Unpacker dEta vs. dPhi, |eta| < 1.5', 19, -9.5, 9.5, 19, -9.5, 9.5)
    h_Emu_vs_Unp_pT_hiEta = TH2D('h_Emu_vs_Unp_pT_hiEta', 'Emulator vs. Unpacker pT, |eta| > 1.5', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_Emu_vs_Unp_mode_hiEta = TH2D('h_Emu_vs_Unp_mode_hiEta', 'Emulator vs. Unpacker mode, |eta| > 1.5', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_dEta_vs_dPhi_hiEta = TH2D('h_dEta_vs_dPhi_hiEta', 'Emulator - Unpacker dEta vs. dPhi, |eta| < 1.5', 19, -9.5, 9.5, 19, -9.5, 9.5)

    ## h_Emu_vs_Unp_phi = TH2D('h_Emu_vs_Unp_phi', 'Emulator vs. Unpacker phi', phi_bins[0], phi_bins[1], phi_bins[2], phi_bins[0], phi_bins[1], phi_bins[2])
    ## h_Emu_vs_Unp_eta = TH2D('h_Emu_vs_Unp_eta', 'Emulator vs. Unpacker eta', eta_bins[0], eta_bins[1], eta_bins[2], eta_bins[0], eta_bins[1], eta_bins[2])

    ## Main event loop    
    # for iEvt in range(tree.GetEntries()):
    for iEvt in range(tree_1.GetEntries()):
        
        if (iEvt > 100000): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt
        # tree.GetEntry(iEvt)
        tree_1.GetEntry(iEvt)
        tree_2.GetEntry(iEvt)

        ## Get branches from the trees
        # Event  = tree.EventAuxiliary
        # Hits_1 = tree.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        # Trks_1 = tree.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        # Hits_2 = tree.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        # Trks_2 = tree.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation
        
        Event  = tree_1.EventAuxiliary
        Hits_1 = tree_1.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_1 = tree_1.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation
        Hits_2 = tree_2.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_2 = tree_2.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        # if (nHits1 == 0 and nHits2 == 0): continue

        # ######################################
        # ### Print out every hit in every event
        # ######################################

        # print 'Unpacker: %d hits and %d tracks in event %d' % ( nHits1, nTrks1, Event.event() )
        # for iHit1 in range(nHits1):
        #     Hit1 = Hits_1.at(iHit1)
        #     print 'BX = %d, station = %d, sector = %d, ' % ( Hit1.BX(), Hit1.Station(), Hit1.Sector() ), \
        #         'CSC ID = %d, strip = %d, wire = %d, neighbor = %d' % ( Hit1.CSC_ID(), Hit1.Strip(), Hit1.Wire(), Hit1.Neighbor() )
            
        # print 'Emulator: %d hits and %d tracks in event %d' % ( nHits2, nTrks2, Event.event() )
        # for iHit2 in range(nHits2):
        #     Hit2 = Hits_2.at(iHit2)
        #     print 'BX = %d, station = %d, sector = %d, ' % ( Hit2.BX(), Hit2.Station(), Hit2.Sector() ), \
        #         'CSC ID = %d, strip = %d, wire = %d, nTrks = %d' % ( Hit2.CSC_ID(), Hit2.Strip(), Hit2.Wire(), nTrks2 )
        #     ## if (nTrks2 > 0 or nHits1 > 0):
        #     ## if Hit2.Eta() < -5:
        #     ## if Hit2.Ring() < 0 or Hit2.Ring() > 3:
        #         # print 'BX = %d, station = %d, sector = %d, subsector = %d, ' % ( Hit2.BX(), Hit2.Station(), Hit2.Sector(),  Hit2.Subsector() ), \
        #         #     'ring = %d, CSC ID = %d, chamber = %d, strip = %d, wire = %d, ' % ( Hit2.Ring(), Hit2.CSC_ID(), Hit2.Chamber(), Hit2.Strip(), Hit2.Wire() ), \
        #         #     'eta = %.3f, theta_deg = %.3f, phi_glob_deg = %.3f' % ( Hit2.Eta(), Hit2.Theta_deg(), Hit2.Phi_glob_deg() )
        # continue


        #####################################################################################
        ### Compare hits in emulator and unpacker
        ###   * Emulator outputs all hits it received, whether or not a track was formed
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

        # ########################################
        # ### Print out every track in every event
        # ########################################

        # if (nTrks1 == 0 and nTrks2 == 0): continue
        # print 'Unpacker: %d tracks in event %d' % ( nTrks1, Event.event() )
        # for iTrk1 in range(nTrks1):
        #     Trk1 = Trks_1.at(iTrk1)
        #     has_neighbor = 0
        #     all_neighbor = 0
        #     ## Check if some (or all) of the hits in the track are from a neighboring sector
        #     if ( Trk1.ME1_neighbor() == 1 or Trk1.ME2_neighbor() == 1 or Trk1.ME3_neighbor() == 1 or Trk1.ME4_neighbor() == 1 ): has_neighbor = 1
        #     if ( Trk1.ME1_neighbor() != 0 and Trk1.ME2_neighbor() != 0 and Trk1.ME3_neighbor() != 0 and Trk1.ME4_neighbor() != 0 ): all_neighbor = 1
        #     ## if ( all_neighbor == 1 ): continue  
        #     print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk1.BX(), Trk1.Sector(), Trk1.Mode(), Trk1.Eta() ), \
        #         'phi = %d, pT = %d, has some (all) neighbor hits = %d (%d)' % ( Trk1.Phi(), ((Trk1.Pt_GMT()/2.0) - 0.5), has_neighbor, all_neighbor )

        # print 'Emulator: %d tracks in event %d' % ( nTrks2, Event.event() )
        # for iTrk2 in range(nTrks2):
        #     Trk2 = Trks_2.at(iTrk2)
        #     print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk2.BX(), Trk2.Sector(), Trk2.Mode(), Trk2.Eta() ), \
        #         'phi = %d, pT = %d' % ( Trk2.Phi(), ((Trk2.Pt_GMT()/2.0) - 0.5)  )
        # print ''
        # continue


        #####################################################################################
        ### Compare tracks in emulator and unpacker
        ###   * Only compare if emulator and unpacker hits are identical
        #####################################################################################

        # if unmatched_hit_exists:
        #     continue
        # # if neighbor_hit_exists:
        # #     continue
        # if ( nTrks1 == 0 and nTrks2 == 0 ):
        #     continue
        # # if ( nTrks1 > 2 or nTrks2 > 2 ):
        # #     continue

        ## Check that unpacker tracks have match in emulator
        for iTrk1 in range(nTrks1):
            Trk1 = Trks_1.at(iTrk1)
            if Trk1.BX() < -1 or Trk1.BX() > 1:
                continue
            if Trk1.BX() < 0 and bx_m3_hit_exists:
                continue
            if Trk1.BX() > 0 and bx_p3_hit_exists:
                continue
            # if Trk1.Pt_GMT() == 0:
            #     continue
            # if Trk1.All_neighbor() == 1:
            #     continue
            # if Trk1.Has_neighbor() == 0:
            #     continue
            # if abs(Trk1.Eta()) < 1.5:
            #     continue

            numTrks[0] += 1
            unp_trk_matched = False

            h_Unp_BX.Fill( Trk1.BX() )
            h_Unp_mode.Fill( Trk1.Mode() )
            h_Unp_eta.Fill( Trk1.Eta() )
            h_Unp_phi.Fill( Trk1.Phi_glob_deg() )
            h_Unp_pT.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )

            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)
                if TracksMatch( Trk1, Trk2 ):
                    unp_trk_matched = True

                    if ( Trk1.Mode() == Trk2.Mode() and Trk1.Quality() > 11 and abs(Trk1.Pt() - Trk2.Pt()) > 10 and min(Trk1.Pt(), Trk2.Pt()) < 10 ):
                        print '*************** Event %d ********************' % Event.event()

                        print 'Unpacker track: '
                        PrintEMTFTrack( Trk1 )
                        PrintPtLUT( Trk1 )
                        # print 'Unpacker tracks: '
                        # for iTrk1 in range(nTrks1):
                        #     Trk1 = Trks_1.at(iTrk1)
                        #     PrintEMTFTrack( Trk1 )
                        #     PrintPtLUT( Trk1 )
                        
                        # print 'Unpacked hits:'
                        # for iHit1 in range(nHits1):
                        #     Hit1 = Hits_1.at(iHit1)
                        #     PrintEMTFHit( Hit1 )
                    
                        print 'Emulator track: '
                        PrintEMTFTrack( Trk2 )
                        PrintPtLUT( Trk2 )
                        # print 'Emulator tracks: '
                        # for iTrk2 in range(nTrks2):
                        #     Trk2 = Trks_2.at(iTrk2)
                        #     PrintEMTFTrack( Trk2 )
                        #     PrintPtLUT( Trk2 )

                        print 'Emulator hits:'
                        for iHit2 in range(nHits2):
                            Hit2 = Hits_2.at(iHit2)
                            PrintEMTFHitExtra( Hit2 )
                            
                        PrintSimulatorHitHeader()
                        for iHit2 in range(nHits2):
                            Hit2 = Hits_2.at(iHit2)
                            PrintSimulatorHit( Hit2 )

                        print '******************************************'
                        print ''

                    h_Emu_vs_Unp_BX.Fill( Trk1.BX(), Trk2.BX() )
                    h_Emu_vs_Unp_mode.Fill( Trk1.Mode(), Trk2.Mode() )
                    h_dEta_vs_dPhi.Fill( Trk2.Phi_GMT() - Trk1.Phi_GMT(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                    h_dEta_vs_eta.Fill( Trk1.Eta(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                    h_dEta_vs_mode.Fill( Trk1.Mode(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )

                    h_eta.Fill( Trk1.Eta() )
                    h_phi.Fill( Trk1.Phi_glob_deg() )
                    if ( Trk1.BX() == Trk2.BX() ):
                        h_BX.Fill( Trk1.BX() )
                    if ( Trk1.Mode() == Trk2.Mode() ):
                        h_mode.Fill( Trk1.Mode() )
                        h_Emu_vs_Unp_pT.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2]-0.01), min( ((Trk2.Pt_GMT()/2.0) - 0.5) , pT_bins[2]-0.01) )
                        h_dPt_same_mode.Fill( max(dPt_bins[1]+0.01, min(dPt_bins[2]-0.01, ((Trk2.Pt_GMT()/2.0) - 0.5)  - ((Trk1.Pt_GMT()/2.0) - 0.5) ) ) )
                    else:
                        h_dPt_diff_mode.Fill( max(dPt_bins[1]+0.01, min(dPt_bins[2]-0.01, ((Trk2.Pt_GMT()/2.0) - 0.5)  - ((Trk1.Pt_GMT()/2.0) - 0.5) ) ) )

                    if ( abs(Trk1.Eta()) < 1.5 ):
                        h_Emu_vs_Unp_mode_lowEta.Fill( Trk1.Mode(), Trk2.Mode() )
                        h_dEta_vs_dPhi_lowEta.Fill( Trk2.Phi_GMT() - Trk1.Phi_GMT(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                        if ( Trk1.Mode() == Trk2.Mode() ):
                            h_Emu_vs_Unp_pT_lowEta.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2]-0.01), min( ((Trk2.Pt_GMT()/2.0) - 0.5) , pT_bins[2]-0.01) )
                    else:
                        h_Emu_vs_Unp_mode_hiEta.Fill( Trk1.Mode(), Trk2.Mode() )
                        h_dEta_vs_dPhi_hiEta.Fill( Trk2.Phi_GMT() - Trk1.Phi_GMT(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                        if ( Trk1.Mode() == Trk2.Mode() ):
                            h_Emu_vs_Unp_pT_hiEta.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2]-0.01), min( ((Trk2.Pt_GMT()/2.0) - 0.5) , pT_bins[2]-0.01) )

                            
            if not unp_trk_matched:
                numTrksUnm[0] += 1
                h_Unp_only_BX.Fill( Trk1.BX() )
                h_Unp_only_mode.Fill( Trk1.Mode() )
                h_Unp_only_eta.Fill( Trk1.Eta() )
                h_Unp_only_phi.Fill( Trk1.Phi_glob_deg() )
                h_Unp_only_pT.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )
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
            # if Trk2.Pt_GMT() == 0:
            #     continue
            # if abs(Trk2.Eta()) < 1.5:
            #     continue

            numTrks[1] += 1

            h_Emu_BX.Fill( Trk2.BX() )
            h_Emu_mode.Fill( Trk2.Mode() )
            h_Emu_eta.Fill( Trk2.Eta() )
            h_Emu_phi.Fill( Trk2.Phi_glob_deg() )
            h_Emu_pT.Fill( min( ((Trk2.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )

            emu_trk_matched = False
            for iTrk1 in range(nTrks1):
                Trk1 = Trks_1.at(iTrk1)
                if TracksMatch( Trk1, Trk2 ):
                    emu_trk_matched = True

            if not emu_trk_matched:
                numTrksUnm[1] += 1
                h_Emu_only_BX.Fill( Trk2.BX() )
                h_Emu_only_mode.Fill( Trk2.Mode() )
                h_Emu_only_eta.Fill( Trk2.Eta() )
                h_Emu_only_phi.Fill( Trk2.Phi_glob_deg() )
                h_Emu_only_pT.Fill( min( ((Trk2.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )
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


    out_file.cd()

    h_BX.GetXaxis().SetTitle('BX')
    h_BX.Write()
    # h_pT.GetXaxis().SetTitle('pT')
    # h_pT.Write()
    h_dPt_same_mode.GetXaxis().SetTitle('Emu. - Unp. pT')
    h_dPt_same_mode.Write()
    h_dPt_diff_mode.GetXaxis().SetTitle('Emu. - Unp. pT')
    h_dPt_diff_mode.Write()
    h_phi.GetXaxis().SetTitle('phi')
    h_phi.Write()
    h_eta.GetXaxis().SetTitle('eta')
    h_eta.Write()
    h_mode.GetXaxis().SetTitle('Mode')
    h_mode.Write()
    # h_evt.GetXaxis().SetTitle('iEvt')
    # h_evt.Write()

    h_Unp_BX.GetXaxis().SetTitle('BX')
    h_Unp_BX.Write()
    h_Unp_pT.GetXaxis().SetTitle('pT')
    h_Unp_pT.SetLineWidth(2)
    h_Unp_pT.SetLineColor(kBlue)
    h_Unp_pT.Write()
    h_Unp_phi.GetXaxis().SetTitle('phi')
    h_Unp_phi.SetLineWidth(2)
    h_Unp_phi.SetLineColor(kBlue)
    h_Unp_phi.Write()
    h_Unp_eta.GetXaxis().SetTitle('eta')
    h_Unp_eta.SetLineWidth(2)
    h_Unp_eta.SetLineColor(kBlue)
    h_Unp_eta.Write()
    h_Unp_mode.GetXaxis().SetTitle('Mode')
    h_Unp_mode.SetLineWidth(2)
    h_Unp_mode.SetLineColor(kBlue)
    h_Unp_mode.Write()
    # h_Unp_evt.GetXaxis().SetTitle('iEvt')
    # h_Unp_evt.Write()

    h_Emu_BX.GetXaxis().SetTitle('BX')
    h_Emu_BX.Write()
    h_Emu_pT.GetXaxis().SetTitle('pT')
    h_Emu_pT.SetLineWidth(2)
    h_Emu_pT.SetLineColor(kRed)
    h_Emu_pT.Write()
    h_Emu_phi.GetXaxis().SetTitle('phi')
    h_Emu_phi.SetLineWidth(2)
    h_Emu_phi.SetLineColor(kRed)
    h_Emu_phi.Write()
    h_Emu_eta.GetXaxis().SetTitle('eta')
    h_Emu_eta.SetLineWidth(2)
    h_Emu_eta.SetLineColor(kRed)
    h_Emu_eta.Write()
    h_Emu_mode.GetXaxis().SetTitle('Mode')
    h_Emu_mode.SetLineWidth(2)
    h_Emu_mode.SetLineColor(kRed)
    h_Emu_mode.Write()
    # h_Emu_evt.GetXaxis().SetTitle('iEvt')
    # h_Emu_evt.Write()

    h_Unp_only_BX.GetXaxis().SetTitle('BX')
    h_Unp_only_BX.Write()
    h_Unp_only_pT.GetXaxis().SetTitle('pT')
    h_Unp_only_pT.Write()
    h_Unp_only_phi.GetXaxis().SetTitle('phi')
    h_Unp_only_phi.Write()
    h_Unp_only_eta.GetXaxis().SetTitle('eta')
    h_Unp_only_eta.Write()
    h_Unp_only_mode.GetXaxis().SetTitle('Mode')
    h_Unp_only_mode.Write()
    # h_Unp_evt.GetXaxis().SetTitle('iEvt')
    # h_Unp_evt.Write()

    h_Emu_only_BX.GetXaxis().SetTitle('BX')
    h_Emu_only_BX.Write()
    h_Emu_only_pT.GetXaxis().SetTitle('pT')
    h_Emu_only_pT.Write()
    h_Emu_only_phi.GetXaxis().SetTitle('phi')
    h_Emu_only_phi.Write()
    h_Emu_only_eta.GetXaxis().SetTitle('eta')
    h_Emu_only_eta.Write()
    h_Emu_only_mode.GetXaxis().SetTitle('Mode')
    h_Emu_only_mode.Write()
    # h_Emu_evt.GetXaxis().SetTitle('iEvt')
    # h_Emu_evt.Write()

    h_Emu_vs_Unp_BX.GetXaxis().SetTitle('Unpacker BX')
    h_Emu_vs_Unp_BX.GetYaxis().SetTitle('Emulator BX')
    h_Emu_vs_Unp_BX.SetMarkerSize(1.5)
    h_Emu_vs_Unp_BX.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_BX.Write()
    h_Emu_vs_Unp_pT.GetXaxis().SetTitle('Unpacker pT')
    h_Emu_vs_Unp_pT.GetYaxis().SetTitle('Emulator pT')
    h_Emu_vs_Unp_pT.SetMarkerSize(1.5)
    h_Emu_vs_Unp_pT.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_pT.Write()
    # h_Emu_vs_Unp_phi.GetXaxis().SetTitle('Unpacker phi')
    # h_Emu_vs_Unp_phi.GetYaxis().SetTitle('Emulator phi')
    # h_Emu_vs_Unp_phi.SetMarkerSize(1.5)
    # h_Emu_vs_Unp_phi.SetMarkerColor(kWhite)
    # h_Emu_vs_Unp_phi.Write()
    # h_Emu_vs_Unp_eta.GetXaxis().SetTitle('Unpacker eta')
    # h_Emu_vs_Unp_eta.GetYaxis().SetTitle('Emulator eta')
    # h_Emu_vs_Unp_eta.SetMarkerSize(1.5)
    # h_Emu_vs_Unp_eta.SetMarkerColor(kWhite)
    # h_Emu_vs_Unp_eta.Write()
    h_Emu_vs_Unp_mode.GetXaxis().SetTitle('Unpacker mode')
    h_Emu_vs_Unp_mode.GetYaxis().SetTitle('Emulator mode')
    h_Emu_vs_Unp_mode.SetMarkerSize(1.5)
    h_Emu_vs_Unp_mode.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_mode.Write()
    h_dEta_vs_dPhi.GetXaxis().SetTitle('Emulator - Unpacker HW phi')
    h_dEta_vs_dPhi.GetYaxis().SetTitle('Emulator - Unpacker HW eta')
    h_dEta_vs_dPhi.SetMarkerSize(1.5)
    h_dEta_vs_dPhi.SetMarkerColor(kWhite)
    h_dEta_vs_dPhi.Write()
    h_dEta_vs_eta.GetXaxis().SetTitle('Unpacker eta')
    h_dEta_vs_eta.GetYaxis().SetTitle('Emulator - Unpacker HW eta')
    h_dEta_vs_eta.SetMarkerSize(1.5)
    h_dEta_vs_eta.SetMarkerColor(kWhite)
    h_dEta_vs_eta.Write()
    h_dEta_vs_mode.GetXaxis().SetTitle('Unpacker mode')
    h_dEta_vs_mode.GetYaxis().SetTitle('Emulator - Unpacker HW eta')
    h_dEta_vs_mode.SetMarkerSize(1.5)
    h_dEta_vs_mode.SetMarkerColor(kWhite)
    h_dEta_vs_mode.Write()

    h_Emu_vs_Unp_pT_lowEta.GetXaxis().SetTitle('Unpacker pT')
    h_Emu_vs_Unp_pT_lowEta.GetYaxis().SetTitle('Emulator pT')
    h_Emu_vs_Unp_pT_lowEta.SetMarkerSize(1.5)
    h_Emu_vs_Unp_pT_lowEta.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_pT_lowEta.Write()
    h_Emu_vs_Unp_mode_lowEta.GetXaxis().SetTitle('Unpacker mode')
    h_Emu_vs_Unp_mode_lowEta.GetYaxis().SetTitle('Emulator mode')
    h_Emu_vs_Unp_mode_lowEta.SetMarkerSize(1.5)
    h_Emu_vs_Unp_mode_lowEta.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_mode_lowEta.Write()
    h_dEta_vs_dPhi_lowEta.GetXaxis().SetTitle('Emulator - Unpacker HW phi')
    h_dEta_vs_dPhi_lowEta.GetYaxis().SetTitle('Emulator - Unpacker HW eta')
    h_dEta_vs_dPhi_lowEta.SetMarkerSize(1.5)
    h_dEta_vs_dPhi_lowEta.SetMarkerColor(kWhite)
    h_dEta_vs_dPhi_lowEta.Write()
    h_Emu_vs_Unp_pT_hiEta.GetXaxis().SetTitle('Unpacker pT')
    h_Emu_vs_Unp_pT_hiEta.GetYaxis().SetTitle('Emulator pT')
    h_Emu_vs_Unp_pT_hiEta.SetMarkerSize(1.5)
    h_Emu_vs_Unp_pT_hiEta.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_pT_hiEta.Write()
    h_Emu_vs_Unp_mode_hiEta.GetXaxis().SetTitle('Unpacker mode')
    h_Emu_vs_Unp_mode_hiEta.GetYaxis().SetTitle('Emulator mode')
    h_Emu_vs_Unp_mode_hiEta.SetMarkerSize(1.5)
    h_Emu_vs_Unp_mode_hiEta.SetMarkerColor(kWhite)
    h_Emu_vs_Unp_mode_hiEta.Write()
    h_dEta_vs_dPhi_hiEta.GetXaxis().SetTitle('Emulator - Unpacker HW phi')
    h_dEta_vs_dPhi_hiEta.GetYaxis().SetTitle('Emulator - Unpacker HW eta')
    h_dEta_vs_dPhi_hiEta.SetMarkerSize(1.5)
    h_dEta_vs_dPhi_hiEta.SetMarkerColor(kWhite)
    h_dEta_vs_dPhi_hiEta.Write()

    out_file.Close()
    del tree
    file.Close()

if __name__ == '__main__':
    main()
