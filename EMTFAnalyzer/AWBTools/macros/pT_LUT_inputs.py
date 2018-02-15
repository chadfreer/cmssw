#! /usr/bin/env python

from ROOT import *
gROOT.SetBatch(True)
from Helper import *

gStyle.SetOptStat(0)

def main():

    print 'Inside pT_LUT_inputs'

    prefix = 'root://eoscms//eos/cms'
    file_dir = '/store/user/abrinke1/EMTF/Emulator/trees/SingleMuon/EMTF_EFF/160912_110056/0000/'
    in_files = TChain('Events')

    for i in range(87):
        file_name = '%s%sEMTF_Tree_%d.root' % (prefix, file_dir, i+1)
        if i % 10 is 0: print 'Opening %s' % file_name
        in_files.Add(file_name)

    # in_files.Add('/afs/cern.ch/user/a/abrinke1/EMTFAnalyzer/CMSSW_8_0_19/src/L1Trigger/L1TMuonEndCap/EMTF_Tree_ExpressPhysics_279975_dupFix_debug.root')

    out_file = TFile('plots/pT_LUT_inputs.root','recreate')

    int_bins = [10, -1.5, 8.5]
    dPhi_bins = [121, -12.1, 12.1]
    dTh_bins = [21, -3.0, 3.0]
    ratio_bins = [151, -75.5, 75.5]
    ring_bins = [11, -5.5, 5.5]
    cham_bins = [36, 0.5, 36.5]
    patt_bins = [12, -0.5, 11.5]
    clct_bins = [11, -5.5, 5.5]

    dPhis = {}
    dThetas = {}
    FRs = {}
    CLCTs = {}
    for i in [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]:

        dPhis[i] = {}
        if i in [12, 13, 14, 15]:
            dPhis[i]['12'] = TH2D('h_%d_dPhi_12' % i, 'Mode %d dPhi_12 ratio vs. degrees' % i, dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], ratio_bins[0], ratio_bins[1], ratio_bins[2])
        if i in [6, 7, 14, 15]:
            dPhis[i]['23'] = TH2D('h_%d_dPhi_23' % i, 'Mode %d dPhi_23 ratio vs. degrees' % i, dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], ratio_bins[0], ratio_bins[1], ratio_bins[2])
        if i in [3, 7, 11, 15]:
            dPhis[i]['34'] = TH2D('h_%d_dPhi_34' % i, 'Mode %d dPhi_34 ratio vs. degrees' % i, dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], ratio_bins[0], ratio_bins[1], ratio_bins[2])
        if i in [10, 11]:
            dPhis[i]['13'] = TH2D('h_%d_dPhi_13' % i, 'Mode %d dPhi_13 ratio vs. degrees' % i, dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], ratio_bins[0], ratio_bins[1], ratio_bins[2])
        if i in [5, 13]:
            dPhis[i]['24'] = TH2D('h_%d_dPhi_24' % i, 'Mode %d dPhi_24 ratio vs. degrees' % i, dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], ratio_bins[0], ratio_bins[1], ratio_bins[2])
        if i in [9]:
            dPhis[i]['14'] = TH2D('h_%d_dPhi_14' % i, 'Mode %d dPhi_14 ratio vs. degrees' % i, dPhi_bins[0], dPhi_bins[1], dPhi_bins[2], ratio_bins[0], ratio_bins[1], ratio_bins[2])

        dThetas[i] = {}
        if i in [12]:
            dThetas[i]['12'] = TH2D('h_%d_dTheta_12' % i, 'Mode %d dTheta_12 vs. degrees' % i, dTh_bins[0], dTh_bins[1], dTh_bins[2], int_bins[0], int_bins[1], int_bins[2])
        if i in [6]:
            dThetas[i]['23'] = TH2D('h_%d_dTheta_23' % i, 'Mode %d dTheta_23 vs. degrees' % i, dTh_bins[0], dTh_bins[1], dTh_bins[2], int_bins[0], int_bins[1], int_bins[2])
        if i in [3]:
            dThetas[i]['34'] = TH2D('h_%d_dTheta_34' % i, 'Mode %d dTheta_34 vs. degrees' % i, dTh_bins[0], dTh_bins[1], dTh_bins[2], int_bins[0], int_bins[1], int_bins[2])
        if i in [10, 14]:
            dThetas[i]['13'] = TH2D('h_%d_dTheta_13' % i, 'Mode %d dTheta_13 vs. degrees' % i, dTh_bins[0], dTh_bins[1], dTh_bins[2], int_bins[0], int_bins[1], int_bins[2])
        if i in [5, 7]:
            dThetas[i]['24'] = TH2D('h_%d_dTheta_24' % i, 'Mode %d dTheta_24 vs. degrees' % i, dTh_bins[0], dTh_bins[1], dTh_bins[2], int_bins[0], int_bins[1], int_bins[2])
        if i in [9, 11, 13]:
            dThetas[i]['14'] = TH2D('h_%d_dTheta_14' % i, 'Mode %d dTheta_14 vs. degrees' % i, dTh_bins[0], dTh_bins[1], dTh_bins[2], int_bins[0], int_bins[1], int_bins[2])

        FRs[i] = {}
        if i in [9, 10, 11, 12, 13, 14, 15]:
            FRs[i]['1'] = TH2D('h_%d_FR_1' % i, 'Mode %d FR_1 ring vs. chamber' % i, cham_bins[0], cham_bins[1], cham_bins[2], ring_bins[0], ring_bins[1], ring_bins[2])
        if i in [5, 6, 12]:
            FRs[i]['2'] = TH2D('h_%d_FR_2' % i, 'Mode %d FR_2 ring vs. chamber' % i, cham_bins[0], cham_bins[1], cham_bins[2], ring_bins[0], ring_bins[1], ring_bins[2])
        if i in [3, 6, 10]:
            FRs[i]['3'] = TH2D('h_%d_FR_3' % i, 'Mode %d FR_3 ring vs. chamber' % i, cham_bins[0], cham_bins[1], cham_bins[2], ring_bins[0], ring_bins[1], ring_bins[2])
        if i in [3, 5, 9]:
            FRs[i]['4'] = TH2D('h_%d_FR_4' % i, 'Mode %d FR_4 ring vs. chamber' % i, cham_bins[0], cham_bins[1], cham_bins[2], ring_bins[0], ring_bins[1], ring_bins[2])

        CLCTs[i] = {}
        if i in [9, 10, 11, 12, 13, 14]:
            CLCTs[i]['1'] = TH2D('h_%d_CLCT_1' % i, 'Mode %d CLCT_1 LUT vs. LCT' % i, patt_bins[0], patt_bins[1], patt_bins[2], clct_bins[0], clct_bins[1], clct_bins[2])
        if i in [5, 6, 7, 12]:
            CLCTs[i]['2'] = TH2D('h_%d_CLCT_2' % i, 'Mode %d CLCT_2 LUT vs. LCT' % i, patt_bins[0], patt_bins[1], patt_bins[2], clct_bins[0], clct_bins[1], clct_bins[2])
        if i in [3, 6, 10]:
            CLCTs[i]['3'] = TH2D('h_%d_CLCT_3' % i, 'Mode %d CLCT_3 LUT vs. LCT' % i, patt_bins[0], patt_bins[1], patt_bins[2], clct_bins[0], clct_bins[1], clct_bins[2])
        if i in [3, 5, 9]:
            CLCTs[i]['4'] = TH2D('h_%d_CLCT_4' % i, 'Mode %d CLCT_4 LUT vs. LCT' % i, patt_bins[0], patt_bins[1], patt_bins[2], clct_bins[0], clct_bins[1], clct_bins[2])

        


    for iEvt in range(in_files.GetEntries()):
        
        if (iEvt > 10000): break
        if iEvt % 100 is 0: print 'Event #', iEvt
        in_files.GetEntry(iEvt)

        ## Get branches from the trees
        Event  = in_files.EventAuxiliary

        Hits = in_files.l1tEMTFHits_simEmtfDigis_CSC_L1TMuonEmulation
        Trks = in_files.l1tEMTFTracks_simEmtfDigis__L1TMuonEmulation
        Hits_unp = in_files.l1tEMTFHits_emtfStage2Digis__L1TMuonEmulation
        Trks_unp = in_files.l1tEMTFTracks_emtfStage2Digis__L1TMuonEmulation
        
        nHits = Hits.size()
        nTrks = Trks.size()
        nHits_unp = Hits_unp.size()
        nTrks_unp = Trks_unp.size()

        for iTrk in range(nTrks):
            Trk = Trks.at(iTrk)

            # disagree = False
            # for iHit in range(Trk.PtrHits().size()):
            #     Hit = Trk.PtrHits().at(iHit)
            #     if Hit.Phi_loc_int() != Trk.Phis().at(iHit): disagree = True

            # unmatched = False
            # for iHit in range(Trk.PtrHits().size()):
            #     Hit = Trk.PtrHits().at(iHit)
            #     no_match = True
            #     for jHit in range(Trk.Phis().size()):
            #         if Hit.Phi_loc_int() == Trk.Phis().at(jHit): no_match = False
            #     if no_match: unmatched = True

            # if not unmatched: continue
            # print '\ndisagree = %s, unmatched = %s' % (disagree, unmatched)
            # for iHit in range(Trk.PtrHits().size()):
            #     Hit = Trk.PtrHits().at(iHit)
            #     print 'Hit hit phi = %d' % Hit.Phi_loc_int()
            # for jHit in range(Trk.Phis().size()):
            #     print 'Trk hit phi = %d' % Trk.Phis().at(jHit)

            # PrintEMTFTrack(Trk)
            # PrintPtLUT(Trk)
            # for iHit in range(Trk.PtrHits().size()):
            #     Hit = Trk.PtrHits().at(iHit)
            #     print 'Hit %d hit phi (%d) and track hit phi (%d)' % (iHit+1, Hit.Phi_loc_int(), Trk.Phis().at(iHit))
            #     PrintEMTFHitExtra(Hit)

        for iMode in [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]:
            for iTrk in range(nTrks):
                Trk = Trks.at(iTrk)
                if Trk.Mode() != iMode: continue

                for iHit1 in range(Trk.PtrHits().size()):
                    Hit1 = Trk.PtrHits().at(iHit1)

                    for iSt in FRs[iMode].keys():
                        if '1' in iSt and Hit1.Station() == 1: FRs[iMode][iSt].Fill(Hit1.Chamber(), Hit1.Ring()*Hit1.Endcap(), 1.0*Trk.FR_1())
                        if '2' in iSt and Hit1.Station() == 2: FRs[iMode][iSt].Fill(Hit1.Chamber(), Hit1.Ring()*Hit1.Endcap(), 1.0*Trk.FR_2())
                        if '3' in iSt and Hit1.Station() == 3: FRs[iMode][iSt].Fill(Hit1.Chamber(), Hit1.Ring()*Hit1.Endcap(), 1.0*Trk.FR_3())
                        if '4' in iSt and Hit1.Station() == 4: FRs[iMode][iSt].Fill(Hit1.Chamber(), Hit1.Ring()*Hit1.Endcap(), 1.0*Trk.FR_4())

                    for iSt in CLCTs[iMode].keys():
                        if '1' in iSt and Hit1.Station() == 1: CLCTs[iMode][iSt].Fill(Hit1.Pattern(), Trk.CLCT_1())
                        if '2' in iSt and Hit1.Station() == 2: CLCTs[iMode][iSt].Fill(Hit1.Pattern(), Trk.CLCT_2())
                        if '3' in iSt and Hit1.Station() == 3: CLCTs[iMode][iSt].Fill(Hit1.Pattern(), Trk.CLCT_3())
                        if '4' in iSt and Hit1.Station() == 4: CLCTs[iMode][iSt].Fill(Hit1.Pattern(), Trk.CLCT_4())

                    for iHit2 in range(iHit1+1, Trk.PtrHits().size()):
                        Hit2 = Trk.PtrHits().at(iHit2)
                        
                        st = [Hit1.Station(), Hit2.Station()]
                        dPhi = CalcDPhi( Hit2.Phi_glob_rad(), Hit1.Phi_glob_rad() ) * 180.0 / 3.14159
                        dTheta = CalcDPhi( Hit2.Theta_rad(), Hit1.Theta_rad() ) * 180.0 / 3.14159
                        if Hit1.Station() > Hit2.Station(): dPhi = -1 * dPhi
                        if Hit1.Station() > Hit2.Station(): dTheta = -1 * dTheta


                        for iSt in dPhis[iMode].keys():
                            dPhi_int = -999
                            if '12' in iSt and 1 in st and 2 in st: dPhi_int = Trk.DPhi_12()
                            if '23' in iSt and 2 in st and 3 in st: dPhi_int = Trk.DPhi_23()
                            if '34' in iSt and 3 in st and 4 in st: dPhi_int = Trk.DPhi_34()
                            if '13' in iSt and 1 in st and 3 in st: dPhi_int = Trk.DPhi_13()
                            if '24' in iSt and 2 in st and 4 in st: dPhi_int = Trk.DPhi_24()
                            if '14' in iSt and 1 in st and 4 in st: dPhi_int = Trk.DPhi_34()

                            if dPhi_int == -999: continue
                            if dPhi_int == 0 and dPhi == 0: dPhi_ratio = 1
                            elif dPhi_int != 0 and dPhi == 0: dPhi_ratio = 0
                            else: dPhi_ratio = dPhi_int*1.0 / dPhi

                            ## if dPhi < dPhi_bins[1] or dPhi > dPhi_bins[2]:
                            if (Trk.Mode() == 10 or Trk.Mode() == 12) and abs(dPhi) > 8.5: ## 512 / 60.0 = 8.53333
                                print '\n*** Emulator track with buggy dPhi_%s' % iSt
                                PrintEMTFTrack(Trk)
                                PrintPtLUT(Trk)
                                print '- Hits'
                                PrintEMTFHitExtra(Hit1)
                                PrintEMTFHitExtra(Hit2)

                                print '\n*** Matching unpacked track ***'
                                for jTrk in range(nTrks_unp):
                                    if ( Trks_unp.at(jTrk).Eta_GMT() == Trk.Eta_GMT() and Trks_unp.at(jTrk).Phi_GMT() == Trk.Phi_GMT() ):
                                        PrintEMTFTrack(Trks_unp.at(jTrk))
                                        PrintPtLUT(Trks_unp.at(jTrk))
                                        print '- Hits'
                                        for jHit in range(Trks_unp.at(jTrk).PtrHits().size()):
                                            PrintEMTFHit(Trks_unp.at(jTrk).PtrHits().at(jHit))

                                print ''
                                PrintSimulatorHitHeader()
                                for jHit in range(nHits_unp):
                                    if Hits_unp.at(jHit).Sector_index() == Trk.Sector_index():
                                        PrintSimulatorHit( Hits_unp.at(jHit) )


                            if dPhi < dPhi_bins[1]: dPhi = dPhi_bins[1]+0.1
                            if dPhi > dPhi_bins[2]: dPhi = dPhi_bins[2]-0.1
 
                            dPhis[iMode][iSt].Fill(dPhi, dPhi_ratio)


                        for iSt in dThetas[iMode].keys():
                            dTheta_int = -999
                            if '12' in iSt and 1 in st and 2 in st: dTheta_int = Trk.DTheta_12()
                            if '23' in iSt and 2 in st and 3 in st: dTheta_int = Trk.DTheta_23()
                            if '34' in iSt and 3 in st and 4 in st: dTheta_int = Trk.DTheta_34()
                            if '13' in iSt and 1 in st and 3 in st: dTheta_int = Trk.DTheta_13()
                            if '24' in iSt and 2 in st and 4 in st: dTheta_int = Trk.DTheta_24()
                            if '14' in iSt and 1 in st and 4 in st: dTheta_int = Trk.DTheta_34()

                            if dTheta_int == -999: continue
                            # if dTheta < dTh_bins[1] or dTheta > dTh_bins[2]:
                            #     print '\n*******************************************'
                            #     print '*** Odd event with very large dTheta_%s' % iSt
                            #     PrintEMTFTrack(Trk)
                            #     PrintPtLUT(Trk)
                            #     PrintEMTFHitExtra(Hit1)
                            #     PrintEMTFHitExtra(Hit2)

                            #     nSameChamber = 0
                            #     print '\n*** Other hits in same chamber as Hit1 ***'
                            #     for jHit in range(nHits):
                            #         if HitsMatchChamber(Hit1, Hits.at(jHit)) and Hit1.Sector_index() == Hits.at(jHit).Sector_index() and not HitsMatch(Hit1, Hits.at(jHit)): 
                            #             nSameChamber += 1
                            #             PrintEMTFHitExtra( Hits.at(jHit) )
                            #     print '\n*** Other hits in same chamber as Hit2 ***'
                            #     for jHit in range(nHits):
                            #         if HitsMatchChamber(Hit2, Hits.at(jHit)) and Hit2.Sector_index() == Hits.at(jHit).Sector_index() and not HitsMatch(Hit2, Hits.at(jHit)): 
                            #             nSameChamber += 1
                            #             PrintEMTFHitExtra( Hits.at(jHit) )

                            #     if nSameChamber == 0:
                            #         print '\n*** All hits in same sector ***'
                            #         for jHit in range(nHits):
                            #             if Hit1.Sector_index() == Hits.at(jHit).Sector_index():
                            #                 PrintEMTFHitExtra( Hits.at(jHit) )

                                # print '\n*** All emulator tracks ***'
                                # for jTrk in range(nTrks):
                                #     print ''
                                #     PrintEMTFTrack(Trks.at(jTrk))
                                #     for jHit in range(Trks.at(jTrk).PtrHits().size()):
                                #         PrintEMTFHitExtra(Trks.at(jTrk).PtrHits().at(jHit))

                                # print '\n*** All unpacked tracks ***'
                                # for jTrk in range(nTrks_unp):
                                #     print ''
                                #     PrintEMTFTrack(Trks_unp.at(jTrk))
                                #     for jHit in range(Trks_unp.at(jTrk).PtrHits().size()):
                                #         PrintEMTFHit(Trks_unp.at(jTrk).PtrHits().at(jHit))

                            if dTheta < dTh_bins[1]: dTheta = dTh_bins[1]+0.1
                            if dTheta > dTh_bins[2]: dTheta = dTh_bins[2]-0.1

                            dThetas[iMode][iSt].Fill(dTheta, dTheta_int)

                            # if dTheta_int == 0 and dTheta == 0: dTheta_ratio = 1
                            # elif dTheta == 0: dTheta_ratio = ratio_bins[2]-0.1
                            # else: dTheta_ratio = dTheta_int / dTheta

                            # if dTheta_ratio < ratio_bins[1]: dTheta_ratio = ratio_bins[1]+0.1
                            # if dTheta_ratio > ratio_bins[2]: dTheta_ratio = ratio_bins[2]-0.1
                            # dThetas[iMode][iSt].Fill(dTheta, dTheta_ratio)



    ## End loop over events

    out_file.cd()

    # for iMode in [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]:

    #     for iSt in dPhis[iMode].keys():
    #         dPhis[iMode][iSt].GetXaxis().SetTitle('dPhi_%s (degrees)' % iSt)
    #         dPhis[iMode][iSt].GetYaxis().SetTitle('LUT dPhi (int) / dPhi (degrees)')
    #         dPhis[iMode][iSt].Write()
    #         can = TCanvas(dPhis[iMode][iSt].GetName())
    #         can.cd()

    #         dPhis[iMode][iSt].Draw('colz')
    #         can.SaveAs('plots/png/%s.png' % dPhis[iMode][iSt].GetName())
    #         can.SaveAs('plots/pdf/%s.pdf' % dPhis[iMode][iSt].GetName())

    #     for iSt in dThetas[iMode].keys():
    #         dThetas[iMode][iSt].GetXaxis().SetTitle('dTheta_%s (degrees)' % iSt)
    #         dThetas[iMode][iSt].GetYaxis().SetTitle('LUT dTheta (int)')
    #         dThetas[iMode][iSt].Write()
    #         can = TCanvas(dThetas[iMode][iSt].GetName())
    #         can.cd()

    #         dThetas[iMode][iSt].Draw('colz')
    #         can.SaveAs('plots/png/%s.png' % dThetas[iMode][iSt].GetName())
    #         can.SaveAs('plots/pdf/%s.pdf' % dThetas[iMode][iSt].GetName())

    #     for iSt in FRs[iMode].keys():
    #         FRs[iMode][iSt].GetXaxis().SetTitle('LCT chamber')
    #         FRs[iMode][iSt].GetYaxis().SetTitle('LCT ring')
    #         FRs[iMode][iSt].Write()
    #         can = TCanvas(FRs[iMode][iSt].GetName())
    #         can.cd()

    #         FRs[iMode][iSt].Draw('colz')
    #         can.SaveAs('plots/png/%s.png' % FRs[iMode][iSt].GetName())
    #         can.SaveAs('plots/pdf/%s.pdf' % FRs[iMode][iSt].GetName())

    #     for iSt in CLCTs[iMode].keys():
    #         CLCTs[iMode][iSt].GetXaxis().SetTitle('LCT CLCT pattern')
    #         CLCTs[iMode][iSt].GetYaxis().SetTitle('LUT CLCT bits')
    #         CLCTs[iMode][iSt].Write()
    #         can = TCanvas(CLCTs[iMode][iSt].GetName())
    #         can.cd()

    #         CLCTs[iMode][iSt].Draw('colz')
    #         can.SaveAs('plots/png/%s.png' % CLCTs[iMode][iSt].GetName())
    #         can.SaveAs('plots/pdf/%s.pdf' % CLCTs[iMode][iSt].GetName())

    out_file.Close()

if __name__ == '__main__':
    main()
