#! /usr/bin/env python

## Compare emulator tracks running with input LCTs from emtfStage2Digis vs. csctfDigis

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside emul_vs_unpack_tracks'

    file_name_1 = '../NTupleMaker/EMTF_Tree_ZMu_274442_csctfDigis_10k.root'
    file_name_2 = '../NTupleMaker/EMTF_Tree_ZMu_274442_emtfStage2Digis_10k.root'

    out_file = TFile('plots/emtfDigi_vs_csctfDigi_emul_tracks.root','recreate')

    tree_name = 'Events'

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

    h_BX = TH1D('h_BX', 'eDigi & cDigi BX', BX_bins[0], BX_bins[1], BX_bins[2])
    ## h_pT = TH1D('h_pT', 'eDigi & cDigi pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_phi = TH1D('h_phi', 'eDigi & cDigi phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_eta = TH1D('h_eta', 'eDigi & cDigi eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_mode = TH1D('h_mode', 'eDigi & cDigi mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_evt = TH1D('h_evt', 'eDigi & cDigi evt', evt_bins[0], evt_bins[1], evt_bins[2])
    h_dPt_same_mode = TH1D('h_dPt_same_mode', 'eDigi - cDigi pT, same mode', dPt_bins[0], dPt_bins[1], dPt_bins[2])
    h_dPt_diff_mode = TH1D('h_dPt_diff_mode', 'eDigi - cDigi pT, diff. mode', dPt_bins[0], dPt_bins[1], dPt_bins[2])

    h_cDigi_BX = TH1D('h_cDigi_BX', 'csctfDigi BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_cDigi_pT = TH1D('h_cDigi_pT', 'csctfDigi pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_cDigi_phi = TH1D('h_cDigi_phi', 'csctfDigi phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_cDigi_eta = TH1D('h_cDigi_eta', 'csctfDigi eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_cDigi_mode = TH1D('h_cDigi_mode', 'csctfDigi mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_cDigi_evt = TH1D('h_cDigi_evt', 'csctfDigi evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_cDigi_only_BX = TH1D('h_cDigi_only_BX', 'csctfDigi-only BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_cDigi_only_pT = TH1D('h_cDigi_only_pT', 'csctfDigi-only pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_cDigi_only_phi = TH1D('h_cDigi_only_phi', 'csctfDigi-only phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_cDigi_only_eta = TH1D('h_cDigi_only_eta', 'csctfDigi-only eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_cDigi_only_mode = TH1D('h_cDigi_only_mode', 'csctfDigi-only mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_cDigi_only_evt = TH1D('h_cDigi_only_evt', 'csctfDigi-only evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_eDigi_BX = TH1D('h_eDigi_BX', 'emtfDigi BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_eDigi_pT = TH1D('h_eDigi_pT', 'emtfDigi pT', pT_bins[0], pT_bins[1], pT_bins[2]) 
    h_eDigi_phi = TH1D('h_eDigi_phi', 'emtfDigi phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_eDigi_eta = TH1D('h_eDigi_eta', 'emtfDigi eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_eDigi_mode = TH1D('h_eDigi_mode', 'emtfDigi mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_eDigi_evt = TH1D('h_eDigi_evt', 'emtfDigi evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_eDigi_only_BX = TH1D('h_eDigi_only_BX', 'emtfDigi-only BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_eDigi_only_pT = TH1D('h_eDigi_only_pT', 'emtfDigi-only pT', pT_bins[0], pT_bins[1], pT_bins[2]) 
    h_eDigi_only_phi = TH1D('h_eDigi_only_phi', 'emtfDigi-only phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_eDigi_only_eta = TH1D('h_eDigi_only_eta', 'emtfDigi-only eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_eDigi_only_mode = TH1D('h_eDigi_only_mode', 'emtfDigi-only mode', mode_bins[0], mode_bins[1], mode_bins[2])
    ## h_eDigi_only_evt = TH1D('h_eDigi_only_evt', 'emtfDigi-only evt', evt_bins[0], evt_bins[1], evt_bins[2])

    h_eDigi_vs_cDigi_BX = TH2D('h_eDigi_vs_cDigi_BX', 'emtfDigi vs. csctfDigi BX', BX_bins[0], BX_bins[1], BX_bins[2], BX_bins[0], BX_bins[1], BX_bins[2])
    h_eDigi_vs_cDigi_pT = TH2D('h_eDigi_vs_cDigi_pT', 'emtfDigi vs. csctfDigi pT', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_eDigi_vs_cDigi_mode = TH2D('h_eDigi_vs_cDigi_mode', 'emtfDigi vs. csctfDigi mode', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_dEta_vs_dPhi = TH2D('h_dEta_vs_dPhi', 'emtfDigi - csctfDigi dEta vs. dPhi', 19, -9.5, 9.5, 19, -9.5, 9.5)
    h_dEta_vs_eta = TH2D('h_dEta_vs_eta', 'emtfDigi - csctfDigi dEta vs. Eta', eta_bins[0], eta_bins[1], eta_bins[2], 19, -9.5, 9.5)
    h_dEta_vs_mode = TH2D('h_dEta_vs_mode', 'emtfDigi - csctfDigi dEta vs. Mode', mode_bins[0], mode_bins[1], mode_bins[2], 19, -9.5, 9.5)

    h_eDigi_vs_cDigi_pT_lowEta = TH2D('h_eDigi_vs_cDigi_pT_lowEta', 'emtfDigi vs. csctfDigi pT, |eta| < 1.5', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_eDigi_vs_cDigi_mode_lowEta = TH2D('h_eDigi_vs_cDigi_mode_lowEta', 'emtfDigi vs. csctfDigi mode, |eta| < 1.5', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_dEta_vs_dPhi_lowEta = TH2D('h_dEta_vs_dPhi_lowEta', 'emtfDigi - csctfDigi dEta vs. dPhi, |eta| < 1.5', 19, -9.5, 9.5, 19, -9.5, 9.5)
    h_eDigi_vs_cDigi_pT_hiEta = TH2D('h_eDigi_vs_cDigi_pT_hiEta', 'emtfDigi vs. csctfDigi pT, |eta| > 1.5', pT_bins[0], pT_bins[1], pT_bins[2], pT_bins[0], pT_bins[1], pT_bins[2])
    h_eDigi_vs_cDigi_mode_hiEta = TH2D('h_eDigi_vs_cDigi_mode_hiEta', 'emtfDigi vs. csctfDigi mode, |eta| > 1.5', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_dEta_vs_dPhi_hiEta = TH2D('h_dEta_vs_dPhi_hiEta', 'emtfDigi - csctfDigi dEta vs. dPhi, |eta| < 1.5', 19, -9.5, 9.5, 19, -9.5, 9.5)

    ## h_eDigi_vs_cDigi_phi = TH2D('h_eDigi_vs_cDigi_phi', 'emtfDigi vs. csctfDigi phi', phi_bins[0], phi_bins[1], phi_bins[2], phi_bins[0], phi_bins[1], phi_bins[2])
    ## h_eDigi_vs_cDigi_eta = TH2D('h_eDigi_vs_cDigi_eta', 'emtfDigi vs. csctfDigi eta', eta_bins[0], eta_bins[1], eta_bins[2], eta_bins[0], eta_bins[1], eta_bins[2])

    ## Main event loop    
    # for iEvt in range(tree.GetEntries()):
    for iEvt in range(tree_1.GetEntries()):
        
        ## if (iEvt > 100): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt
        tree_1.GetEntry(iEvt)
        tree_2.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = tree_1.EventAuxiliary
        Hits_1 = tree_1.l1tEMTFHits_simEmtfDigis_CSC_L1TMuonEmulation
        Trks_1 = tree_1.l1tEMTFTracks_simEmtfDigis__L1TMuonEmulation
        Hits_2 = tree_2.l1tEMTFHits_simEmtfDigis_CSC_L1TMuonEmulation
        Trks_2 = tree_2.l1tEMTFTracks_simEmtfDigis__L1TMuonEmulation
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        if (nHits1 == 0 and nHits2 == 0): continue

        # ######################################
        # ### Print out every hit in every event
        # ######################################

        # print 'csctfDigi: %d hits and %d tracks in event %d' % ( nHits1, nTrks1, Event.event() )
        # for iHit1 in range(nHits1):
        #     Hit1 = Hits_1.at(iHit1)
        #     print 'BX = %d, station = %d, sector = %d, ' % ( Hit1.BX(), Hit1.Station(), Hit1.Sector() ), \
        #         'CSC ID = %d, strip = %d, wire = %d, neighbor = %d' % ( Hit1.CSC_ID(), Hit1.Strip(), Hit1.Wire(), Hit1.Neighbor() )
            
        # print 'emtfDigi: %d hits and %d tracks in event %d' % ( nHits2, nTrks2, Event.event() )
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
        ### Compare hits in emtfDigi and csctfDigi
        ###   * emtfDigi outputs all hits it received, whether or not a track was formed
        ###   * csctfDigi usually outputs neighbor hits twice, but sometimes it misses one
        #####################################################################################

        ## Check that csctfDigi hits have match in emtfDigi
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

        ## Check that emtfDigi hits have match in csctfDigi
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
        # print 'csctfDigi: %d tracks in event %d' % ( nTrks1, Event.event() )
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

        # print 'emtfDigi: %d tracks in event %d' % ( nTrks2, Event.event() )
        # for iTrk2 in range(nTrks2):
        #     Trk2 = Trks_2.at(iTrk2)
        #     print 'BX = %d, sector = %d, mode = %d, eta = %d, ' % ( Trk2.BX(), Trk2.Sector(), Trk2.Mode(), Trk2.Eta() ), \
        #         'phi = %d, pT = %d' % ( Trk2.Phi(), ((Trk2.Pt_GMT()/2.0) - 0.5)  )
        # print ''
        # continue


        #####################################################################################
        ### Compare tracks in emtfDigi and csctfDigi
        ###   * Only compare if emtfDigi and csctfDigi hits are identical
        #####################################################################################

        # if unmatched_hit_exists:
        #     continue
        # # if neighbor_hit_exists:
        # #     continue
        # if ( nTrks1 == 0 and nTrks2 == 0 ):
        #     continue
        # # if ( nTrks1 > 2 or nTrks2 > 2 ):
        # #     continue

        ## Check that csctfDigi tracks have match in emtfDigi
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

            h_cDigi_BX.Fill( Trk1.BX() )
            h_cDigi_mode.Fill( Trk1.Mode() )
            h_cDigi_eta.Fill( Trk1.Eta() )
            h_cDigi_phi.Fill( Trk1.Phi_glob_deg() )
            h_cDigi_pT.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )

            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)
                if TracksMatch( Trk1, Trk2 ):
                    unp_trk_matched = True

                    h_eDigi_vs_cDigi_BX.Fill( Trk1.BX(), Trk2.BX() )
                    h_eDigi_vs_cDigi_mode.Fill( Trk1.Mode(), Trk2.Mode() )
                    h_dEta_vs_dPhi.Fill( Trk2.Phi_GMT() - Trk1.Phi_GMT(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                    h_dEta_vs_eta.Fill( Trk1.Eta(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                    h_dEta_vs_mode.Fill( Trk1.Mode(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )

                    h_eta.Fill( Trk1.Eta() )
                    h_phi.Fill( Trk1.Phi_glob_deg() )
                    if ( Trk1.BX() == Trk2.BX() ):
                        h_BX.Fill( Trk1.BX() )
                    if ( Trk1.Mode() == Trk2.Mode() ):
                        h_mode.Fill( Trk1.Mode() )
                        h_eDigi_vs_cDigi_pT.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2]-0.01), min( ((Trk2.Pt_GMT()/2.0) - 0.5) , pT_bins[2]-0.01) )
                        h_dPt_same_mode.Fill( max(dPt_bins[1]+0.01, min(dPt_bins[2]-0.01, ((Trk2.Pt_GMT()/2.0) - 0.5)  - ((Trk1.Pt_GMT()/2.0) - 0.5) ) ) )
                    else:
                        h_dPt_diff_mode.Fill( max(dPt_bins[1]+0.01, min(dPt_bins[2]-0.01, ((Trk2.Pt_GMT()/2.0) - 0.5)  - ((Trk1.Pt_GMT()/2.0) - 0.5) ) ) )

                    if ( abs(Trk1.Eta()) < 1.5 ):
                        h_eDigi_vs_cDigi_mode_lowEta.Fill( Trk1.Mode(), Trk2.Mode() )
                        h_dEta_vs_dPhi_lowEta.Fill( Trk2.Phi_GMT() - Trk1.Phi_GMT(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                        if ( Trk1.Mode() == Trk2.Mode() ):
                            h_eDigi_vs_cDigi_pT_lowEta.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2]-0.01), min( ((Trk2.Pt_GMT()/2.0) - 0.5) , pT_bins[2]-0.01) )
                    else:
                        h_eDigi_vs_cDigi_mode_hiEta.Fill( Trk1.Mode(), Trk2.Mode() )
                        h_dEta_vs_dPhi_hiEta.Fill( Trk2.Phi_GMT() - Trk1.Phi_GMT(), Trk2.Eta_GMT() - Trk1.Eta_GMT() )
                        if ( Trk1.Mode() == Trk2.Mode() ):
                            h_eDigi_vs_cDigi_pT_hiEta.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2]-0.01), min( ((Trk2.Pt_GMT()/2.0) - 0.5) , pT_bins[2]-0.01) )

                            
            if not unp_trk_matched:
                numTrksUnm[0] += 1
                h_cDigi_only_BX.Fill( Trk1.BX() )
                h_cDigi_only_mode.Fill( Trk1.Mode() )
                h_cDigi_only_eta.Fill( Trk1.Eta() )
                h_cDigi_only_phi.Fill( Trk1.Phi_glob_deg() )
                h_cDigi_only_pT.Fill( min( ((Trk1.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )
                if (nTrks2 > 0):
                    numTrksUnmExist[0] += 1

        ## Check that emtfDigi tracks have match in csctfDigi
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

            h_eDigi_BX.Fill( Trk2.BX() )
            h_eDigi_mode.Fill( Trk2.Mode() )
            h_eDigi_eta.Fill( Trk2.Eta() )
            h_eDigi_phi.Fill( Trk2.Phi_glob_deg() )
            h_eDigi_pT.Fill( min( ((Trk2.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )

            emu_trk_matched = False
            for iTrk1 in range(nTrks1):
                Trk1 = Trks_1.at(iTrk1)
                if TracksMatch( Trk1, Trk2 ):
                    emu_trk_matched = True

            if not emu_trk_matched:
                numTrksUnm[1] += 1
                h_eDigi_only_BX.Fill( Trk2.BX() )
                h_eDigi_only_mode.Fill( Trk2.Mode() )
                h_eDigi_only_eta.Fill( Trk2.Eta() )
                h_eDigi_only_phi.Fill( Trk2.Phi_glob_deg() )
                h_eDigi_only_pT.Fill( min( ((Trk2.Pt_GMT()/2.0) - 0.5), pT_bins[2] - 0.01) )
                if (nTrks1 > 0):
                    numTrksUnmExist[1] += 1



    print '*******************************************************'
    print '*******            The BIG picture              *******'
    print '*******************************************************'
    print '                       csctfDigi    -  emtfDigi'
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
    h_dPt_same_mode.GetXaxis().SetTitle('eDigi - cDigi pT')
    h_dPt_same_mode.Write()
    h_dPt_diff_mode.GetXaxis().SetTitle('eDigi - cDigi pT')
    h_dPt_diff_mode.Write()
    h_phi.GetXaxis().SetTitle('phi')
    h_phi.Write()
    h_eta.GetXaxis().SetTitle('eta')
    h_eta.Write()
    h_mode.GetXaxis().SetTitle('Mode')
    h_mode.Write()
    # h_evt.GetXaxis().SetTitle('iEvt')
    # h_evt.Write()

    h_cDigi_BX.GetXaxis().SetTitle('BX')
    h_cDigi_BX.Write()
    h_cDigi_pT.GetXaxis().SetTitle('pT')
    h_cDigi_pT.SetLineWidth(2)
    h_cDigi_pT.SetLineColor(kBlue)
    h_cDigi_pT.Write()
    h_cDigi_phi.GetXaxis().SetTitle('phi')
    h_cDigi_phi.SetLineWidth(2)
    h_cDigi_phi.SetLineColor(kBlue)
    h_cDigi_phi.Write()
    h_cDigi_eta.GetXaxis().SetTitle('eta')
    h_cDigi_eta.SetLineWidth(2)
    h_cDigi_eta.SetLineColor(kBlue)
    h_cDigi_eta.Write()
    h_cDigi_mode.GetXaxis().SetTitle('Mode')
    h_cDigi_mode.SetLineWidth(2)
    h_cDigi_mode.SetLineColor(kBlue)
    h_cDigi_mode.Write()
    # h_cDigi_evt.GetXaxis().SetTitle('iEvt')
    # h_cDigi_evt.Write()

    h_eDigi_BX.GetXaxis().SetTitle('BX')
    h_eDigi_BX.Write()
    h_eDigi_pT.GetXaxis().SetTitle('pT')
    h_eDigi_pT.SetLineWidth(2)
    h_eDigi_pT.SetLineColor(kRed)
    h_eDigi_pT.Write()
    h_eDigi_phi.GetXaxis().SetTitle('phi')
    h_eDigi_phi.SetLineWidth(2)
    h_eDigi_phi.SetLineColor(kRed)
    h_eDigi_phi.Write()
    h_eDigi_eta.GetXaxis().SetTitle('eta')
    h_eDigi_eta.SetLineWidth(2)
    h_eDigi_eta.SetLineColor(kRed)
    h_eDigi_eta.Write()
    h_eDigi_mode.GetXaxis().SetTitle('Mode')
    h_eDigi_mode.SetLineWidth(2)
    h_eDigi_mode.SetLineColor(kRed)
    h_eDigi_mode.Write()
    # h_eDigi_evt.GetXaxis().SetTitle('iEvt')
    # h_eDigi_evt.Write()

    h_cDigi_only_BX.GetXaxis().SetTitle('BX')
    h_cDigi_only_BX.Write()
    h_cDigi_only_pT.GetXaxis().SetTitle('pT')
    h_cDigi_only_pT.Write()
    h_cDigi_only_phi.GetXaxis().SetTitle('phi')
    h_cDigi_only_phi.Write()
    h_cDigi_only_eta.GetXaxis().SetTitle('eta')
    h_cDigi_only_eta.Write()
    h_cDigi_only_mode.GetXaxis().SetTitle('Mode')
    h_cDigi_only_mode.Write()
    # h_cDigi_evt.GetXaxis().SetTitle('iEvt')
    # h_cDigi_evt.Write()

    h_eDigi_only_BX.GetXaxis().SetTitle('BX')
    h_eDigi_only_BX.Write()
    h_eDigi_only_pT.GetXaxis().SetTitle('pT')
    h_eDigi_only_pT.Write()
    h_eDigi_only_phi.GetXaxis().SetTitle('phi')
    h_eDigi_only_phi.Write()
    h_eDigi_only_eta.GetXaxis().SetTitle('eta')
    h_eDigi_only_eta.Write()
    h_eDigi_only_mode.GetXaxis().SetTitle('Mode')
    h_eDigi_only_mode.Write()
    # h_eDigi_evt.GetXaxis().SetTitle('iEvt')
    # h_eDigi_evt.Write()

    h_eDigi_vs_cDigi_BX.GetXaxis().SetTitle('csctfDigi BX')
    h_eDigi_vs_cDigi_BX.GetYaxis().SetTitle('emtfDigi BX')
    h_eDigi_vs_cDigi_BX.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_BX.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_BX.Write()
    h_eDigi_vs_cDigi_pT.GetXaxis().SetTitle('csctfDigi pT')
    h_eDigi_vs_cDigi_pT.GetYaxis().SetTitle('emtfDigi pT')
    h_eDigi_vs_cDigi_pT.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_pT.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_pT.Write()
    # h_eDigi_vs_cDigi_phi.GetXaxis().SetTitle('csctfDigi phi')
    # h_eDigi_vs_cDigi_phi.GetYaxis().SetTitle('emtfDigi phi')
    # h_eDigi_vs_cDigi_phi.SetMarkerSize(1.5)
    # h_eDigi_vs_cDigi_phi.SetMarkerColor(kWhite)
    # h_eDigi_vs_cDigi_phi.Write()
    # h_eDigi_vs_cDigi_eta.GetXaxis().SetTitle('csctfDigi eta')
    # h_eDigi_vs_cDigi_eta.GetYaxis().SetTitle('emtfDigi eta')
    # h_eDigi_vs_cDigi_eta.SetMarkerSize(1.5)
    # h_eDigi_vs_cDigi_eta.SetMarkerColor(kWhite)
    # h_eDigi_vs_cDigi_eta.Write()
    h_eDigi_vs_cDigi_mode.GetXaxis().SetTitle('csctfDigi mode')
    h_eDigi_vs_cDigi_mode.GetYaxis().SetTitle('emtfDigi mode')
    h_eDigi_vs_cDigi_mode.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_mode.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_mode.Write()
    h_dEta_vs_dPhi.GetXaxis().SetTitle('emtfDigi - csctfDigi HW phi')
    h_dEta_vs_dPhi.GetYaxis().SetTitle('emtfDigi - csctfDigi HW eta')
    h_dEta_vs_dPhi.SetMarkerSize(1.5)
    h_dEta_vs_dPhi.SetMarkerColor(kWhite)
    h_dEta_vs_dPhi.Write()
    h_dEta_vs_eta.GetXaxis().SetTitle('csctfDigi eta')
    h_dEta_vs_eta.GetYaxis().SetTitle('emtfDigi - csctfDigi HW eta')
    h_dEta_vs_eta.SetMarkerSize(1.5)
    h_dEta_vs_eta.SetMarkerColor(kWhite)
    h_dEta_vs_eta.Write()
    h_dEta_vs_mode.GetXaxis().SetTitle('csctfDigi mode')
    h_dEta_vs_mode.GetYaxis().SetTitle('emtfDigi - csctfDigi HW eta')
    h_dEta_vs_mode.SetMarkerSize(1.5)
    h_dEta_vs_mode.SetMarkerColor(kWhite)
    h_dEta_vs_mode.Write()

    h_eDigi_vs_cDigi_pT_lowEta.GetXaxis().SetTitle('csctfDigi pT')
    h_eDigi_vs_cDigi_pT_lowEta.GetYaxis().SetTitle('emtfDigi pT')
    h_eDigi_vs_cDigi_pT_lowEta.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_pT_lowEta.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_pT_lowEta.Write()
    h_eDigi_vs_cDigi_mode_lowEta.GetXaxis().SetTitle('csctfDigi mode')
    h_eDigi_vs_cDigi_mode_lowEta.GetYaxis().SetTitle('emtfDigi mode')
    h_eDigi_vs_cDigi_mode_lowEta.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_mode_lowEta.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_mode_lowEta.Write()
    h_dEta_vs_dPhi_lowEta.GetXaxis().SetTitle('emtfDigi - csctfDigi HW phi')
    h_dEta_vs_dPhi_lowEta.GetYaxis().SetTitle('emtfDigi - csctfDigi HW eta')
    h_dEta_vs_dPhi_lowEta.SetMarkerSize(1.5)
    h_dEta_vs_dPhi_lowEta.SetMarkerColor(kWhite)
    h_dEta_vs_dPhi_lowEta.Write()
    h_eDigi_vs_cDigi_pT_hiEta.GetXaxis().SetTitle('csctfDigi pT')
    h_eDigi_vs_cDigi_pT_hiEta.GetYaxis().SetTitle('emtfDigi pT')
    h_eDigi_vs_cDigi_pT_hiEta.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_pT_hiEta.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_pT_hiEta.Write()
    h_eDigi_vs_cDigi_mode_hiEta.GetXaxis().SetTitle('csctfDigi mode')
    h_eDigi_vs_cDigi_mode_hiEta.GetYaxis().SetTitle('emtfDigi mode')
    h_eDigi_vs_cDigi_mode_hiEta.SetMarkerSize(1.5)
    h_eDigi_vs_cDigi_mode_hiEta.SetMarkerColor(kWhite)
    h_eDigi_vs_cDigi_mode_hiEta.Write()
    h_dEta_vs_dPhi_hiEta.GetXaxis().SetTitle('emtfDigi - csctfDigi HW phi')
    h_dEta_vs_dPhi_hiEta.GetYaxis().SetTitle('emtfDigi - csctfDigi HW eta')
    h_dEta_vs_dPhi_hiEta.SetMarkerSize(1.5)
    h_dEta_vs_dPhi_hiEta.SetMarkerColor(kWhite)
    h_dEta_vs_dPhi_hiEta.Write()

    out_file.Close()
    del tree_1
    del tree_2
    file_1.Close()
    file_2.Close()

if __name__ == '__main__':
    main()
