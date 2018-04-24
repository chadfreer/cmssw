#! /usr/bin/env python

## Compare tracks coming out of EMTF and CSCTF

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside csctf_vs_emtf_tracks'

    file_name = '/afs/cern.ch/user/a/abrinke1/EmuPull_807/CMSSW_8_0_7/src/L1Trigger/L1TMuonEndCap/l1temtf_unpacker_emulator_04_22_run_272936.root'
    out_file = TFile('plots/csctf_vs_emtf_tracks.root','recreate')

    tree_name = 'Events'

    file = TFile.Open(file_name)
    tree = file.Get(tree_name)

    #################
    ### Book counters
    #################

    numTrks = {}
    numTrksUnm = {}
    numTrksUnmExist = {}

    numTrks[0] = 0
    numTrksUnm[0] = 0
    numTrksUnmExist[0] = 0

    numTrks[1] = 0
    numTrksUnm[1] = 0
    numTrksUnmExist[1] = 0

    ###################
    ### Book histograms
    ###################

    BX_bins = [8, -3.5, 4.5]
    eta_bins = [501, -250.5, 250.5]
    mode_bins = [18, -1.5, 16.5]

    h_BX = TH1D('h_BX', 'Csc. & Unp. BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_eta = TH1D('h_eta', 'Csc. & Unp. eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_mode = TH1D('h_mode', 'Csc. & Unp. mode', mode_bins[0], mode_bins[1], mode_bins[2])

    h_Unp_BX = TH1D('h_Unp_BX', 'EMTF BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_Unp_eta = TH1D('h_Unp_eta', 'EMTF eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_Unp_mode = TH1D('h_Unp_mode', 'EMTF mode', mode_bins[0], mode_bins[1], mode_bins[2])

    h_Csc_BX = TH1D('h_Csc_BX', 'CSCTF BX', BX_bins[0], BX_bins[1], BX_bins[2])
    h_Csc_eta = TH1D('h_Csc_eta', 'CSCTF eta', eta_bins[0], eta_bins[1], eta_bins[2])
    h_Csc_mode = TH1D('h_Csc_mode', 'CSCTF mode', mode_bins[0], mode_bins[1], mode_bins[2])

    h_Csc_vs_Unp_BX = TH2D('h_Csc_vs_Unp_BX', 'CSCTF vs. EMTF BX', BX_bins[0], BX_bins[1], BX_bins[2], BX_bins[0], BX_bins[1], BX_bins[2])
    h_Csc_vs_Unp_mode = TH2D('h_Csc_vs_Unp_mode', 'CSCTF vs. EMTF mode', mode_bins[0], mode_bins[1], mode_bins[2], mode_bins[0], mode_bins[1], mode_bins[2])
    h_Csc_vs_Unp_eta = TH2D('h_Csc_vs_Unp_eta', 'CSCTF vs. EMTF eta', eta_bins[0], eta_bins[1], eta_bins[2], eta_bins[0], eta_bins[1], eta_bins[2])

    ## Main event loop    
    for iEvt in range(tree.GetEntries()):
        
        ## if (iEvt > 10000): continue
        if iEvt % 1000 is 0: print 'Event #', iEvt
        tree.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = tree.EventAuxiliary
        Hits_1 = tree.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        Trks_1 = tree.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        Trks_2_tmp = tree.cscL1TrackCSCDetIdCSCCorrelatedLCTDigiMuonDigiCollectionstdpairs_csctfDigis__L1TMuonEmulation
        nTrks2_tmp = Trks_2_tmp.size()
        Trks_2 = []
        for iTrk2 in range(nTrks2_tmp):
            Trks_2.append(Trks_2_tmp.at(iTrk2).first)
        
        nHits1 = Hits_1.size()
        nTrks1 = Trks_1.size()
        nTrks2 = len(Trks_2)

        if (nHits1 == 0): continue

        ## Check that EMTF hits have match in CSCTF
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

        # if neighbor_hit_exists:
        #     continue
        if ( nTrks1 == 0 and nTrks2 == 0 ):
            continue
        if ( nTrks1 > 1 or nTrks2 > 1 ):
            continue

        ## Check that EMTF tracks have match in CSCTF
        skip_event = False
        for iTrk1 in range(nTrks1):
            if skip_event:
                continue
            Trk1 = Trks_1.at(iTrk1)
            if Trk1.BX() < -1 or Trk1.BX() > 1:
                skip_event = True
                continue
            if Trk1.BX() < 0 and bx_m3_hit_exists:
                skip_event = True
                continue
            if Trk1.BX() > 0 and bx_p3_hit_exists:
                skip_event = True
                continue
            if Trk1.Pt_GMT() <= 0:
                skip_event = True
                continue

            numTrks[0] += 1
            unp_trk_matched = False

            h_Unp_BX.Fill( Trk1.BX() )
            h_Unp_mode.Fill( Trk1.Mode() )
            h_Unp_eta.Fill( Trk1.Eta_GMT() )

            for iTrk2 in range(nTrks2):
                Trk2 = Trks_2[iTrk2]
                ## if TracksMatch( Trk1, Trk2 ):
                if True:
                    unp_trk_matched = True

                    h_Csc_vs_Unp_BX.Fill( Trk1.BX(), Trk2.BX() )
                    h_Csc_vs_Unp_mode.Fill( Trk1.Mode(), Trk2.mode() )
                    csctf_eta = Trk2.eta_packed()
                    if Trk2.endcap() == 2:
                        csctf_eta = -1*csctf_eta
                    h_Csc_vs_Unp_eta.Fill( Trk1.Eta_GMT(), csctf_eta )

            if not unp_trk_matched:
                numTrksUnm[0] += 1
                if (nTrks2 > 0):
                    numTrksUnmExist[0] += 1


        if skip_event:
            continue

        ## Check that CSCTF tracks have match in EMTF
        for iTrk2 in range(nTrks2):
            Trk2 = Trks_2[iTrk2]

            numTrks[1] += 1

            h_Csc_BX.Fill( Trk2.BX() )
            h_Csc_mode.Fill( Trk2.mode() )
            csctf_eta = Trk2.eta_packed()
            if Trk2.endcap() == 2:
                csctf_eta = -1*csctf_eta
            h_Csc_eta.Fill( csctf_eta )

            csc_trk_matched = False
            for iTrk1 in range(nTrks1):
                Trk1 = Trks_1.at(iTrk1)
                ## if TracksMatch( Trk1, Trk2 ):
                if True:
                    csc_trk_matched = True

            if not csc_trk_matched:
                numTrksUnm[1] += 1
                if (nTrks1 > 0):
                    numTrksUnmExist[1] += 1



    print '*******************************************************'
    print '*******            The BIG picture              *******'
    print '*******************************************************'
    print '                       EMTF    -  CSCTF'
    print 'numTrks:                %6d %11d' % (numTrks[0], numTrks[1]) 
    print 'numTrksUnm:             %6d %11d' % (numTrksUnm[0], numTrksUnm[1]) 
    print 'numTrksUnmExist:        %6d %11d' % (numTrksUnmExist[0], numTrksUnmExist[1]) 


    out_file.cd()

    h_BX.GetXaxis().SetTitle('BX')
    h_BX.Write()
    h_eta.GetXaxis().SetTitle('eta')
    h_eta.Write()
    h_mode.GetXaxis().SetTitle('Mode')
    h_mode.Write()

    h_Unp_BX.GetXaxis().SetTitle('BX')
    h_Unp_BX.Write()
    h_Unp_eta.GetXaxis().SetTitle('eta')
    h_Unp_eta.SetLineWidth(2)
    h_Unp_eta.SetLineColor(kBlue)
    h_Unp_eta.Write()
    h_Unp_mode.GetXaxis().SetTitle('Mode')
    h_Unp_mode.SetLineWidth(2)
    h_Unp_mode.SetLineColor(kBlue)
    h_Unp_mode.Write()

    h_Csc_BX.GetXaxis().SetTitle('BX')
    h_Csc_BX.Write()
    h_Csc_eta.GetXaxis().SetTitle('eta')
    h_Csc_eta.SetLineWidth(2)
    h_Csc_eta.SetLineColor(kRed)
    h_Csc_eta.Write()
    h_Csc_mode.GetXaxis().SetTitle('Mode')
    h_Csc_mode.SetLineWidth(2)
    h_Csc_mode.SetLineColor(kRed)
    h_Csc_mode.Write()

    h_Csc_vs_Unp_BX.GetXaxis().SetTitle('EMTF BX')
    h_Csc_vs_Unp_BX.GetYaxis().SetTitle('CSCTF BX')
    h_Csc_vs_Unp_BX.SetMarkerSize(1.5)
    h_Csc_vs_Unp_BX.SetMarkerColor(kWhite)
    h_Csc_vs_Unp_BX.Write()
    h_Csc_vs_Unp_eta.GetXaxis().SetTitle('EMTF eta')
    h_Csc_vs_Unp_eta.GetYaxis().SetTitle('CSCTF eta')
    h_Csc_vs_Unp_eta.SetMarkerSize(1.5)
    h_Csc_vs_Unp_eta.SetMarkerColor(kWhite)
    h_Csc_vs_Unp_eta.Write()
    h_Csc_vs_Unp_mode.GetXaxis().SetTitle('EMTF mode')
    h_Csc_vs_Unp_mode.GetYaxis().SetTitle('CSCTF mode')
    h_Csc_vs_Unp_mode.SetMarkerSize(1.5)
    h_Csc_vs_Unp_mode.SetMarkerColor(kWhite)
    h_Csc_vs_Unp_mode.Write()

    out_file.Close()
    del tree
    file.Close()

if __name__ == '__main__':
    main()
