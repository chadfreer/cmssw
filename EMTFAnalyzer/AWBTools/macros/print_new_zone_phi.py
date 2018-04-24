#! /usr/bin/env python

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside print_new_zone_phi'

    prefix = 'root://eoscms//eos/cms'
    file_dir = '/store/user/abrinke1/EMTF/Emulator/trees/SingleMuon/EMTF_EFF/160912_110056/0000/'
    in_files = TChain('Events')
    in_files.Add('/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/pattern_phi/EMTF_Tree_ExpressPhysics_281613_dupFix_debug_ABCDE.root')

    nMismatch = 0
    nMissSt = {}
    nMissSt_match = {}
    nMissSt_match_1 = {}
    for i in range(4): 
        nMissSt[i] = 0
        nMissSt_match[i] = 0
        nMissSt_match_1[i] = 0

    for iEvt in range(in_files.GetEntries()):
        
        # if (iEvt < 10000): continue
        # if (iEvt > 50000): break
        if iEvt % 100 is 0: print 'Event #', iEvt
        in_files.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = in_files.EventAuxiliary

        Hits_1 = in_files.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        Trks_1 = in_files.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        Hits_2 = in_files.l1tEMTFHits_simEmtfDigis_CSC_L1TMuonEmulation
        Trks_2 = in_files.l1tEMTFTracks_simEmtfDigis__L1TMuonEmulation
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nHits2 = Hits_2.size()
        nTrks2 = Trks_2.size()

        nUnp = 0
        nEmu = 0
        mismatch = False
        miss_st = {}
        unp_st = {}
        emu_st = {}
        for i in range(4): 
            miss_st[i] = False
            unp_st[i] = [-99, -99]
            emu_st[i] = [-99, -99]

        for iTrk1 in range(nTrks1):
            Trk1 = Trks_1.at(iTrk1)
            if abs(Trk1.BX()) > 1: continue
            if Trk1.Endcap()*Trk1.Sector() != -6: continue
            nUnp += 1
            iUnp = iTrk1
            for iHit1 in range(Trk1.PtrHits().size()):
                unp_st[Trk1.PtrHits().at(iHit1).Station() - 1] = [Trk1.PtrHits().at(iHit1).Strip(), Trk1.PtrHits().at(iHit1).Wire()]

            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)
                if abs(Trk2.BX()) > 1: continue
                if Trk2.Endcap()*Trk2.Sector() != -6: continue
                nEmu += 1
                for iHit2 in range(Trk2.PtrHits().size()):
                    emu_st[Trk2.PtrHits().at(iHit2).Station() - 1] = [Trk2.PtrHits().at(iHit2).Strip(), Trk2.PtrHits().at(iHit2).Wire()]

                if Trk1.Mode() != Trk2.Mode(): 
                    mismatch = True
                    iEmu = iTrk2
                if Trk1.Mode() == Trk2.Mode() - 8: miss_st[0] = True
                if Trk1.Mode() == Trk2.Mode() - 4: miss_st[1] = True
                if Trk1.Mode() == Trk2.Mode() - 2: miss_st[2] = True
                if Trk1.Mode() == Trk2.Mode() - 1: miss_st[3] = True


        hits_match = True
        for i in range(4):
            for j in range(2):
                if unp_st[i][j] != emu_st[i][j] and not miss_st[i]: hits_match = False

        if mismatch: nMismatch += 1
        for i in range(4):
            if miss_st[i]: nMissSt[i] += 1
            if miss_st[i] and hits_match: nMissSt_match[i] += 1
            if miss_st[i] and hits_match and nUnp == 1 and nEmu == 1: nMissSt_match_1[i] += 1

        if not (miss_st[1] and nUnp == 1 and nEmu == 1 and hits_match): continue

        print '\n*************** Run %d, Lumi %d, Event %d ********************' % (Event.run(), Event.luminosityBlock(), Event.event())

        print '\n*** Unpacker track ***'
        Trk1 = Trks_1.at(iUnp)
        PrintEMTFTrack( Trk1 )
        PrintPtLUT( Trk1 )
        print ' - Hits in track'
        for iHit in range(Trk1.PtrHits().size()):
            PrintEMTFHit( Trk1.PtrHits().at(iHit) )

        print '\n*** Emulator track ***'
        Trk2 = Trks_2.at(iEmu)
        PrintEMTFTrack( Trk2 )
        PrintPtLUT( Trk2 )
        hit_min_phi = 999
        hit_max_phi = -999
        hit_st2_phi = -999
        print ' - Hits in track'
        for iHit in range(Trk2.PtrHits().size()):
            PrintEMTFHitExtra( Trk2.PtrHits().at(iHit) )
            if Trk2.PtrHits().at(iHit).Station() != 2 and Trk2.PtrHits().at(iHit).Phi_loc_deg() < hit_min_phi: hit_min_phi = Trk2.PtrHits().at(iHit).Phi_loc_deg()
            if Trk2.PtrHits().at(iHit).Station() != 2 and Trk2.PtrHits().at(iHit).Phi_loc_deg() > hit_max_phi: hit_max_phi = Trk2.PtrHits().at(iHit).Phi_loc_deg()
            if Trk2.PtrHits().at(iHit).Station() == 2: hit_st2_phi = Trk2.PtrHits().at(iHit).Phi_loc_deg()
        if (hit_st2_phi > hit_min_phi and hit_st2_phi < hit_max_phi):
            print '\n### INSIDE: Station 2 LCT local phi = %.2f, {min, max} of other stations = {%.2f, %.2f}' % (hit_st2_phi, hit_min_phi, hit_max_phi)
        elif (hit_st2_phi == hit_min_phi or hit_st2_phi == hit_max_phi):
            print '\n### BORDER: Station 2 LCT local phi = %.2f, {min, max} of other stations = {%.2f, %.2f}' % (hit_st2_phi, hit_min_phi, hit_max_phi)
        else:
            distance = min(abs(hit_st2_phi - hit_min_phi), abs(hit_st2_phi - hit_max_phi))
            print '\n### OUTSIDE by %.2f: Station 2 LCT local phi = %.2f, {min, max} of other stations = {%.2f, %.2f}' % (distance, hit_st2_phi, hit_min_phi, hit_max_phi)

        print '\n*** Hits with sector index = 11 ***'
        for iHit2 in range(nHits2):
            Hit2 = Hits_2.at(iHit2)
            if Hit2.Sector_index() == 11:
                PrintEMTFHitExtra( Hit2 )
                    
        print ''
        PrintSimulatorHitHeader()
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            if Hit1.Sector_index() == 11: PrintSimulatorHit( Hit1 )

        print '\n******************************************'

    ## End loop over events

    print 'Tracks with different modes:                          %4d' % nMismatch
    for i in range(4):
        print 'Tracks missing St %d:                                  %4d' % (i+1, nMissSt[i])
        print 'Tracks missing St %d, other hits match:                %4d' % (i+1, nMissSt_match[i])
        print 'Tracks missing St %d, other hits match, 1 unp/emu hit: %4d' % (i+1, nMissSt_match_1[i])


if __name__ == '__main__':
    main()
