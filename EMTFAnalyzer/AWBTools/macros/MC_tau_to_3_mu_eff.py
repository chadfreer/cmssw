#! /usr/bin/env python

## Compare tracks coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    file_name = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/lowPt_MC/EMTF_MC_Tree_tau_to_3_mu_09_21.root'
    out_file = TFile('plots/MC_tau_to_3_mu_eff.root','recreate')

    tree_name = 'Events'

    file = TFile.Open(file_name)
    tree = file.Get(tree_name)

    ## RECO muon cuts
    eta_min = 1.2
    eta_max = 2.4

    ## EMTF track cancellation
    cancel_by_dR = True
    cancel_by_LCT = False
    dR_cut = 0.1

    #################
    ### Book counters
    #################

    ## Number of unique hits and tracks
    numLen = 15
    numGens = {}
    numRecos = {}
    numTrks = {}
    numHits = {}

    for i in range(numLen):
        numGens[i] = 0
        numRecos[i] = 0
        numTrks[i] = 0
        numHits[i] = 0

    ## Triggers fired
    SingleMu_0 = 0
    SingleMu_Q8_0 = 0
    SingleMu_Q4_0 = 0
    DoubleMu_0 = 0
    DoubleMu_Q4_0 = 0
    TripleMu_0 = 0
    TripleMu_Q4_0 = 0
    SingleMu_22 = 0
    DoubleMu_12_5 = 0
    DoubleMu_0_LCT = 0
    DoubleMu_0_LCT_St1 = 0
    DoubleMu_Q4_0_LCT = 0
    DoubleMu_Q4_0_LCT_St1 = 0
    TripleMu_0_OR_DoubleMu_0_LCT_St1 = 0
    TripleMu_Q4_0_OR_DoubleMu_Q4_0_LCT = 0

    ###################
    ### Book histograms
    ###################

    nTrk_bins = [8, -0.5, 7.5]
    nHit_bins = [16, -0.5, 15.5]
    pT_bins = [32, -1.5, 30.5]
    phi_bins = [64, -3.2, 3.2]
    eta_bins = [50, -2.5, 2.5]
    mode_bins = [18, -1.5, 16.5]
    stat_bins = [5, -0.5, 4.5]
    dR_bins = [17, -0.2, 1.5]
    dPhi_bins = [22, -1.2, 1.0]
    dEta_bins = [22, -0.6, 0.5]

    h_nGen = TH1D('h_nGen', 'Number of GEN muons', nTrk_bins[0], nTrk_bins[1], nTrk_bins[2])
    h_gen_pT = TH1D('h_gen_pT', 'GEN muon pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_gen_phi = TH1D('h_gen_phi', 'GEN muon phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_gen_eta = TH1D('h_gen_eta', 'GEN muon eta', eta_bins[0], eta_bins[1], eta_bins[2])

    h_nReco = TH1D('h_nReco', 'Number of RECO muons', nTrk_bins[0], nTrk_bins[1], nTrk_bins[2])
    h_reco_pT = TH1D('h_reco_pT', 'RECO muon pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_reco_phi = TH1D('h_reco_phi', 'RECO muon phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_reco_eta = TH1D('h_reco_eta', 'RECO muon eta', eta_bins[0], eta_bins[1], eta_bins[2])

    h_nTrk = TH1D('h_nTrk', 'Number of unique EMTF tracks', nTrk_bins[0], nTrk_bins[1], nTrk_bins[2])
    h_trk_pT = TH1D('h_trk_pT', 'EMTF track pT', pT_bins[0], pT_bins[1], pT_bins[2])
    h_trk_phi = TH1D('h_trk_phi', 'EMTF track phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_trk_eta = TH1D('h_trk_eta', 'EMTF track eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_trk_mode = TH1D('h_trk_mode', 'EMTF track mode', mode_bins[0], mode_bins[1], mode_bins[2])
    h_trk_qual = TH1D('h_trk_qual', 'EMTF track quality', mode_bins[0], mode_bins[1], mode_bins[2])

    h_nHit = TH1D('h_nHit', 'Number of unique EMTF hits (LCTs)', nHit_bins[0], nHit_bins[1], nHit_bins[2])
    h_hit_phi = TH1D('h_hit_phi', 'EMTF hit phi', phi_bins[0], phi_bins[1], phi_bins[2])
    h_hit_eta = TH1D('h_hit_eta', 'EMTF hit eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_hit_stat = TH1D('h_hit_stat', 'EMTF hit station', stat_bins[0], stat_bins[1], stat_bins[2])

    h_nTrk_vs_nGen = TH2D('h_nTrk_vs_nGen', 'Number of unique EMTF tracks vs. GEN muons', nTrk_bins[0], nTrk_bins[1], nTrk_bins[2], nTrk_bins[0], nTrk_bins[1], nTrk_bins[2])
    h_nTrk_vs_nReco = TH2D('h_nTrk_vs_nReco', 'Number of unique EMTF tracks vs. RECO muons', nTrk_bins[0], nTrk_bins[1], nTrk_bins[2], nTrk_bins[0], nTrk_bins[1], nTrk_bins[2])
    h_nHit_vs_nTrk = TH2D('h_nHit_vs_nTrk', 'Number of unique EMTF hits vs. tracks', nTrk_bins[0], nTrk_bins[1], nTrk_bins[2], nHit_bins[0], nHit_bins[1], nHit_bins[2])

    h_trk_gen_dR = TH1D('h_trk_gen_dR', 'dR(EMTF track, GEN muon)', dR_bins[0], dR_bins[1], dR_bins[2])
    h_trk_gen_dPhi = TH1D('h_trk_gen_dPhi', 'dPhi(EMTF track, GEN muon)', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2])
    h_trk_gen_dEta = TH1D('h_trk_gen_dEta', 'dEta(EMTF track, GEN muon)', dEta_bins[0], dEta_bins[1], dEta_bins[2])

    h_hit_gen_dR = TH1D('h_hit_gen_dR', 'dR(EMTF hit, GEN muon)', dR_bins[0], dR_bins[1], dR_bins[2])
    h_hit_gen_dPhi = TH1D('h_hit_gen_dPhi', 'dPhi(EMTF hit, GEN muon)', dPhi_bins[0], dPhi_bins[1], dPhi_bins[2])
    h_hit_gen_dEta = TH1D('h_hit_gen_dEta', 'dEta(EMTF hit, GEN muon)', dEta_bins[0], dEta_bins[1], dEta_bins[2])

    ## Main event loop    
    nEvt = 0
    for iEvt in range(tree.GetEntries()):

        # if iEvt > 1000: break
        if iEvt % 100 is 0: print 'Event #', iEvt
        tree.GetEntry(iEvt)
        nEvt += 1

        ## Get branches from the trees
        Event = tree.EventAuxiliary
        Gens = tree.recoGenParticles_genParticles__HLT
        Recos = tree.recoMuons_muons__HLT
        Trks  = tree.l1tEMTFTracks_simEmtfDigis__reL1T
        Hits  = tree.l1tEMTFHits_simEmtfDigis_CSC_reL1T

        nGens = Gens.size()
        nRecos = Recos.size()
        nTrks = Trks.size()
        nHits = Hits.size()

        unique_gens = []
        unique_recos = []
        unique_trks = []
        unique_hits_1 = []
        unique_hits_2 = []
        unique_hits_3 = []
        
        trks_in_sect = {}
        hits_in_sect_1 = {}
        hits_in_sect_3 = {}
        for i in range(12):
            trks_in_sect[i] = 0
            hits_in_sect_1[i] = 0
            hits_in_sect_3[i] = 0

        ## Find GEN muons
        for iGen in range(Gens.size()):
            Gen = Gens.at(iGen)
            if abs(Gen.pdgId()) != 13: continue
            if abs(Gen.eta()) < eta_min: continue
            if abs(Gen.eta()) > eta_max: continue 

            unique_gens.append(iGen)
            h_gen_pT.Fill( min(Gen.pt(), pT_bins[2]-0.01) )
            h_gen_phi.Fill( Gen.phi() )
            h_gen_eta.Fill( Gen.eta() )

        if len(unique_gens) != 3: continue
        h_nGen.Fill( min(len(unique_gens), h_nTrk[2]-0.01) )
        numGens[min(len(unique_gens), numLen-1)] += 1

        ## Find RECO muons
        for iReco in range(Recos.size()):
            Reco = Recos.at(iReco)
            if Reco.isStandAloneMuon() != 1: continue
            if Reco.isTrackerMuon() != 1: continue
            if Reco.isGlobalMuon() != 1: continue
            if Reco.isPFMuon() != 1: continue
            if abs(Reco.eta()) < 1.2: continue

            unique_recos.append(iReco)
            h_reco_pT.Fill( min(Reco.pt(), pT_bins[2]-0.01) )
            h_reco_phi.Fill( Reco.phi() )
            h_reco_eta.Fill( Reco.eta() )

        h_nReco.Fill( min(len(unique_recos), h_nTrk[2]-0.01) )
        numRecos[min(len(unique_recos), numLen-1)] += 1

        ## Find unique EMTF tracks
        for iTrk in range(nTrks):
            Trk = Trks.at(iTrk)
            if Trk.BX() != 0: continue
            trks_in_sect[Trk.Sector_index()] += 1

            unique_trk = True
            for jTrk in range(nTrks):
                if iTrk == jTrk: continue
                Trk2 = Trks.at(jTrk)
                if Trk2.BX() != 0: continue

                for iHit in range(Trk.PtrHits().size()):
                    for jHit in range(Trk2.PtrHits().size()):
                        if HitsMatch( Trk.PtrHits().at(iHit), Trk2.PtrHits().at(jHit) ):
                            if Trk.Quality() < Trk2.Quality() or (Trk.Quality() == Trk2.Quality() and iTrk > jTrk): 
                                if cancel_by_LCT: unique_trk = False
                
                if Trk.Sector() == Trk2.Sector() and CalcDR( Trk.Eta(), Trk.Phi_glob_rad(), Trk2.Eta(), Trk2.Phi_glob_rad() ) < dR_cut:
                    if Trk.Quality() < Trk2.Quality() or (Trk.Quality() == Trk2.Quality() and iTrk > jTrk): 
                        if cancel_by_dR: unique_trk = False
            
            if unique_trk:
                unique_trks.append(iTrk)
                h_trk_pT.Fill( min(Trk.Pt(), pT_bins[2]-0.01) )
                h_trk_phi.Fill( Trk.Phi_glob_rad() )
                h_trk_eta.Fill( Trk.Eta() )
                h_trk_mode.Fill( Trk.Mode() )
                h_trk_qual.Fill( Trk.Quality() )

        numTrks[min(len(unique_trks), numLen-1)] += 1
        h_nTrk.Fill( min(len(unique_trks), nTrk_bins[2]-0.01) )
        h_nTrk_vs_nGen.Fill( min(len(unique_gens), h_nTrk[2]-0.01), min(len(unique_trks), nTrk_bins[2]-0.01) )
        h_nTrk_vs_nReco.Fill( min(len(unique_recos), h_nTrk[2]-0.01), min(len(unique_trks), nTrk_bins[2]-0.01) )

        ## Find hits not associated with any EMTF tracks
        for iHit in range(nHits):
            Hit = Hits.at(iHit)
            if Hit.BX() != 0: continue
            unique_hit_1 = True
            for jTrk in range(nTrks):
                for jHit in range(Trks.at(jTrk).PtrHits().size()):
                    if HitsMatch( Hit, Trks.at(jTrk).PtrHits().at(jHit) ):
                        unique_hit_1 = False

            if unique_hit_1: 
                unique_hits_1.append(iHit)
                hits_in_sect_1[Hit.Sector_index()] += 1

        ## Sort hits by station
        for iSt in range(4):
            for iHit in unique_hits_1:
                Hit = Hits.at(iHit)
                if Hit.Station() == iSt+1:
                    unique_hits_2.append(iHit)

        ## Find hits in closest station, not exceeding 3 tracks + hits per sector
        for iHit in unique_hits_2:
            Hit = Hits.at(iHit)

            if trks_in_sect[Hit.Sector_index()] + hits_in_sect_3[Hit.Sector_index()] < 3:
                hits_in_sect_3[Hit.Sector_index()] += 1
                unique_hits_3.append(iHit)
                h_hit_phi.Fill( Hit.Phi_glob_rad() )
                h_hit_eta.Fill( Hit.Eta() )
                h_hit_stat.Fill( Hit.Station() )

        numHits[min(len(unique_hits_3), numLen-1)] += 1
        h_nHit.Fill( min(len(unique_hits_3), nHit_bins[2]-0.01) )
        h_nHit_vs_nTrk.Fill( min(len(unique_trks), h_nHit[2]-0.01), min(len(unique_hits_3), nHit_bins[2]-0.01) )

        ## Find tracks and hits closest to GEN muons
        dR_trk_gens = []
        for iGen in unique_gens:
            Gen = Gens.at(iGen)
            for iTrk in unique_trks:
                Trk = Trks.at(iTrk)
                dR_trk_gens.append( CalcDR( Gen.eta(), Gen.phi(), Trk.Eta(), Trk.Phi_glob_rad() ) )
        dR_hit_gens = []
        for iGen in unique_gens:
            Gen = Gens.at(iGen)
            for iHit in unique_hits_3:
                Hit = Hits.at(iHit)
                dR_hit_gens.append( CalcDR( Gen.eta(), Gen.phi(), Hit.Eta(), Hit.Phi_glob_rad() ) )
        
        ## Track number of trigger legs fired
        SingleMu_leg = 0
        DoubleMu_leg = 0
        MuOpen_leg = 0
        LCT_leg = 0
        SingleMu_22_leg = 0
        DoubleMu_12_leg = 0
        DoubleMu_5_leg = 0
        LCT_St1_leg = 0

        used_trks = []
        used_hits = []
        trk_matched_gens = []
        hit_matched_gens = []
        ## Find EMTF track that best matches the GEN muon
        for iDR in sorted(dR_trk_gens):
            for iGen in unique_gens:
                Gen = Gens.at(iGen)
                for iTrk in unique_trks:
                    if iTrk in used_trks: continue
                    if iGen in trk_matched_gens: continue
                    Trk = Trks.at(iTrk)
                    dR_trk = CalcDR( Gen.eta(), Gen.phi(), Trk.Eta(), Trk.Phi_glob_rad() ) 
                    if dR_trk == iDR:
                        used_trks.append(iTrk)
                        trk_matched_gens.append(iGen)
                        dPhi_trk = CalcDPhi( Gen.phi(), Trk.Phi_glob_rad() ) * Gen.charge()
                        dEta_trk = Trk.Eta() - Gen.eta()

                        if dR_trk > dR_bins[1] and dR_trk < dR_bins[2]: h_trk_gen_dR.Fill(dR_trk)
                        else: h_trk_gen_dR.Fill(dR_bins[2]-0.01)
                        if dPhi_trk > dPhi_bins[1] and dPhi_trk < dPhi_bins[2]: h_trk_gen_dPhi.Fill(dPhi_trk)
                        else: h_trk_gen_dPhi.Fill(dPhi_bins[2]-0.01)
                        if dEta_trk > dEta_bins[1] and dEta_trk < dEta_bins[2]: h_trk_gen_dEta.Fill(dEta_trk)
                        else: h_trk_gen_dEta.Fill(dEta_bins[2]-0.01)

                        if Trk.Quality() >= 12:
                            SingleMu_leg += 1
                            if Trk.Pt() >= 22: SingleMu_22_leg += 1
                        if Trk.Quality() >= 8:
                            DoubleMu_leg += 1
                            if Trk.Pt() >= 5: DoubleMu_5_leg += 1
                            if Trk.Pt() >= 12: DoubleMu_12_leg += 1
                        if Trk.Quality() >= 4:
                            MuOpen_leg += 1


        for iGen in unique_gens:
            Gen = Gens.at(iGen)
            if not iGen in trk_matched_gens:
                h_trk_gen_dR.Fill(dR_bins[1]+0.01)
                h_trk_gen_dPhi.Fill(dPhi_bins[1]+0.01)
                h_trk_gen_dEta.Fill(dEta_bins[1]+0.01)
                        
        ## If no track is found, find the EMTF hit that best matches the GEN muon
        for iDR in sorted(dR_hit_gens):
            for iGen in unique_gens:
                if iGen in trk_matched_gens: continue
                Gen = Gens.at(iGen)
                for iHit in unique_hits_3:
                    if iHit in used_hits: continue
                    if iGen in hit_matched_gens: continue
                    Hit = Hits.at(iHit)
                    dR_hit = CalcDR( Gen.eta(), Gen.phi(), Hit.Eta(), Hit.Phi_glob_rad() ) 
                    if dR_hit == iDR:
                        used_hits.append(iHit)
                        hit_matched_gens.append(iGen)
                        dPhi_hit = CalcDPhi( Gen.phi(), Hit.Phi_glob_rad() ) * Gen.charge()
                        dEta_hit = Hit.Eta() - Gen.eta()

                        if dR_hit > dR_bins[1] and dR_hit < dR_bins[2]: h_hit_gen_dR.Fill(dR_hit)
                        else: h_hit_gen_dR.Fill(dR_bins[2]-0.01)
                        if dPhi_hit > dPhi_bins[1] and dPhi_hit < dPhi_bins[2]: h_hit_gen_dPhi.Fill(dPhi_hit)
                        else: h_hit_gen_dPhi.Fill(dPhi_bins[2]-0.01)
                        if dEta_hit > dEta_bins[1] and dEta_hit < dEta_bins[2]: h_hit_gen_dEta.Fill(dEta_hit)
                        else: h_hit_gen_dEta.Fill(dEta_bins[2]-0.01)

                        LCT_leg += 1
                        if Hit.Station() == 1: LCT_St1_leg += 1

        for iGen in unique_gens:
            Gen = Gens.at(iGen)
            if not iGen in trk_matched_gens and not iGen in hit_matched_gens:
                h_hit_gen_dR.Fill(dR_bins[1]+0.01)
                h_hit_gen_dPhi.Fill(dPhi_bins[1]+0.01)
                h_hit_gen_dEta.Fill(dEta_bins[1]+0.01)

        if SingleMu_leg > 0: SingleMu_0 += 1
        if DoubleMu_leg > 0: SingleMu_Q8_0 += 1
        if MuOpen_leg > 0: SingleMu_Q4_0 += 1
        if DoubleMu_leg > 1: DoubleMu_0 += 1
        if MuOpen_leg > 1: DoubleMu_Q4_0 += 1
        if DoubleMu_leg > 2: TripleMu_0 += 1
        if MuOpen_leg > 2: TripleMu_Q4_0 += 1
        if SingleMu_22_leg > 0: SingleMu_22 += 1
        if DoubleMu_12_leg > 0 and DoubleMu_5_leg > 1: DoubleMu_12_5 += 1
        if DoubleMu_leg > 1 and LCT_leg > 0: DoubleMu_0_LCT += 1
        if DoubleMu_leg > 1 and LCT_St1_leg > 0: DoubleMu_0_LCT_St1 += 1
        if MuOpen_leg > 1 and LCT_leg > 0: DoubleMu_Q4_0_LCT += 1
        if MuOpen_leg > 1 and LCT_St1_leg > 0: DoubleMu_Q4_0_LCT_St1 += 1

        if (DoubleMu_leg > 2) or (DoubleMu_leg > 1 and LCT_St1_leg): TripleMu_0_OR_DoubleMu_0_LCT_St1 += 1
        if (MuOpen_leg > 2) or (MuOpen_leg > 1 and LCT_leg > 0): TripleMu_Q4_0_OR_DoubleMu_Q4_0_LCT += 1

    ## End loop over events



    print '*******************************************************'
    print '*****        Track and hit multiplicities         *****'
    print '*******************************************************'
    print '      GEN muons  -  RECO muons  -  Tracks  -  Hits'
    for i in range(numLen):
        print '%2d %12d %12d %11d %9d' % (i, numGens[i], numRecos[i], numTrks[i], numHits[i])

    print '****************************************'
    print '*****    Triggered event yields    *****'
    print '****************************************'
    print 'SingleMu_0             %6d     %.1f%%' % (SingleMu_0, 100.0*SingleMu_0/nEvt)
    print 'SingleMu_Q8_0          %6d     %.1f%%' % (SingleMu_Q8_0, 100.0*SingleMu_Q8_0/nEvt)
    print 'SingleMu_Q4_0          %6d     %.1f%%' % (SingleMu_Q4_0, 100.0*SingleMu_Q4_0/nEvt)
    print 'DoubleMu_0             %6d     %.1f%%' % (DoubleMu_0, 100.0*DoubleMu_0/nEvt)
    print 'DoubleMu_Q4_0          %6d     %.1f%%' % (DoubleMu_Q4_0, 100.0*DoubleMu_Q4_0/nEvt)
    print 'TripleMu_0             %6d     %.1f%%' % (TripleMu_0, 100.0*TripleMu_0/nEvt)
    print 'TripleMu_Q4_0          %6d     %.1f%%' % (TripleMu_Q4_0, 100.0*TripleMu_Q4_0/nEvt)
    print 'SingleMu_22            %6d     %.1f%%' % (SingleMu_22, 100.0*SingleMu_22/nEvt)
    print 'DoubleMu_12_5          %6d     %.1f%%' % (DoubleMu_12_5, 100.0*DoubleMu_12_5/nEvt)
    print 'DoubleMu_0_LCT         %6d     %.1f%%' % (DoubleMu_0_LCT, 100.0*DoubleMu_0_LCT/nEvt)
    print 'DoubleMu_0_LCT_St1     %6d     %.1f%%' % (DoubleMu_0_LCT_St1, 100.0*DoubleMu_0_LCT_St1/nEvt)
    print 'DoubleMu_Q4_0_LCT      %6d     %.1f%%' % (DoubleMu_Q4_0_LCT, 100.0*DoubleMu_Q4_0_LCT/nEvt)
    print 'DoubleMu_Q4_0_LCT_St1  %6d     %.1f%%' % (DoubleMu_Q4_0_LCT_St1, 100.0*DoubleMu_Q4_0_LCT_St1/nEvt)
    print ''
    print 'TripleMu_0_OR_DoubleMu_0_LCT_St1      %6d     %.1f%%' % (TripleMu_0_OR_DoubleMu_0_LCT_St1, 100.0*TripleMu_0_OR_DoubleMu_0_LCT_St1/nEvt)
    print 'TripleMu_Q4_0_OR_DoubleMu_Q4_0_LCT    %6d     %.1f%%' % (TripleMu_Q4_0_OR_DoubleMu_Q4_0_LCT, 100.0*TripleMu_Q4_0_OR_DoubleMu_Q4_0_LCT/nEvt)

    out_file.cd()

    h_nGen.GetXaxis().SetTitle('Number of GEN muons')
    h_nGen.Write()
    h_gen_pT.GetXaxis().SetTitle('pT')
    h_gen_pT.Write()
    h_gen_phi.GetXaxis().SetTitle('phi')
    h_gen_phi.Write()
    h_gen_eta.GetXaxis().SetTitle('eta')
    h_gen_eta.Write()

    h_nReco.GetXaxis().SetTitle('Number of RECO muons')
    h_nReco.Write()
    h_reco_pT.GetXaxis().SetTitle('pT')
    h_reco_pT.Write()
    h_reco_phi.GetXaxis().SetTitle('phi')
    h_reco_phi.Write()
    h_reco_eta.GetXaxis().SetTitle('eta')
    h_reco_eta.Write()

    h_nTrk.GetXaxis().SetTitle('Number of unique EMTF tracks')
    h_nTrk.Write()
    h_trk_pT.GetXaxis().SetTitle('pT')
    h_trk_pT.Write()
    h_trk_phi.GetXaxis().SetTitle('phi')
    h_trk_phi.Write()
    h_trk_eta.GetXaxis().SetTitle('eta')
    h_trk_eta.Write()
    h_trk_mode.GetXaxis().SetTitle('Mode')
    h_trk_mode.Write()
    h_trk_qual.GetXaxis().SetTitle('Quality')
    h_trk_qual.Write()

    h_nHit.GetXaxis().SetTitle('Number of unique EMTF hits (LCTs)')
    h_nHit.Write()
    h_hit_phi.GetXaxis().SetTitle('phi')
    h_hit_phi.Write()
    h_hit_eta.GetXaxis().SetTitle('eta')
    h_hit_eta.Write()
    h_hit_stat.GetXaxis().SetTitle('Station')
    h_hit_stat.Write()

    h_nTrk_vs_nGen.GetXaxis().SetTitle('Number of GEN muons')
    h_nTrk_vs_nGen.GetYaxis().SetTitle('Number of unique EMTF tracks')
    h_nTrk_vs_nGen.Write()
    h_nTrk_vs_nReco.GetXaxis().SetTitle('Number of RECO muons')
    h_nTrk_vs_nReco.GetYaxis().SetTitle('Number of unique EMTF tracks')
    h_nTrk_vs_nReco.Write()
    h_nHit_vs_nTrk.GetXaxis().SetTitle('Number of unique EMTF tracks')
    h_nHit_vs_nTrk.GetYaxis().SetTitle('Number of unique EMTF hits (LCTs)')
    h_nHit_vs_nTrk.Write()

    h_trk_gen_dR.Write()
    h_trk_gen_dR.GetXaxis().SetTitle('dR(EMTF track, GEN muon)')
    h_trk_gen_dPhi.Write()
    h_trk_gen_dPhi.GetXaxis().SetTitle('dPhi(EMTF track, GEN muon) x GEN charge')
    h_trk_gen_dEta.Write()
    h_trk_gen_dEta.GetXaxis().SetTitle('dEta(EMTF track, GEN muon)')

    h_hit_gen_dR.Write()
    h_hit_gen_dR.GetXaxis().SetTitle('dR(EMTF hit, GEN muon)')
    h_hit_gen_dPhi.Write()
    h_hit_gen_dPhi.GetXaxis().SetTitle('dPhi(EMTF hit, GEN muon) x GEN charge')
    h_hit_gen_dEta.Write()
    h_hit_gen_dEta.GetXaxis().SetTitle('dEta(EMTF hit, GEN muon)')

    out_file.Close()

    del tree
    file.Close()

if __name__ == '__main__':
    main()

