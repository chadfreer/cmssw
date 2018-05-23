#! /usr/bin/env python

## Compare hits coming out of EMTF and CSCTF

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside csctf_vs_emtf_hits'

    # file_name_1 = '../NTupleMaker/EMTF_Tree_ZMu_274442_csctfDigis_1k.root'
    # file_name_2 = '../NTupleMaker/EMTF_Tree_ZMu_274442_emtfStage2Digis_1k.root'
    # file_name_1 = '../NTupleMaker/EMTF_Tree_ZMu_276282_csctfDigis_4k.root'
    # file_name_2 = '../NTupleMaker/EMTF_Tree_ZMu_276282_emtfStage2Digis_4k.root'
    # file_name_1 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_14/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_SingleMuon_csctfDigis_278017_80k_BC.root'
    # file_name_2 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_14/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_SingleMuon_278017_80k_BC.root'

    # file_name_1 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_18/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_DoubleMuon_279116_2nd_LCT_Sector_m6_csctfDigis.root'
    # file_name_2 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_18/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_DoubleMuon_279116_2nd_LCT_Sector_m6_v2.root'

    # file_name_1 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_19/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_ExpressPhysics_279116_10k_csctfDigis.root'
    # file_name_2 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_19/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_ExpressPhysics_279116_10k.root'

    # file_name_1 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_19/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_ExpressPhysics_280363_10k_csctfDigis_067A.root'
    # file_name_2 = '/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_19/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_ExpressPhysics_280363_10k_067A.root'

    file_name_1 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/csctf_vs_emtf/EMTF_Tree_ExpressPhysics_281707_csctfDigis_40k_ABCD.root'
    file_name_2 = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/csctf_vs_emtf/EMTF_Tree_ExpressPhysics_281707_40k_ABCD.root'

    # out_file = TFile('plots/csctf_vs_emtf_hits_279024.root','recreate')
    # out_file = TFile('plots/csctf_vs_emtf_hits_279116.root','recreate')
    # out_file = TFile('plots/csctf_vs_emtf_hits_280363_preFix.root','recreate')
    out_file = TFile('plots/csctf_vs_emtf_hits_281707.root','recreate')

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

    numHits[0] = 0
    numHitsUnm[0] = 0
    numHitsUnmExist[0] = 0

    numHits[1] = 0
    numHitsUnm[1] = 0
    numHitsUnmExist[1] = 0
    
    nMatch_0_ME = {}
    nMatch_1_ME = {}
    nMatch_2_ME = {}
    nMatch_0_ME_neig = {}
    nMatch_1_ME_neig = {}
    nMatch_2_ME_neig = {}

    for iSt in range(4):
        nMatch_0_ME[iSt+1] = 0
        nMatch_1_ME[iSt+1] = 0
        nMatch_2_ME[iSt+1] = 0
        nMatch_0_ME_neig[iSt+1] = 0
        nMatch_1_ME_neig[iSt+1] = 0
        nMatch_2_ME_neig[iSt+1] = 0

    csctf_ch = {}
    emtf_ch = {}
    for iEnd in range(2):
        csctf_ch[iEnd] = {}
        emtf_ch[iEnd] = {}
        for iSt in range(4):
            csctf_ch[iEnd][iSt] = {}
            emtf_ch[iEnd][iSt] = {}
            for iSect in range(6):
                csctf_ch[iEnd][iSt][iSect] = {}
                emtf_ch[iEnd][iSt][iSect] = {}
                for iId in range(9):
                    csctf_ch[iEnd][iSt][iSect][iId] = [0, 0]
                    emtf_ch[iEnd][iSt][iSect][iId] = [0, 0]

    ###################
    ### Book histograms
    ###################

    CSC_ID_bins = [9, 0.5, 9.5]
    st_bins = [9, -4.5, 4.5]
    sect_bins = [13, -6.5, 6.5]
    sect_ID_bins = [54, 0.5, 54.5]
    bx_bins = [7, -3.5, 3.5]
    wire_bins = [130, -1.5, 128.5]
    strip_bins = [258, -1.5, 256.5]
    occ_bins = [21, -0.5, 20.5]
    
    h_matched = TH2D('h_matched', 'Matched hits', st_bins[0], st_bins[1], st_bins[2], CSC_ID_bins[0], CSC_ID_bins[1], CSC_ID_bins[2])
    h_missing = TH2D('h_missing', 'Missing hits', st_bins[0], st_bins[1], st_bins[2], CSC_ID_bins[0], CSC_ID_bins[1], CSC_ID_bins[2])
    h_matched_sect_ID = TH2D('h_matched_sect_ID', 'Matched hits', sect_ID_bins[0], sect_ID_bins[1], sect_ID_bins[2], st_bins[0], st_bins[1], st_bins[2])
    h_missing_sect_ID = TH2D('h_missing_sect_ID', 'Missing hits', sect_ID_bins[0], sect_ID_bins[1], sect_ID_bins[2], st_bins[0], st_bins[1], st_bins[2])
    h_matched_bx = TH1D('h_matched_bx', 'Matched hits bx', bx_bins[0], bx_bins[1], bx_bins[2])
    h_missing_bx = TH1D('h_missing_bx', 'Missing hits bx', bx_bins[0], bx_bins[1], bx_bins[2])
    h_matched_wire = TH1D('h_matched_wire', 'Matched hits wire', wire_bins[0], wire_bins[1], wire_bins[2])
    h_missing_wire = TH1D('h_missing_wire', 'Missing hits wire', wire_bins[0], wire_bins[1], wire_bins[2])
    h_matched_strip = TH1D('h_matched_strip', 'Matched hits strip', strip_bins[0], strip_bins[1], strip_bins[2])
    h_missing_strip = TH1D('h_missing_strip', 'Missing hits strip', strip_bins[0], strip_bins[1], strip_bins[2])
    h_matched_id3_wire = TH1D('h_matched_id3_wire', 'Matched hits in station 1, CSC ID 1-3', wire_bins[0], wire_bins[1], wire_bins[2])
    h_missing_id3_wire = TH1D('h_missing_id3_wire', 'Missing hits in station 1, CSC ID 1-3', wire_bins[0], wire_bins[1], wire_bins[2])
    h_matched_id9_wire = TH1D('h_matched_id9_wire', 'Matched hits in station 1, CSC ID 6-9', wire_bins[0], wire_bins[1], wire_bins[2])
    h_missing_id9_wire = TH1D('h_missing_id9_wire', 'Missing hits in station 1, CSC ID 6-9', wire_bins[0], wire_bins[1], wire_bins[2])
    h_matched_occ_sect = TH1D('h_matched_occ_sect', 'Matched hits', occ_bins[0], occ_bins[1], occ_bins[2])
    h_missing_occ_sect = TH1D('h_missing_occ_sect', 'Missing hits', occ_bins[0], occ_bins[1], occ_bins[2])
    h_matched_occ_stat = TH1D('h_matched_occ_stat', 'Matched hits', occ_bins[0], occ_bins[1], occ_bins[2])
    h_missing_occ_stat = TH1D('h_missing_occ_stat', 'Missing hits', occ_bins[0], occ_bins[1], occ_bins[2])
    h_matched_occ_chamb = TH1D('h_matched_occ_chamb', 'Matched hits', occ_bins[0], occ_bins[1], occ_bins[2])
    h_missing_occ_chamb = TH1D('h_missing_occ_chamb', 'Missing hits', occ_bins[0], occ_bins[1], occ_bins[2])
    h_matched_evt = TH1D('h_matched_evt', 'Matched hits', 18000, 0, 1800000000)
    h_missing_evt = TH1D('h_missing_evt', 'Missing hits', 18000, 0, 1800000000)
    h_matched_sect_vs_evt = TH2D('h_matched_sect_vs_evt', 'Matched hits', 18000, 0, 1800000000, sect_bins[0], sect_bins[1], sect_bins[2])
    h_missing_sect_vs_evt = TH2D('h_missing_sect_vs_evt', 'Missing hits', 18000, 0, 1800000000, sect_bins[0], sect_bins[1], sect_bins[2])
    h_matched_lumi = TH1D('h_matched_lumi', 'Matched hits', 1200, 0, 1200)
    h_missing_lumi = TH1D('h_missing_lumi', 'Missing hits', 1200, 0, 1200)
    h_matched_sect_vs_lumi = TH2D('h_matched_sect_vs_lumi', 'Matched hits', 1200, 0, 1200, sect_bins[0], sect_bins[1], sect_bins[2])
    h_missing_sect_vs_lumi = TH2D('h_missing_sect_vs_lumi', 'Missing hits', 1200, 0, 1200, sect_bins[0], sect_bins[1], sect_bins[2])

    ## Main event loop    
    for iEvt in range(tree_1.GetEntries()):

        # if iEvt > 1000: break
        # if (iEvt < 5500 or iEvt > 6700): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt
        tree_1.GetEntry(iEvt)
        tree_2.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = tree_1.EventAuxiliary
        Hits_1 = tree_1.l1tEMTFHits_simEmtfDigis__L1TMuonEmulation
        Hits_2 = tree_2.l1tEMTFHits_simEmtfDigis__L1TMuonEmulation ## EMTFHits from emulator, originally LCTs from unpacker
        ## Hits_2 = tree_2.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation ## EMTFHits directly from unpacker
        Trks_1 = tree_1.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        Trks_2 = tree_2.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        DAQ_2 = tree_2.l1tEMTFDaqOuts_emtfStage2Digis__L1TMuonEmulation
        LegTrks = tree_1.cscL1TrackCSCDetIdCSCCorrelatedLCTDigiMuonDigiCollectionstdpairs_csctfDigis__L1TMuonEmulation
        
        nHits1 = Hits_1.size()
        nHits2 = Hits_2.size()
        nTrks1 = Trks_1.size()
        nTrks2 = Trks_2.size()
        nLegTrks = LegTrks.size()

        if (nHits1 == 0 and nHits2 == 0): continue

        nHitsSec6_csctf = 0
        nHitsSec6_emtf = 0
        nTrksSec6 = 0
                
        # for iHit1 in range(nHits1):
        #     Hit1 = Hits_1.at(iHit1)
        #     if Hit1.Endcap() == -1 and Hit1.Sector() == 6 and Hit1.BX() == -3:
        #         nHitsSec6_csctf += 1
        # for iHit2 in range(nHits2):
        #     Hit2 = Hits_2.at(iHit2)
        #     if Hit2.Endcap() == -1 and Hit2.Sector() == 6 and Hit2.BX() == -3:
        #         nHitsSec6_emtf += 1
        # for iTrk2 in range(nTrks2):
        #     Trk2 = Trks_2.at(iTrk2)
        #     if Trk2.Endcap() == -1 and Trk2.Sector() == 6 and Trk2.BX() == -3:
        #         nTrksSec6 += 1
        # if nHitsSec6_emtf > 0 and nHitsSec6_csctf > 0:
        #     print 'Non-buggy event: %d EMTF LCTs (%d CSCTF LCTs) and %d EMTF tracks in sector -6' % (nHitsSec6_emtf, nHitsSec6_csctf, nTrksSec6)


        ## Check that CSCTF hits have match in EMTF
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            if abs(Hit1.BX()) > 1: continue  ## Only check BX = {-1,0,1} for now
            # if Hit1.BX() > 3: continue  
            if Hit1.Neighbor() == 1: continue
            if Hit1.Endcap() == 1 and (Hit1.Ring() == 1 or Hit1.Ring() == 4) and Hit1.Chamber() == 36: continue
            numHits[0] += 1

            nSector = 0
            nStation = 0
            nChamber = 0
            for jHit1 in range(nHits1):
                if jHit1 == iHit1: continue
                if Hits_1.at(jHit1).Neighbor() == 0:
                    if Hit1.Endcap() * Hit1.Sector() == Hits_1.at(jHit1).Endcap() * Hits_1.at(jHit1).Sector():
                        nSector += 1
                        if Hit1.Station() == Hits_1.at(jHit1).Station():
                            nStation += 1
                    if HitsMatchChamber( Hit1, Hits_1.at(jHit1) ):
                        nChamber += 1

            good_chamber = True
            # if ( (Hit1.Endcap() == 1 and Hit1.Station() == 2 and (Hit1.CSC_ID() == 6 or Hit1.CSC_ID() == 1)) or
            #      (Hit1.Endcap() == -1 and Hit1.Station() == 2 and (Hit1.CSC_ID() == 2 or Hit1.CSC_ID() == 1)) ):
            #     good_chamber = False
            
            match_exists = False
            match_strip_wire = False
            match_exists_no_bx = False
            match_bx = False
            match_endcap = False
            match_sector = False
            match_sector_station = False
            match_chamber = False
            match_chamber_no_cscID = False
            match_1_ME = False
            match_2_ME = False

            for iDaq in range( DAQ_2.size() ):
                ME_2 = DAQ_2.at(iDaq).GetMECollection()
                for iME in range(ME_2.size()):
                    ME =  ME_2.at(iME)
                    ## Most common mis-match is BX mis-match.  In cases of ambiguous strip/wire pairings, only one may match.
                    # if ( ME.Strip() == Hit1.Strip() and ME.Wire() == Hit1.Wire() and ME.TBIN() == Hit1.BX() + 3 ):
                    if ( ME.Strip() == Hit1.Strip() or ME.Wire() == Hit1.Wire() ): ## and ME.TBIN() == Hit1.BX() + 3 ):
                        if ( ME.Station() > 0 and ME.Station() < 5):
                            if ( ME.Station() == Hit1.Station() and ME.CSC_ID() == Hit1.CSC_ID() ):
                                if (match_1_ME): match_2_ME = True
                                match_1_ME = True
                        elif ( ME.Station() == 0 and Hit1.Station() == 1 and ME.CSC_ID() == Hit1.CSC_ID() ):
                            if (match_1_ME): match_2_ME = True
                            match_1_ME = True
                        elif ( ME.Station() == 5 and 
                               ( (ME.CSC_ID() == 1 and Hit1.Station() == 1 and Hit1.CSC_ID() == 3) or 
                                 (ME.CSC_ID() == 2 and Hit1.Station() == 1 and Hit1.CSC_ID() == 6) or 
                                 (ME.CSC_ID() == 3 and Hit1.Station() == 1 and Hit1.CSC_ID() == 9) or 
                                 (ME.CSC_ID() == 4 and Hit1.Station() == 2 and Hit1.CSC_ID() == 3) or 
                                 (ME.CSC_ID() == 5 and Hit1.Station() == 2 and Hit1.CSC_ID() == 9) or 
                                 (ME.CSC_ID() == 6 and Hit1.Station() == 3 and Hit1.CSC_ID() == 3) or 
                                 (ME.CSC_ID() == 7 and Hit1.Station() == 3 and Hit1.CSC_ID() == 9) or 
                                 (ME.CSC_ID() == 8 and Hit1.Station() == 4 and Hit1.CSC_ID() == 3) or 
                                 (ME.CSC_ID() == 9 and Hit1.Station() == 4 and Hit1.CSC_ID() == 9) ) ):
                            if (match_1_ME): match_2_ME = True
                            match_1_ME = True


            if ( ( Hit1.Station() == 1 and Hit1.Subsector() == 2 and Hit1.CSC_ID() % 3 == 0 ) or
                 ( Hit1.Station() > 1 and (Hit1.CSC_ID() == 3 or Hit1.CSC_ID() == 9) ) ):
                if (match_2_ME): nMatch_2_ME_neig[Hit1.Station()] += 1
                elif (match_1_ME): nMatch_1_ME_neig[Hit1.Station()] += 1
                else: nMatch_0_ME_neig[Hit1.Station()] += 1

                if (match_1_ME and not match_2_ME): True
            #         # print '\n******* CSCTF neighbor-chamber hit in event %d has no match *******' % iEvt
            #         # PrintEMTFHit( Hit1 )
                    
            #         # print 'EMTF hits in event:'
            #         # for iHit2 in range(nHits2):
            #         #     if Hits_2.at(iHit2).BX() != 0: continue
            #         #     if Hits_2.at(iHit2).Neighbor() == 1: continue
            #         #     PrintEMTFHit( Hits_2.at(iHit2) )
            #         # print 'Other CSCTF hits in event:'
            #         # for jHit1 in range(nHits1):
            #         #     if Hits_1.at(jHit1).BX() != 0: continue
            #         #     if Hits_1.at(jHit1).Neighbor() == 1: continue
            #         #     if (jHit1 != iHit1): PrintEMTFHit( Hits_1.at(jHit1) )

            #         # print 'EMTF tracks in event:'
            #         # for iTrk2 in range(nTrks2):
            #         #     PrintEMTFTrack( Trks_2.at(iTrk2) )

            #         # print 'CSCTF tracks in event:'
            #         # for iLegTrk in range(nLegTrks):
            #         #     LegTrk = LegTrks.at(iLegTrk).first
            #         #     print 'BX = %d, endcap = %d, sector = %d, me1ID = %d, me1Tbin = %d,' % ( LegTrk.BX(), LegTrk.endcap(), LegTrk.sector(), LegTrk.me1ID(), LegTrk.me1Tbin() ), \
            #         #         'me2ID = %d, me2Tbin = %d, me3ID = %d, me3Tbin = %d, me4ID = %d, me4Tbin = %d' % ( LegTrk.me2ID(), LegTrk.me2Tbin(), LegTrk.me3ID(), LegTrk.me3Tbin(), LegTrk.me4ID(), LegTrk.me4Tbin() )

            #         # for iDaq in range( DAQ_2.size() ):
            #         #     print '\nEMTF DAQ output #%d' % (iDaq+1) 
            #         #     EvtHd_2 = DAQ_2.at(iDaq).GetEventHeader()
            #         #     PrintEventHeaderHeader()
            #         #     PrintEventHeader( EvtHd_2 )
                        
            #         #     ME_2 = DAQ_2.at(iDaq).GetMECollection()
            #         #     if (ME_2.size() > 0): PrintMEHeader()
            #         #     else: print 'No ME output'
            #         #     for iME in range(ME_2.size()):
            #         #         PrintME( ME_2.at(iME) )

            #             # SP_2 = DAQ_2.at(iDaq).GetSPCollection()
            #             # if (SP_2.size() > 0): PrintSPHeader()
            #             # else: print 'No SP output'
            #             # for iSP in range(SP_2.size()):
            #             #     PrintSP( SP_2.at(iSP) )
            #         # print '***********************************************'

            else:
                if (match_2_ME): nMatch_2_ME[Hit1.Station()] += 1
                elif (match_1_ME): nMatch_1_ME[Hit1.Station()] += 1
                else: nMatch_0_ME[Hit1.Station()] += 1

            for iHit2 in range(nHits2):
                Hit2 = Hits_2.at(iHit2)
                if HitsMatch( Hit1, Hit2 ): match_exists = True
                if HitsMatchChamber( Hit1, Hit2 ) and ( (Hit1.Wire() == Hit2.Wire()) or (Hit1.Strip() == Hit2.Strip()) ): match_strip_wire = True
                if HitsMatchNoBX( Hit1, Hit2 ): match_exists_no_bx = True
                if HitsMatchChamber( Hit1, Hit2 ): match_chamber = True
                if ( Hit1.BX() == Hit2.BX() and Hit1.Endcap() == Hit2.Endcap() and Hit1.Station() == Hit2.Station() and 
                     Hit1.Sector() == Hit2.Sector() and Hit1.Subsector() == Hit2.Subsector() ): match_chamber_no_cscID = True
                if ( Hit1.BX() == Hit2.BX() ): match_bx = True
                if ( Hit1.Endcap() == Hit2.Endcap() ): match_endcap = True
                if ( Hit1.Endcap() == Hit2.Endcap() and Hit1.Sector() == Hit2.Sector() ): match_sector = True
                if ( Hit1.Endcap() == Hit2.Endcap() and Hit1.Sector() == Hit2.Sector() and Hit1.Station() == Hit2.Station() ): match_sector_station = True

            # if (not match_exists) and (not match_exists_no_bx) and good_chamber:
            csctf_ch[(Hit1.Endcap() > 0)][Hit1.Station()-1][Hit1.Sector()-1][Hit1.CSC_ID()-1][0] += 1
            if not match_exists_no_bx:
                csctf_ch[(Hit1.Endcap() > 0)][Hit1.Station()-1][Hit1.Sector()-1][Hit1.CSC_ID()-1][1] += 1
                # PrintEMTFHit(Hit1)
                numHitsUnm[0] += 1
                if (nHits2) > 0: numHitsUnmExist[0] += 1
                h_missing.Fill( Hit1.Station() * Hit1.Endcap(), Hit1.CSC_ID() )
                h_missing_evt.Fill( Event.event() )
                h_missing_sect_vs_evt.Fill( Event.event(), Hit1.Endcap() * Hit1.Sector() )
                h_missing_lumi.Fill( Event.luminosityBlock() )
                h_missing_sect_vs_lumi.Fill( Event.luminosityBlock(), Hit1.Endcap() * Hit1.Sector() )
                ## if ( Hit1.Station() == 1 ): 
                h_missing_sect_ID.Fill( Hit1.CSC_ID() + 9*(Hit1.Sector() - 1), Hit1.Station() * Hit1.Endcap() )
                h_missing_occ_sect.Fill( min(nSector, occ_bins[2] - 0.1) )
                h_missing_occ_stat.Fill( min(nStation, occ_bins[2] - 0.1) )
                h_missing_occ_chamb.Fill( min(nChamber, occ_bins[2] - 0.1) )
                h_missing_bx.Fill( Hit1.BX() )
                h_missing_strip.Fill( max( strip_bins[1]+0.01, min( strip_bins[2]-0.01, Hit1.Strip() ) ) )
                h_missing_wire.Fill( max( wire_bins[1]+0.01, min( wire_bins[2]-0.01, Hit1.Wire() ) ) )
                if (Hit1.CSC_ID() < 4): h_missing_id3_wire.Fill( max( wire_bins[1]+0.01, min( wire_bins[2]-0.01, Hit1.Wire() ) ) )
                if (Hit1.CSC_ID() > 6): h_missing_id9_wire.Fill( max( wire_bins[1]+0.01, min( wire_bins[2]-0.01, Hit1.Wire() ) ) )

                # print '\n******* CSCTF hit in event %d has no match *******' % iEvt
                # PrintEMTFHit( Hit1 )
                # print 'EMTF hits in event'
                # # print 'EMTF hits in sector %d' % (Hit1.Endcap()*Hit1.Sector())
                # for iHit2 in range(nHits2):
                #     ## if Hits_2.at(iHit2).BX() != 0: continue
                #     # if Hits_2.at(iHit2).Endcap()*Hits_2.at(iHit2).Sector() != Hit1.Endcap()*Hit1.Sector(): continue
                #     if Hits_2.at(iHit2).Neighbor() == 1: continue
                #     PrintEMTFHit( Hits_2.at(iHit2) )
                # print 'CSCTF hits in event'
                # # print 'CSCTF hits in sector %d' % (Hit1.Endcap()*Hit1.Sector())
                # for jHit1 in range(nHits1):
                #     ## if Hits_1.at(jHit1).BX() != 0: continue
                #     # if Hits_1.at(jHit1).Endcap()*Hits_1.at(jHit1).Sector() != Hit1.Endcap()*Hit1.Sector(): continue
                #     if Hits_1.at(jHit1).Neighbor() == 1: continue
                #     ## if (jHit1 != iHit1): 
                #     PrintEMTFHit( Hits_1.at(jHit1) )

                # print 'EMTF tracks in event:'
                # for iTrk2 in range(nTrks2):
                #     PrintEMTFTrack( Trks_2.at(iTrk2) )

                # print 'CSCTF tracks in event:'
                # for iLegTrk in range(nLegTrks):
                #     LegTrk = LegTrks.at(iLegTrk).first
                #     print 'BX = %d, endcap = %d, sector = %d, me1ID = %d, me1Tbin = %d,' % ( LegTrk.BX(), LegTrk.endcap(), LegTrk.sector(), LegTrk.me1ID(), LegTrk.me1Tbin() ), \
                #         'me2ID = %d, me2Tbin = %d, me3ID = %d, me3Tbin = %d, me4ID = %d, me4Tbin = %d' % ( LegTrk.me2ID(), LegTrk.me2Tbin(), LegTrk.me3ID(), LegTrk.me3Tbin(), LegTrk.me4ID(), LegTrk.me4Tbin() )

                # for iDaq in range( DAQ_2.size() ):
                #     print '\nEMTF DAQ output #%d' % (iDaq+1) 
                #     EvtHd_2 = DAQ_2.at(iDaq).GetEventHeader()
                #     PrintEventHeaderHeader()
                #     PrintEventHeader( EvtHd_2 )

                #     ME_2 = DAQ_2.at(iDaq).GetMECollection()
                #     if (ME_2.size() > 0): PrintMEHeader()
                #     else: print 'No ME output'
                #     for iME in range(ME_2.size()):
                #         PrintME( ME_2.at(iME) )

                #     SP_2 = DAQ_2.at(iDaq).GetSPCollection()
                #     if (SP_2.size() > 0): PrintSPHeader()
                #     else: print 'No SP output'
                #     for iSP in range(SP_2.size()):
                #         PrintSP( SP_2.at(iSP) )
                # print '***********************************************'


            else:
                h_matched.Fill( Hit1.Station() * Hit1.Endcap(), Hit1.CSC_ID() )
                ## if (Hit1.Station() == 1): 
                h_matched_sect_ID.Fill( Hit1.CSC_ID() + 9*(Hit1.Sector() - 1), Hit1.Station() * Hit1.Endcap() )
                h_matched_occ_sect.Fill( min(nSector, occ_bins[2] - 0.1) )
                h_matched_occ_stat.Fill( min(nStation, occ_bins[2] - 0.1) )
                h_matched_occ_chamb.Fill( min(nChamber, occ_bins[2] - 0.1) )
                h_matched_evt.Fill( Event.event() )
                h_matched_sect_vs_evt.Fill( Event.event(), Hit1.Endcap() * Hit1.Sector() )
                h_matched_lumi.Fill( Event.luminosityBlock() )
                h_matched_sect_vs_lumi.Fill( Event.luminosityBlock(), Hit1.Endcap() * Hit1.Sector() )
                h_matched_bx.Fill( Hit1.BX() )
                h_matched_strip.Fill( max( strip_bins[1]+0.01, min( strip_bins[2]-0.01, Hit1.Strip() ) ) )
                h_matched_wire.Fill( max( wire_bins[1]+0.01, min( wire_bins[2]-0.01, Hit1.Wire() ) ) )
                if (Hit1.CSC_ID() < 4): h_matched_id3_wire.Fill( max( wire_bins[1]+0.01, min( wire_bins[2]-0.01, Hit1.Wire() ) ) )
                if (Hit1.CSC_ID() > 6): h_matched_id9_wire.Fill( max( wire_bins[1]+0.01, min( wire_bins[2]-0.01, Hit1.Wire() ) ) )

                    
        ## Check that EMTF hits have match in CSCTF
        for iHit2 in range(nHits2):
            Hit2 = Hits_2.at(iHit2)
            if abs(Hit2.BX()) > 1: continue  ## Only check BX = {-1,0,+1}
            # if Hit2.BX() > 3: continue
            if Hit2.Neighbor() == 1: continue
            if Hit2.Endcap() == 1 and (Hit2.Ring() == 1 or Hit2.Ring() == 4) and Hit2.Chamber() == 36: continue
            numHits[1] += 1
            
            good_chamber = True
            # if ( (Hit2.Endcap() == 1 and Hit2.Station() == 2 and (Hit2.CSC_ID() == 6 or Hit2.CSC_ID() == 1)) or
            #      (Hit2.Endcap() == -1 and Hit2.Station() == 2 and (Hit2.CSC_ID() == 2 or Hit2.CSC_ID() == 1)) ):
            #     good_chamber = False
            
            match_exists = False
            match_strip_wire = False
            match_exists_no_bx = False
            for iHit1 in range(nHits1):
                Hit1 = Hits_1.at(iHit1)
                if HitsMatch( Hit1, Hit2 ): match_exists = True
                if HitsMatchChamber( Hit1, Hit2 ) and ( (Hit1.Wire() == Hit2.Wire()) or (Hit1.Strip() == Hit2.Strip()) ): match_strip_wire = True
                if HitsMatchNoBX( Hit1, Hit2 ): match_exists_no_bx = True

            # if not match_exists and not match_exists_no_bx and good_chamber:
            emtf_ch[(Hit2.Endcap() > 0)][Hit2.Station()-1][Hit2.Sector()-1][Hit2.CSC_ID()-1][0] += 1
            if not match_exists_no_bx:
                emtf_ch[(Hit2.Endcap() > 0)][Hit2.Station()-1][Hit2.Sector()-1][Hit2.CSC_ID()-1][1] += 1
                numHitsUnm[1] += 1
                if (nHits1) > 0: numHitsUnmExist[1] += 1

                # print '\n******* EMTF hit in event %d has no match *******' % iEvt
                # PrintEMTFHit( Hit2 )
                # print 'CSCTF hits in event:'
                # for iHit1 in range(nHits1):
                #     PrintEMTFHit( Hits_1.at(iHit1) )
                # print '***********************************************'
                    

    print '*******************************************************'
    print '*******            The BIG picture              *******'
    print '*******************************************************'
    print '                          CSCTF  -  EMTF'
    print 'numHits:                %6d %11d' % (numHits[0], numHits[1]) 
    print 'numHitsUnm:             %6d %11d' % (numHitsUnm[0], numHitsUnm[1]) 
    print 'numHitsUnmExist:        %6d %11d' % (numHitsUnmExist[0], numHitsUnmExist[1]) 
    
    print '\n*******************************************************'
    print '*******       # of matched ME by station        *******'
    print '*******************************************************'
    print '                            1    -    2    -    3    -    4'
    print '0 matches:            %8d  %8d  %8d  %8d' % (nMatch_0_ME[1], nMatch_0_ME[2], nMatch_0_ME[3], nMatch_0_ME[4]) 
    print '1 matches:            %8d  %8d  %8d  %8d' % (nMatch_1_ME[1], nMatch_1_ME[2], nMatch_1_ME[3], nMatch_1_ME[4]) 
    print '2 matches:            %8d  %8d  %8d  %8d' % (nMatch_2_ME[1], nMatch_2_ME[2], nMatch_2_ME[3], nMatch_2_ME[4]) 
    print '0 matches neighbor:   %8d  %8d  %8d  %8d' % (nMatch_0_ME_neig[1], nMatch_0_ME_neig[2], nMatch_0_ME_neig[3], nMatch_0_ME_neig[4]) 
    print '1 matches neighbor:   %8d  %8d  %8d  %8d' % (nMatch_1_ME_neig[1], nMatch_1_ME_neig[2], nMatch_1_ME_neig[3], nMatch_1_ME_neig[4]) 
    print '2 matches neighbor:   %8d  %8d  %8d  %8d' % (nMatch_2_ME_neig[1], nMatch_2_ME_neig[2], nMatch_2_ME_neig[3], nMatch_2_ME_neig[4]) 


    # print '\n******* Chambers with no mismatches *******'
    # for iEnd in range(2):
    #     for iSt in range(4):
    #         for iSect in range(6):
    #             for iId in range(9):
    #                 if csctf_ch[iEnd][iSt][iSect][iId][0] == 0: continue
    #                 if csctf_ch[iEnd][iSt][iSect][iId][1] != 0: continue
    #                 if emtf_ch[iEnd][iSt][iSect][iId][0] == 0: continue
    #                 if emtf_ch[iEnd][iSt][iSect][iId][1] != 0: continue
    #                 print 'Endcap %d, station %d, sector %d, CSC ID %d has 0 mis-matches out of %d' % (iEnd, iSt+1, iSect+1, iId+1,
    #                                                                                                    csctf_ch[iEnd][iSt][iSect][iId][0])


    out_file.cd()

    h_missing.GetXaxis().SetTitle('Station x Endcap')
    h_missing.GetYaxis().SetTitle('CSC ID')
    h_missing.Write()

    h_matched.GetXaxis().SetTitle('Station x Endcap')
    h_matched.GetYaxis().SetTitle('CSC ID')
    h_matched.Write()

    h_matched.Add( h_missing )
    h_missing.Divide( h_matched )
    h_missing.Scale( 100. )
    h_missing.SetName('h_missing_pct')
    h_missing.SetTitle('Percentage of hits missing')
    h_missing.Write()

    h_missing_sect_ID.GetXaxis().SetTitle('Sector x 9 + CSC ID')
    h_missing_sect_ID.GetYaxis().SetTitle('Station x Endcap')
    h_missing_sect_ID.Write()

    h_matched_sect_ID.GetXaxis().SetTitle('Sector x 9 + CSC ID')
    h_matched_sect_ID.GetYaxis().SetTitle('Station x Endcap')
    h_matched_sect_ID.Write()

    h_matched_sect_ID.Add( h_missing_sect_ID )
    h_missing_sect_ID.Divide( h_matched_sect_ID )
    h_missing_sect_ID.Scale( 100. )
    h_missing_sect_ID.SetName('h_missing_pct_sect_ID')
    h_missing_sect_ID.SetTitle('Percentage of hits missing')
    h_missing_sect_ID.Write()

    h_missing_bx.GetXaxis().SetTitle('BX')
    h_missing_bx.SetLineWidth(2)
    h_missing_bx.SetLineColor(kRed)
    h_missing_bx.Write()

    h_matched_bx.GetXaxis().SetTitle('BX')
    h_matched_bx.SetLineWidth(2)
    h_matched_bx.SetLineColor(kBlue)
    h_matched_bx.Write()

    h_missing_strip.GetXaxis().SetTitle('Halfstrip')
    h_missing_strip.SetLineWidth(2)
    h_missing_strip.SetLineColor(kRed)
    h_missing_strip.Write()

    h_matched_strip.GetXaxis().SetTitle('Halfstrip')
    h_matched_strip.SetLineWidth(2)
    h_matched_strip.SetLineColor(kBlue)
    h_matched_strip.Write()

    h_missing_wire.GetXaxis().SetTitle('Keywire group')
    h_missing_wire.SetLineWidth(2)
    h_missing_wire.SetLineColor(kRed)
    h_missing_wire.Write()

    h_matched_wire.GetXaxis().SetTitle('Keywire group')
    h_matched_wire.SetLineWidth(2)
    h_matched_wire.SetLineColor(kBlue)
    h_matched_wire.Write()

    h_missing_id3_wire.GetXaxis().SetTitle('Keywire group')
    h_missing_id3_wire.SetLineWidth(2)
    h_missing_id3_wire.SetLineColor(kRed)
    h_missing_id3_wire.Write()

    h_matched_id3_wire.GetXaxis().SetTitle('Keywire group')
    h_matched_id3_wire.SetLineWidth(2)
    h_matched_id3_wire.SetLineColor(kBlue)
    h_matched_id3_wire.Write()

    h_matched_id3_wire.Add( h_missing_id3_wire )
    h_missing_id3_wire.Divide( h_matched_id3_wire )
    h_missing_id3_wire.Scale( 100. )
    h_missing_id3_wire.SetName('h_missing_pct_id3_wire')
    h_missing_id3_wire.SetTitle('Percentage of hits missing in CSC ID 1-3')
    h_missing_id3_wire.Write()

    h_missing_id9_wire.GetXaxis().SetTitle('Keywire group')
    h_missing_id9_wire.SetLineWidth(2)
    h_missing_id9_wire.SetLineColor(kRed)
    h_missing_id9_wire.Write()

    h_matched_id9_wire.GetXaxis().SetTitle('Keywire group')
    h_matched_id9_wire.SetLineWidth(2)
    h_matched_id9_wire.SetLineColor(kBlue)
    h_matched_id9_wire.Write()

    h_matched_id9_wire.Add( h_missing_id9_wire )
    h_missing_id9_wire.Divide( h_matched_id9_wire )
    h_missing_id9_wire.Scale( 100. )
    h_missing_id9_wire.SetName('h_missing_pct_id9_wire')
    h_missing_id9_wire.SetTitle('Percentage of hits missing in CSC ID 6-9')
    h_missing_id9_wire.Write()

    h_missing_occ_sect.GetXaxis().SetTitle('Number of hits in same sector')
    h_missing_occ_sect.SetLineWidth(2)
    h_missing_occ_sect.SetLineColor(kRed)
    h_missing_occ_sect.Write()

    h_matched_occ_sect.GetXaxis().SetTitle('Number of hits in same sector')
    h_matched_occ_sect.SetLineWidth(2)
    h_matched_occ_sect.SetLineColor(kBlue)
    h_matched_occ_sect.Write()

    h_matched_occ_sect.Add( h_missing_occ_sect )
    h_missing_occ_sect.Divide( h_matched_occ_sect )
    h_missing_occ_sect.Scale( 100. )
    h_missing_occ_sect.SetName('h_missing_pct_occ_sect')
    h_missing_occ_sect.SetTitle('Percentage of hits missing')
    h_missing_occ_sect.Write()

    h_missing_occ_stat.GetXaxis().SetTitle('Number of hits in same sector and station')
    h_missing_occ_stat.SetLineWidth(2)
    h_missing_occ_stat.SetLineColor(kRed)
    h_missing_occ_stat.Write()

    h_matched_occ_stat.GetXaxis().SetTitle('Number of hits in same sector and station')
    h_matched_occ_stat.SetLineWidth(2)
    h_matched_occ_stat.SetLineColor(kBlue)
    h_matched_occ_stat.Write()

    h_matched_occ_stat.Add( h_missing_occ_stat )
    h_missing_occ_stat.Divide( h_matched_occ_stat )
    h_missing_occ_stat.Scale( 100. )
    h_missing_occ_stat.SetName('h_missing_pct_occ_stat')
    h_missing_occ_stat.SetTitle('Percentage of hits missing')
    h_missing_occ_stat.Write()

    h_missing_occ_chamb.GetXaxis().SetTitle('Number of hits in same chamber')
    h_missing_occ_chamb.SetLineWidth(2)
    h_missing_occ_chamb.SetLineColor(kRed)
    h_missing_occ_chamb.Write()

    h_matched_occ_chamb.GetXaxis().SetTitle('Number of hits in same chamber')
    h_matched_occ_chamb.SetLineWidth(2)
    h_matched_occ_chamb.SetLineColor(kBlue)
    h_matched_occ_chamb.Write()

    h_matched_occ_chamb.Add( h_missing_occ_chamb )
    h_missing_occ_chamb.Divide( h_matched_occ_chamb )
    h_missing_occ_chamb.Scale( 100. )
    h_missing_occ_chamb.SetName('h_missing_pct_occ_chamb')
    h_missing_occ_chamb.SetTitle('Percentage of hits missing')
    h_missing_occ_chamb.Write()

    h_missing_evt.GetXaxis().SetTitle('Event number')
    h_missing_evt.SetLineWidth(2)
    h_missing_evt.SetLineColor(kRed)
    h_missing_evt.Write()

    h_matched_evt.GetXaxis().SetTitle('Event number')
    h_matched_evt.SetLineWidth(2)
    h_matched_evt.SetLineColor(kBlue)
    h_matched_evt.Write()

    h_matched_evt.Add( h_missing_evt )
    h_missing_evt.Divide( h_matched_evt )
    h_missing_evt.Scale( 100. )
    h_missing_evt.SetName('h_missing_pct_evt')
    h_missing_evt.SetTitle('Percentage of hits missing in event')
    h_missing_evt.Write()

    h_missing_sect_vs_evt.GetXaxis().SetTitle('Event number')
    h_missing_sect_vs_evt.GetYaxis().SetTitle('Sector')
    h_missing_sect_vs_evt.SetLineWidth(2)
    h_missing_sect_vs_evt.SetLineColor(kRed)
    h_missing_sect_vs_evt.Write()

    h_matched_sect_vs_evt.GetXaxis().SetTitle('Event number')
    h_matched_sect_vs_evt.GetYaxis().SetTitle('Sector')
    h_matched_sect_vs_evt.SetLineWidth(2)
    h_matched_sect_vs_evt.SetLineColor(kBlue)
    h_matched_sect_vs_evt.Write()

    h_matched_sect_vs_evt.Add( h_missing_sect_vs_evt )
    h_missing_sect_vs_evt.Divide( h_matched_sect_vs_evt )
    h_missing_sect_vs_evt.Scale( 100. )
    h_missing_sect_vs_evt.SetName('h_missing_pct_sect_vs_evt')
    h_missing_sect_vs_evt.SetTitle('Percentage of hits missing in event')
    h_missing_sect_vs_evt.Write()

    h_missing_lumi.GetXaxis().SetTitle('Luminosity block')
    h_missing_lumi.SetLineWidth(2)
    h_missing_lumi.SetLineColor(kRed)
    h_missing_lumi.Write()

    h_matched_lumi.GetXaxis().SetTitle('Luminosity block')
    h_matched_lumi.SetLineWidth(2)
    h_matched_lumi.SetLineColor(kBlue)
    h_matched_lumi.Write()

    h_matched_lumi.Add( h_missing_lumi )
    h_missing_lumi.Divide( h_matched_lumi )
    h_missing_lumi.Scale( 100. )
    h_missing_lumi.SetName('h_missing_pct_lumi')
    h_missing_lumi.SetTitle('Percentage of hits missing in event')
    h_missing_lumi.Write()

    h_missing_sect_vs_lumi.GetXaxis().SetTitle('Luminosity block')
    h_missing_sect_vs_lumi.GetYaxis().SetTitle('Sector')
    h_missing_sect_vs_lumi.SetLineWidth(2)
    h_missing_sect_vs_lumi.SetLineColor(kRed)
    h_missing_sect_vs_lumi.Write()

    h_matched_sect_vs_lumi.GetXaxis().SetTitle('Luminosity block')
    h_matched_sect_vs_lumi.GetYaxis().SetTitle('Sector')
    h_matched_sect_vs_lumi.SetLineWidth(2)
    h_matched_sect_vs_lumi.SetLineColor(kBlue)
    h_matched_sect_vs_lumi.Write()

    h_matched_sect_vs_lumi.Add( h_missing_sect_vs_lumi )
    h_missing_sect_vs_lumi.Divide( h_matched_sect_vs_lumi )
    h_missing_sect_vs_lumi.Scale( 100. )
    h_missing_sect_vs_lumi.SetName('h_missing_pct_sect_vs_lumi')
    h_missing_sect_vs_lumi.SetTitle('Percentage of hits missing in event')
    h_missing_sect_vs_lumi.Write()

    out_file.Close()
    del tree_1
    del tree_2
    file_1.Close()
    file_2.Close()

if __name__ == '__main__':
    main()
