#! /usr/bin/env python

## Compare tracks coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)

def main():

    print 'Inside emul_vs_unpack_LCTs'

    file_name_1 = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_2/src/EventFilter/L1TRawToDigi/EMTF_RAWToRoot_v0_run_270389_10k.root'
    file_name_2 = '/afs/cern.ch/user/a/abrinke1/EmuCorr/CMSSW_8_0_2/src/L1Trigger/L1TMuonEndCap/l1temtf_superprimitives_04_22_run_270389_10k.root' 
    out_file = TFile('plots/emul_vs_unpack_LCTs_10k.root','recreate')

    tree_name_1 = 'Events'
    tree_name_2 = 'Events'

    file_1 = TFile.Open(file_name_1)
    file_2 = TFile.Open(file_name_2)

    tree_1 = file_1.Get(tree_name_1)
    tree_2 = file_2.Get(tree_name_2)


    #################
    ### Book counters
    #################

    numHits = {}
    numHitsUnm = {}
    numHitsUnmExist = {}
    numHitsUnmNonZeroWire = {}

    numHits[0] = 0
    numHitsUnm[0] = 0
    numHitsUnmExist[0] = 0
    numHitsUnmNonZeroWire[0] = 0

    numHits[1] = 0
    numHitsUnm[1] = 0
    numHitsUnmExist[1] = 0
    numHitsUnmNonZeroWire[1] = 0

    numEndcapDiff = 0
    numStationDiff = 0
    numSectorDiff = 0
    numRingDiff = 0
    numChamberDiff = 0
    numValidDiff = 0
    numQualityDiff = 0
    numWireDiff = 0
    numStripDiff = 0
    numPatternDiff = 0
    numBendDiff = 0
    numBXDiff = 0
    numBX0Diff = 0
    numSyncErrDiff = 0
    numCSCIDDiff = 0

    ## Main event loop    
    for iEvt in range(tree_1.GetEntries()):
        
        if (iEvt > 100): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt

        tree_1.GetEntry(iEvt)
        tree_2.GetEntry(iEvt)

        ## Get branches from the trees
        Event = tree_1.EventAuxiliary
        Hits_1 = tree_1.l1tEMTFHits_unpack__EMTF
        Hits_2 = tree_2.l1tEMTFHits_simEmtfDigis_EMTF_L1TMuonEmulation
        Trks_1 = tree_1.l1tEMTFTracks_unpack__EMTF
        Trks_2 = tree_2.l1tEMTFTracks_simEmtfDigis_EMTF_L1TMuonEmulation

        if Event.event() != tree_2.EventAuxiliary.event():
            print 'In iEvt %d, tree 1 event = %d, tree 2 event = %d' % ( iEvt, Event.event(), tree_2.EventAuxiliary.event() )

        nHits1  = Hits_1.size()
        nHits2  = Hits_2.size()
        nTrks1  = Trks_1.size()
        nTrks2  = Trks_2.size()

        if (nHits1 == 0 or nHits2 == 0): continue

        # ######################################
        # ### Print out every LCT in every event
        # ######################################

        # print '******************************'
        # print 'Unpacker: %d hits and %d tracks in event %d' % ( nHits1, nTrks1, Event.event() )
        # for iHit1 in range(nHits1):
        #     Hit1 = Hits_1.at(iHit1)
        #     # print 'BX = %d, station = %d, sector = %d, ' % ( Hit1.BX(), Hit1.Station(), Hit1.Sector() ), \
        #     #     'CSC ID = %d, strip = %d, wire = %d, neighbor = %d' % ( Hit1.CSC_ID(), Hit1.Strip(), Hit1.Wire(), Hit1.Neighbor() )
        #     Id1 = Hit1.PtrCSC_DetId()
        #     print 'CSCDetId: endcap = %d, station = %d, triggerSector = %d, ' % ( Id1.endcap(), Id1.station(), Id1.triggerSector() ), \
        #         'ring = %d, chamber = %d' % ( Id1.ring(), Id1.chamber() )
        #     LCT1 = Hit1.PtrCSC_LCTDigi()
        #     print 'LCTDigi: valid = %d, quality = %d, wire = %d, strip = %d' % (LCT1.isValid(), LCT1.getQuality(), LCT1.getKeyWG(), LCT1.getStrip() ), \
        #         'pattern = %d, bend = %d, bx = %d, sync_err = %d, csc_ID = %d' % (LCT1.getPattern(), LCT1.getBend(), LCT1.getBX(), LCT1.getSyncErr(), LCT1.getCSCID() )
            
        # print 'Emulator: %d hits and %d tracks in event %d' % ( nHits2, nTrks2, Event.event() )
        # for iHit2 in range(nHits2):
        #     Hit2 = Hits_2.at(iHit2)
        #     # print 'BX = %d, station = %d, sector = %d, ' % ( Hit2.BX() - 6, Hit2.Station(), Hit2.Sector() ), \
        #     #     'CSC ID = %d, strip = %d, wire = %d, nTrks = %d' % ( Hit2.CSC_ID(), Hit2.Strip(), Hit2.Wire(), nTrks2 )
        #     Id2 = Hit2.PtrCSC_DetId()
        #     print 'CSCDetId: endcap = %d, station = %d, triggerSector = %d, ' % ( Id2.endcap(), Id2.station(), Id2.triggerSector() ), \
        #         'ring = %d, chamber = %d' % ( Id2.ring(), Id2.chamber() )
        #     LCT2 = Hit2.PtrCSC_LCTDigi()
        #     print 'LCTDigi: valid = %d, quality = %d, wire = %d, strip = %d' % (LCT2.isValid(), LCT2.getQuality(), LCT2.getKeyWG(), LCT2.getStrip() ), \
        #         'pattern = %d, bend = %d, bx = %d, sync_err = %d, csc_ID = %d' % (LCT2.getPattern(), LCT2.getBend(), LCT2.getBX(), LCT2.getSyncErr(), LCT2.getCSCID() )
        # print ''
        # continue


        #####################################################################################
        ### Compare hits in emulator and unpacker
        ###   * Emulator outputs all hits it received, whether or not a track was formed
        ###   * Unpacker outputs hits only in sectors with tracks (zero-suppression)
        ###   * Unpacker ouputs neighbor hits twice, and may build duplicate tracks with them
        #####################################################################################

        ## Check that unpacker hits have match in emulator
        unmatched_hit_exists = False
        for iHit1 in range(nHits1):
            Hit1 = Hits_1.at(iHit1)
            if Hit1.Neighbor() == 1:  ## Remove neighbor hits (which should appear twice)
                continue

            numHits[0] += 1
            unp_hit_matched = False
            for iHit2 in range(nHits2):
                Hit2 = Hits_2.at(iHit2)
                if Hit1.BX() == Hit2.BX() and Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector():
                    if Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire():
                        unp_hit_matched = True

                        Id1  = Hit1.PtrCSC_DetId()
                        LCT1 = Hit1.PtrCSC_LCTDigi()
                        Id2  = Hit2.PtrCSC_DetId()
                        LCT2 = Hit2.PtrCSC_LCTDigi()
                        # print '******************************'
                        # print 'Unp CSCDetId: endcap = %d, station = %d, triggerSector = %d, ' % ( Id1.endcap(), Id1.station(), Id1.triggerSector() ), \
                        #     'ring = %d, chamber = %d' % ( Id1.ring(), Id1.chamber() )
                        # print 'Emu CSCDetId: endcap = %d, station = %d, triggerSector = %d, ' % ( Id2.endcap(), Id2.station(), Id2.triggerSector() ), \
                        #     'ring = %d, chamber = %d' % ( Id2.ring(), Id2.chamber() )
                        # print 'Unp LCTDigi: valid = %d, quality = %d, wire = %d, strip = %d' % (LCT1.isValid(), LCT1.getQuality(), LCT1.getKeyWG(), LCT1.getStrip() ), \
                        #     'pattern = %d, bend = %d, bx = %d, sync_err = %d, csc_ID = %d' % (LCT1.getPattern(), LCT1.getBend(), LCT1.getBX(), LCT1.getSyncErr(), LCT1.getCSCID() )
                        # print 'Emu LCTDigi: valid = %d, quality = %d, wire = %d, strip = %d' % (LCT2.isValid(), LCT2.getQuality(), LCT2.getKeyWG(), LCT2.getStrip() ), \
                        #     'pattern = %d, bend = %d, bx = %d, sync_err = %d, csc_ID = %d' % (LCT2.getPattern(), LCT2.getBend(), LCT2.getBX(), LCT2.getSyncErr(), LCT2.getCSCID() )
                        # print ''

                        # if Id1.triggerSector() != Id2.triggerSector():
                        #     print 'Unp hit (LCT) sector = %d (%d), Emu hit (LCT) sector = %d (%d)' % ( Hit1.Sector(), Id1.triggerSector(), Hit2.Sector(), Id2.triggerSector() )
                        # if Id1.chamber() != Id2.chamber():
                        #     print 'Unp hit (LCT) chamber = %d (%d), Emu hit (LCT) chamber = %d (%d)' % ( Hit1.Chamber(), Id1.chamber(), Hit2.Chamber(), Id2.chamber() )
                        # if LCT1.getCSCID() != LCT2.getCSCID():
                        #     print 'Unp hit (LCT) CSC_ID = %d (%d), Emu hit (LCT) CSC_ID = %d (%d)' % ( Hit1.CSC_ID(), LCT1.getCSCID(), Hit2.CSC_ID(), LCT2.getCSCID() )
                        if LCT1.getBX0() != LCT2.getBX0():
                            print 'Unp hit (LCT) BX0 = %d (%d), Emu hit (LCT) BX0 = %d (%d)' % ( Hit1.BX0(), LCT1.getBX0(), Hit2.BX0(), LCT2.getBX0() )

                        if ( Id1.endcap()        != Id2.endcap()        ): numEndcapDiff += 1
                        if ( Id1.station()       != Id2.station()       ): numStationDiff += 1
                        if ( Id1.triggerSector() != Id2.triggerSector() ): numSectorDiff += 1
                        if ( Id1.ring()          != Id2.ring()          ): numRingDiff += 1
                        if ( Id1.chamber()       != Id2.chamber()       ): numChamberDiff += 1
                        if ( LCT1.isValid()    != LCT2.isValid()    ): numValidDiff += 1
                        if ( LCT1.getQuality() != LCT2.getQuality() ): numQualityDiff += 1
                        if ( LCT1.getKeyWG()   != LCT2.getKeyWG()   ): numWireDiff += 1
                        if ( LCT1.getStrip()   != LCT2.getStrip()   ): numStripDiff += 1
                        if ( LCT1.getPattern() != LCT2.getPattern() ): numPatternDiff += 1
                        if ( LCT1.getBend()    != LCT2.getBend()    ): numBendDiff += 1
                        if ( LCT1.getBX()      != LCT2.getBX()      ): numBXDiff += 1
                        if ( LCT1.getBX0()     != LCT2.getBX0()     ): numBX0Diff += 1
                        if ( LCT1.getSyncErr() != LCT2.getSyncErr() ): numSyncErrDiff += 1
                        if ( LCT1.getCSCID()   != LCT2.getCSCID()   ): numCSCIDDiff += 1

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

            emu_trk_in_sector = False
            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2.at(iTrk2)
                if Hit2.Sector() == Trk2.Sector(): 
                    emu_trk_in_sector = True       
            if not emu_trk_in_sector:  ## Remove hits in sectors without a track
                continue               ## Matches zero-suppression in firmware (but not neighbor analysis?!? - AWB 14.04.16)

            numHits[1] += 1
            emu_hit_matched = False
            for iHit1 in range(nHits1):
                Hit1 = Hits_1.at(iHit1)
                if Hit1.Neighbor() == 1:
                    continue
                if Hit1.BX() == Hit2.BX() and Hit1.Station() == Hit2.Station() and Hit1.Sector() == Hit2.Sector():
                    if Hit1.CSC_ID() == Hit2.CSC_ID() and Hit1.Strip() == Hit2.Strip() and Hit1.Wire() == Hit2.Wire():
                        emu_hit_matched = True

            if not emu_hit_matched:
                unmatched_hit_exists = True
                numHitsUnm[1] += 1
                if nHits1 > 0:
                    numHitsUnmExist[1] += 1
                    if Hit2.Wire() != 0:
                        numHitsUnmNonZeroWire[1] += 1


    print '*******************************************************'
    print '*******            The BIG picture              *******'
    print '*******************************************************'
    print '                       Unpacker    -  Emulator'
    print 'numHits:                %6d %11d' % (numHits[0], numHits[1]) 
    print 'numHitsUnm:             %6d %11d' % (numHitsUnm[0], numHitsUnm[1]) 
    print 'numHitsUnmExist:        %6d %11d' % (numHitsUnmExist[0], numHitsUnmExist[1]) 
    print 'numHitsUnmNonZeroWire:  %6d %11d' % (numHitsUnmNonZeroWire[0], numHitsUnmNonZeroWire[1]) 
    print 'numEndcapDiff = %d'  % numEndcapDiff 
    print 'numStationDiff = %d' % numStationDiff
    print 'numSectorDiff = %d'  % numSectorDiff
    print 'numRingDiff = %d'    % numRingDiff
    print 'numChamberDiff = %d' % numChamberDiff
    print 'numValidDiff = %d'   % numValidDiff
    print 'numQualityDiff = %d' % numQualityDiff
    print 'numWireDiff = %d'    % numWireDiff
    print 'numStripDiff = %d'   % numStripDiff
    print 'numPatternDiff = %d' % numPatternDiff
    print 'numBendDiff = %d'    % numBendDiff
    print 'numBXDiff = %d'      % numBXDiff
    print 'numBX0Diff = %d'     % numBX0Diff
    print 'numSyncErrDiff = %d' % numSyncErrDiff
    print 'numCSCIDDiff = %d'   % numCSCIDDiff

    out_file.cd()

    del tree_1
    del tree_2

    file_1.Close()
    file_2.Close()
    out_file.Close()

if __name__ == '__main__':
    main()
