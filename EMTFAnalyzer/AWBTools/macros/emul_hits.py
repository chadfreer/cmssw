#! /usr/bin/env python

## Compare rates coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside emul_hits'

    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272012_files_12.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272775_10k.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272775_1k_ME1_fix.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/272936_123.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936_thetaCorr1_4k.root'
    ## file_name = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936_thetaCorr2.root'
    file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936.root'
    out_file = TFile('plots/emul_hits.root','recreate')

    tree_name = 'Events'

    file = TFile.Open(file_name)
    tree = file.Get(tree_name)

    numHits = {}
    numHits[0] = 0
    numHits[1] = 0
    numUniqueHits = {}
    numUniqueHits[0] = 0
    numUniqueHits[1] = 0

    # ###################
    # ### Book histograms
    # ###################

    phi_bins_1D = [740, -5, 365]
    phi_bins_2D = [185, -5, 365]
    dPhi_bins_1D = [320, -80, 80]
    dPhi_bins_2D = [80, -80, 80]
    # dPhi_bins_1D = [320, -400, 400]
    # dPhi_bins_2D = [80, -400, 400]
    ch_bins_10 = [75, -37.5, 37.5]
    ch_bins_20 = [39, -19.5, 19.5]
    ring_bins = [11, -5.5, 5.5]
    station_bins = [11, -5.5, 5.5]
    theta_bins = [201, -0.5, 200.5]

    h_phi_10 = TH1D('h_phi_10', 'Hit phi, 10 deg. chambers', phi_bins_1D[0], phi_bins_1D[1], phi_bins_1D[2])
    h_phi_20 = TH1D('h_phi_20', 'Hit phi, 20 deg. chambers', phi_bins_1D[0], phi_bins_1D[1], phi_bins_1D[2])

    h_dPhi_center_10 = TH1D('h_dPhi_center_10', 'Hit phi - chamber center, 10 deg. chambers', dPhi_bins_1D[0], dPhi_bins_1D[1], dPhi_bins_1D[2])
    h_dPhi_center_20 = TH1D('h_dPhi_center_20', 'Hit phi - chamber center, 20 deg. chambers', dPhi_bins_1D[0], dPhi_bins_1D[1], dPhi_bins_1D[2])

    h_phi_vs_chamber_10 = TH2D('h_phi_vs_chamber_10', 'Phi vs. 10 deg. chamber', ch_bins_10[0], ch_bins_10[1], ch_bins_10[2], phi_bins_2D[0], phi_bins_2D[1], phi_bins_2D[2])
    h_phi_vs_chamber_10_r2_st234 = TH2D('h_phi_vs_chamber_10_r2_st234', 'Phi vs. 10 deg. chamber, ring 2, stations 2 - 4', ch_bins_10[0], ch_bins_10[1], ch_bins_10[2], phi_bins_2D[0], phi_bins_2D[1], phi_bins_2D[2])
    h_phi_vs_chamber_10_r134_st1 = TH2D('h_phi_vs_chamber_10_r134_st1', 'Phi vs. 10 deg. chamber, ring != 2 or station 1', ch_bins_10[0], ch_bins_10[1], ch_bins_10[2], phi_bins_2D[0], phi_bins_2D[1], phi_bins_2D[2])
    h_phi_vs_chamber_20 = TH2D('h_phi_vs_chamber_20', 'Phi vs. 20 deg. chamber', ch_bins_20[0], ch_bins_20[1], ch_bins_20[2], phi_bins_2D[0], phi_bins_2D[1], phi_bins_2D[2])
    h_phi_vs_chamber_10.GetXaxis().SetTitle('Chamber x endcap')
    h_phi_vs_chamber_10_r2_st234.GetXaxis().SetTitle('Chamber x endcap')
    h_phi_vs_chamber_10_r134_st1.GetXaxis().SetTitle('Chamber x endcap')
    h_phi_vs_chamber_20.GetXaxis().SetTitle('Chamber x endcap')

    h_dPhi_vs_chamber_10 = TH2D('h_dPhi_vs_chamber_10', 'dPhi vs. 10 deg. chamber', ch_bins_10[0], ch_bins_10[1], ch_bins_10[2], dPhi_bins_2D[0], dPhi_bins_2D[1], dPhi_bins_2D[2])
    h_dPhi_vs_chamber_20 = TH2D('h_dPhi_vs_chamber_20', 'dPhi vs. 20 deg. chamber', ch_bins_20[0], ch_bins_20[1], ch_bins_20[2], dPhi_bins_2D[0], dPhi_bins_2D[1], dPhi_bins_2D[2])
    h_dPhi_vs_chamber_10.GetXaxis().SetTitle('Chamber x endcap')
    h_dPhi_vs_chamber_20.GetXaxis().SetTitle('Chamber x endcap')

    h_dPhi_vs_ring_10 = TH2D('h_dPhi_vs_ring', 'dPhi vs. ring, 10 deg. chamber', ring_bins[0], ring_bins[1], ring_bins[2], dPhi_bins_2D[0], dPhi_bins_2D[1], dPhi_bins_2D[2])
    h_dPhi_vs_ring_10.GetXaxis().SetTitle('Ring x endcap')

    h_dPhi_vs_station_10 = TH2D('h_dPhi_vs_station_10', 'dPhi vs. station, 10 deg. chamber', station_bins[0], station_bins[1], station_bins[2], dPhi_bins_2D[0], dPhi_bins_2D[1], dPhi_bins_2D[2])
    h_dPhi_vs_station_20 = TH2D('h_dPhi_vs_station_20', 'dPhi vs. station, 20 deg. chamber', station_bins[0], station_bins[1], station_bins[2], dPhi_bins_2D[0], dPhi_bins_2D[1], dPhi_bins_2D[2])
    h_dPhi_vs_station_10.GetXaxis().SetTitle('Station x endcap')
    h_dPhi_vs_station_20.GetXaxis().SetTitle('Station x endcap')

    h_theta_vs_ring_st1 = TH2D('h_theta_vs_ring_st1', 'Theta vs. ring, station 1', ring_bins[0], ring_bins[1], ring_bins[2], theta_bins[0], theta_bins[1], theta_bins[2])
    h_theta_vs_ring_st2 = TH2D('h_theta_vs_ring_st2', 'Theta vs. ring, station 2', ring_bins[0], ring_bins[1], ring_bins[2], theta_bins[0], theta_bins[1], theta_bins[2])
    h_theta_vs_ring_st3 = TH2D('h_theta_vs_ring_st3', 'Theta vs. ring, station 3', ring_bins[0], ring_bins[1], ring_bins[2], theta_bins[0], theta_bins[1], theta_bins[2])
    h_theta_vs_ring_st4 = TH2D('h_theta_vs_ring_st4', 'Theta vs. ring, station 4', ring_bins[0], ring_bins[1], ring_bins[2], theta_bins[0], theta_bins[1], theta_bins[2])

    for iEvt in range(tree.GetEntries()):
        
        ## if (iEvt > 40000): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt
        tree.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = tree.EventAuxiliary
        Hits_1 = tree.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        Trks_1 = tree.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        Hits_2 = tree.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_2 = tree.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        if (nHits1 == 0 and nHits2 == 0): continue
        nHitsUnique1 = 0
        nHitsUnique2 = 0

        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            if Hit1.BX() > -3 and Hit1.BX() < 3: ## and Hit1.Neighbor() != 1:

                numHits[0] += 1
                is_unique = True
                for jHit1 in range(nHits1):
                    Hit1a = Hits_1.at(jHit1)
                    if jHit1 < iHit1 and Hit1a.BX() > -3 and Hit1a.BX() < 3 and HitsMatch( Hit1, Hit1a ):
                        is_unique = False
                if is_unique: 
                    numUniqueHits[0] += 1
                    nHitsUnique1 += 1

        for iHit2 in range(nHits2):
            Hit2 = Hits_2.at(iHit2)
            if Hit2.BX() > -3 and Hit2.BX() < 3: ## and Hit2.Neighbor() != 1:

                numHits[1] += 1
                is_unique = True
                for jHit2 in range(nHits2):
                    Hit2a = Hits_2.at(jHit2)
                    if jHit2 < iHit2 and Hit2a.BX() > -3 and Hit2a.BX() < 3 and HitsMatch( Hit2, Hit2a ):
                        is_unique = False
                if is_unique: 
                    numUniqueHits[1] += 1
                    nHitsUnique2 += 1

                ## phi_glob_deg = CalcPhiGlobDeg( Hit2.Phi_loc_int(), Hit2.Sector() )
                phi_glob_deg = Hit2.Phi_glob_deg()
                if (phi_glob_deg <   0): phi_glob_deg = phi_glob_deg + 360
                if (phi_glob_deg > 360): phi_glob_deg = phi_glob_deg - 360
                dPhi_center = HitPhiInChamber( Hit2 )

                if ( Hit2.Station() != 1 and Hit2.Ring() == 1 ):
                    h_phi_20.Fill( phi_glob_deg )
                    h_dPhi_center_20.Fill( dPhi_center )
                    h_phi_vs_chamber_20.Fill( Hit2.Chamber()*Hit2.Endcap(), phi_glob_deg )
                    h_dPhi_vs_chamber_20.Fill( Hit2.Chamber()*Hit2.Endcap(), dPhi_center )
                    h_dPhi_vs_station_20.Fill( Hit2.Station()*Hit2.Endcap(), dPhi_center )

                else:
                    h_phi_10.Fill( phi_glob_deg )
                    h_dPhi_center_10.Fill( dPhi_center )
                    h_phi_vs_chamber_10.Fill( Hit2.Chamber()*Hit2.Endcap(), phi_glob_deg )
                    if ( Hit2.Ring() == 2 and Hit2.Station() > 1 ):
                        h_phi_vs_chamber_10_r2_st234.Fill( Hit2.Chamber()*Hit2.Endcap(), phi_glob_deg )
                    else:
                        h_phi_vs_chamber_10_r134_st1.Fill( Hit2.Chamber()*Hit2.Endcap(), phi_glob_deg )
                    h_dPhi_vs_chamber_10.Fill( Hit2.Chamber()*Hit2.Endcap(), dPhi_center )
                    h_dPhi_vs_ring_10.Fill( Hit2.Ring()*Hit2.Endcap(), dPhi_center )
                    h_dPhi_vs_station_10.Fill( Hit2.Station()*Hit2.Endcap(), dPhi_center )

                if ( Hit2.Station() == 1 ): h_theta_vs_ring_st1.Fill( Hit2.Ring()*Hit2.Endcap(), Hit2.Theta_int() )
                if ( Hit2.Station() == 2 ): h_theta_vs_ring_st2.Fill( Hit2.Ring()*Hit2.Endcap(), Hit2.Theta_int() )
                if ( Hit2.Station() == 3 ): h_theta_vs_ring_st3.Fill( Hit2.Ring()*Hit2.Endcap(), Hit2.Theta_int() )
                if ( Hit2.Station() == 4 ): h_theta_vs_ring_st4.Fill( Hit2.Ring()*Hit2.Endcap(), Hit2.Theta_int() )

        # if nHitsUnique1 != nHitsUnique2:
        #     print ''
        #     print '*** Unpacked hits ***'
        #     for iHit1 in range(nHits1):
        #         Hit1 = Hits_1.at(iHit1)
        #         PrintEMTFHit( Hit1 )
        #     print '*** Emulator hits ***'
        #     for iHit2 in range(nHits2):
        #         Hit2 = Hits_2.at(iHit2)
        #         PrintEMTFHit( Hit2 )

    print '*******************************************************'
    print '*******            The BIG picture              *******'
    print '*******************************************************'
    print '                       Unpacker    -  Emulator'
    print 'numHits:                %6d %11d' % (numHits[0], numHits[1]) 
    print 'numUniqueHits:          %6d %11d' % (numUniqueHits[0], numUniqueHits[1]) 


    out_file.cd()

    h_phi_10.Write()
    h_phi_vs_chamber_10_r2_st234.Write()
    h_phi_vs_chamber_10_r134_st1.Write()
    h_phi_20.Write()

    h_dPhi_center_10.Write()
    h_dPhi_center_20.Write()

    h_phi_vs_chamber_10.Write()
    h_phi_vs_chamber_20.Write()

    h_dPhi_vs_chamber_10.Write()
    h_dPhi_vs_chamber_20.Write()

    h_dPhi_vs_ring_10.Write()

    h_dPhi_vs_station_10.Write()
    h_dPhi_vs_station_20.Write()

    h_theta_vs_ring_st1.Write()
    h_theta_vs_ring_st2.Write()
    h_theta_vs_ring_st3.Write()
    h_theta_vs_ring_st4.Write()

    out_file.Close()
    del tree
    file.Close()

if __name__ == '__main__':
    main()
