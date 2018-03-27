#! /usr/bin/env python

## Compare rates coming out of unpacker and emulator

from ROOT import *
gROOT.SetBatch(False)
from Helper import *

def main():

    print 'Inside rates_L1T'
    
    prefix = 'root://eoscms//eos/cms'
    file_dir = '/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/279975_zbp0/'
    unp_uGMT = TChain('l1UpgradeTree/L1UpgradeTree')
    emu_uGMT = TChain('l1UpgradeEmuTree/L1UpgradeTree')
    unp_EMTF = TChain('l1UpgradeTfMuonTree/L1UpgradeTfMuonTree')
    emu_EMTF = TChain('l1UpgradeTfMuonEmuTree/L1UpgradeTfMuonTree')

    for i in range(99):
        file_name = '%s%sL1Ntuple_%d.root' % (prefix, file_dir, i+1)
        unp_uGMT.Add(file_name)
        emu_uGMT.Add(file_name)
        unp_EMTF.Add(file_name)
        emu_EMTF.Add(file_name)

    out_file = TFile('plots/rates_L1T_10k.root','recreate')

    dR_cut = -0.1

    #################
    ### Book counters
    #################

    SingleMu7 = {}
    SingleMu12 = {}
    SingleMu25 = {}
    DoubleMuOpen_Leg = {}
    DoubleMu_0_Leg = {}
    DoubleMu_3p5_Leg = {}
    DoubleMu_5_Leg = {}
    DoubleMu_10_Leg = {}
    DoubleMu_12_Leg = {}
    DoubleMuOpen = {}
    DoubleMu_0 = {}
    DoubleMu_12_5 = {}

    SingleMu7[0] = 0
    SingleMu12[0] = 0
    SingleMu25[0] = 0
    DoubleMuOpen_Leg[0] = 0
    DoubleMu_0_Leg[0] = 0
    DoubleMu_3p5_Leg[0] = 0
    DoubleMu_5_Leg[0] = 0
    DoubleMu_10_Leg[0] = 0
    DoubleMu_12_Leg[0] = 0
    DoubleMuOpen[0] = 0
    DoubleMu_0[0] = 0
    DoubleMu_12_5[0] = 0

    SingleMu7[1] = 0
    SingleMu12[1] = 0
    SingleMu25[1] = 0
    DoubleMuOpen_Leg[1] = 0
    DoubleMu_0_Leg[1] = 0
    DoubleMu_3p5_Leg[1] = 0
    DoubleMu_5_Leg[1] = 0
    DoubleMu_10_Leg[1] = 0
    DoubleMu_12_Leg[1] = 0
    DoubleMuOpen[1] = 0
    DoubleMu_0[1] = 0
    DoubleMu_12_5[1] = 0

    ###################
    ### Book histograms
    ###################

    phi_bins = [64, -3.2, 3.2]
    eta_bins = [50, -2.5, 2.5]
    qual_bins = [16, -0.5, 15.5]
    pT_bins = [521,-0.5,520.5]

    h_phi_SingleMu25_unp = TH1D('h_phi_SingleMu25_unp', 'Data phi, pass SingleMu25', phi_bins[0], phi_bins[1], phi_bins[2])
    h_phi_SingleMu25_emu = TH1D('h_phi_SingleMu25_emu', 'Emul phi, pass SingleMu25', phi_bins[0], phi_bins[1], phi_bins[2])
    h_eta_SingleMu25_unp = TH1D('h_eta_SingleMu25_unp', 'Data eta, pass SingleMu25', eta_bins[0], eta_bins[1], eta_bins[2])
    h_eta_SingleMu25_emu = TH1D('h_eta_SingleMu25_emu', 'Emul eta, pass SingleMu25', eta_bins[0], eta_bins[1], eta_bins[2])
    h_qual_SingleMu25_unp = TH1D('h_qual_SingleMu25_unp', 'Data qual, pass SingleMu25', qual_bins[0], qual_bins[1], qual_bins[2])
    h_qual_SingleMu25_emu = TH1D('h_qual_SingleMu25_emu', 'Emul qual, pass SingleMu25', qual_bins[0], qual_bins[1], qual_bins[2])
    h_pT_SingleMu25_unp = TH1D('h_pT_SingleMu25_unp', 'Data pT, pass SingleMu25', pT_bins[0], pT_bins[1], pT_bins[2])
    h_pT_SingleMu25_emu = TH1D('h_pT_SingleMu25_emu', 'Emul pT, pass SingleMu25', pT_bins[0], pT_bins[1], pT_bins[2])

    h_eta_2D_DoubleMu0_unp = TH2D('h_eta_2D_DoubleMu0_unp', 'Data eta_1 vs. eta_2, pass DoubleMu0', eta_bins[0], eta_bins[1], eta_bins[2], eta_bins[0], eta_bins[1], eta_bins[2])
    h_eta_2D_DoubleMu0_emu = TH2D('h_eta_2D_DoubleMu0_emu', 'Emul eta_1 vs. eta_2, pass DoubleMu0', eta_bins[0], eta_bins[1], eta_bins[2], eta_bins[0], eta_bins[1], eta_bins[2])

    ## Main event loop    
    for iEvt in range(unp_uGMT.GetEntries()):
        
        if (iEvt > 10000): break
        if iEvt % 100 is 0: print 'Event #', iEvt
        unp_uGMT.GetEntry(iEvt)
        emu_uGMT.GetEntry(iEvt)
        unp_EMTF.GetEntry(iEvt)
        emu_EMTF.GetEntry(iEvt)

        unp_tree = unp_uGMT.L1Upgrade
        emu_tree = emu_uGMT.L1Upgrade
        unp_emtf = unp_EMTF.L1UpgradeEmtfMuon
        emu_emtf = emu_EMTF.L1UpgradeEmtfMuon

        ## See if unpacked tracks would fire the trigger
        SingleMu7_pass = False
        SingleMu12_pass = False
        SingleMu25_pass = False
        DoubleMuOpen_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_0_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_3p5_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_5_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_10_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_12_Leg_pass = [False, 0.0, 0.0]
        DoubleMuOpen_pass = False
        DoubleMu_0_pass = False
        DoubleMu_12_5_pass = False

        for iTrk in range(unp_tree.nMuons):
            if unp_tree.muonBx[iTrk] != 0:
                continue

            Qual = unp_tree.muonQual[iTrk]
            Eta = unp_tree.muonEta[iTrk]
            Phi = unp_tree.muonPhi[iTrk]
            Pt = unp_tree.muonEt[iTrk]

            if (Qual >= 12 and Pt >= 7): 
                if not SingleMu7_pass: SingleMu7[0] += 1
                SingleMu7_pass = True
            if (Qual >= 12 and Pt >= 12): 
                if not SingleMu12_pass: SingleMu12[0] += 1
                SingleMu12_pass = True
            if (Qual >= 12 and Pt >= 25): 
                if not SingleMu25_pass: SingleMu25[0] += 1
                SingleMu25_pass = True
                h_phi_SingleMu25_unp.Fill( Phi )
                h_eta_SingleMu25_unp.Fill( Eta )
                h_qual_SingleMu25_unp.Fill( Qual )
                h_pT_SingleMu25_unp.Fill( min(Pt, pT_bins[2]-0.01) )
            if (Qual >= 4): 
                if not DoubleMuOpen_Leg_pass[0]: 
                    DoubleMuOpen_Leg[0] += 1
                    DoubleMuOpen_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMuOpen_Leg_pass[1], DoubleMuOpen_Leg_pass[2] ) > dR_cut:
                    if not DoubleMuOpen_pass: DoubleMuOpen[0] += 1
                    DoubleMuOpen_pass = True
            if (Qual >= 8 and Pt >= 0):
                if not DoubleMu_0_Leg_pass[0]: 
                    DoubleMu_0_Leg[0] += 1
                    DoubleMu_0_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMu_0_Leg_pass[1], DoubleMu_0_Leg_pass[2] ) > dR_cut:
                    if Pt >= 0 and not DoubleMu_0_pass: 
                        DoubleMu_0[0] += 1
                        DoubleMu_0_pass = True
                        h_eta_2D_DoubleMu0_unp.Fill(DoubleMu_0_Leg_pass[1], Eta)
            if (Qual >= 8 and Pt >= 3.5): 
                if not DoubleMu_3p5_Leg_pass[0]: DoubleMu_3p5_Leg[0] += 1
                DoubleMu_3p5_Leg_pass = [True, Eta, Phi]
            if (Qual >= 8 and Pt >= 5): 
                if not DoubleMu_5_Leg_pass[0]: 
                    DoubleMu_5_Leg[0] += 1
                    DoubleMu_5_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMu_5_Leg_pass[1], DoubleMu_5_Leg_pass[2] ) > dR_cut:
                    if Pt >= 12 and not DoubleMu_12_5_pass:
                        DoubleMu_12_5[0] += 1
                        DoubleMu_12_5_pass = True
            if (Qual >= 8 and Pt >= 10): 
                if not DoubleMu_10_Leg_pass[0]: DoubleMu_10_Leg[0] += 1
                DoubleMu_10_Leg_pass = [True, Eta, Phi]
            if (Qual >= 8 and Pt >= 12): 
                if not DoubleMu_12_Leg_pass[0]: 
                    DoubleMu_12_Leg[0] += 1
                    DoubleMu_12_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMu_12_Leg_pass[1], DoubleMu_12_Leg_pass[2] ) > dR_cut:
                    if Pt >= 5 and not DoubleMu_12_5_pass: 
                        DoubleMu_12_5[0] += 1
                        DoubleMu_12_5_pass = True

        if DoubleMu_0_pass: DoubleMu_0_pass_unp = True
        else: DoubleMu_0_pass_unp = False

        ## See if emulator tracks would fire the trigger
        SingleMu7_pass = False
        SingleMu12_pass = False
        SingleMu25_pass = False
        DoubleMuOpen_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_0_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_3p5_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_5_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_10_Leg_pass = [False, 0.0, 0.0]
        DoubleMu_12_Leg_pass = [False, 0.0, 0.0]
        DoubleMuOpen_pass = False
        DoubleMu_0_pass = False
        DoubleMu_12_5_pass = False

        for iTrk in range(emu_tree.nMuons):
            if emu_tree.muonBx[iTrk] != 0:
                continue

            Qual = emu_tree.muonQual[iTrk]
            Eta = emu_tree.muonEta[iTrk]
            Phi = emu_tree.muonPhi[iTrk]
            Pt = emu_tree.muonEt[iTrk]

            if (Qual >= 12 and Pt >= 7): 
                if not SingleMu7_pass: SingleMu7[1] += 1
                SingleMu7_pass = True
            if (Qual >= 12 and Pt >= 12): 
                if not SingleMu12_pass: SingleMu12[1] += 1
                SingleMu12_pass = True
            if (Qual >= 12 and Pt >= 25): 
                if not SingleMu25_pass: SingleMu25[1] += 1
                SingleMu25_pass = True
                h_phi_SingleMu25_emu.Fill( Phi )
                h_eta_SingleMu25_emu.Fill( Eta )
                h_qual_SingleMu25_emu.Fill( Qual )
                h_pT_SingleMu25_emu.Fill( min(Pt, pT_bins[2]-0.01) )
            if (Qual >= 4): 
                if not DoubleMuOpen_Leg_pass[0]: 
                    DoubleMuOpen_Leg[1] += 1
                    DoubleMuOpen_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMuOpen_Leg_pass[1], DoubleMuOpen_Leg_pass[2] ) > dR_cut:
                    if not DoubleMuOpen_pass: DoubleMuOpen[1] += 1
                    DoubleMuOpen_pass = True
            if (Qual >= 8 and Pt >= 0):
                if not DoubleMu_0_Leg_pass[0]: 
                    DoubleMu_0_Leg[1] += 1
                    DoubleMu_0_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMu_0_Leg_pass[1], DoubleMu_0_Leg_pass[2] ) > dR_cut:
                    if Pt >= 0 and not DoubleMu_0_pass: 
                        DoubleMu_0[1] += 1
                        DoubleMu_0_pass = True
                        h_eta_2D_DoubleMu0_emu.Fill(DoubleMu_0_Leg_pass[1], Eta)
            if (Qual >= 8 and Pt >= 3.5): 
                if not DoubleMu_3p5_Leg_pass[0]: DoubleMu_3p5_Leg[1] += 1
                DoubleMu_3p5_Leg_pass = [True, Eta, Phi]
            if (Qual >= 8 and Pt >= 5): 
                if not DoubleMu_5_Leg_pass[0]: 
                    DoubleMu_5_Leg[1] += 1
                    DoubleMu_5_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMu_5_Leg_pass[1], DoubleMu_5_Leg_pass[2] ) > dR_cut:
                    if Pt >= 12 and not DoubleMu_12_5_pass:
                        DoubleMu_12_5[1] += 1
                        DoubleMu_12_5_pass = True
            if (Qual >= 8 and Pt >= 10): 
                if not DoubleMu_10_Leg_pass[0]: DoubleMu_10_Leg[1] += 1
                DoubleMu_10_Leg_pass = [True, Eta, Phi]
            if (Qual >= 8 and Pt >= 12): 
                if not DoubleMu_12_Leg_pass[0]: 
                    DoubleMu_12_Leg[1] += 1
                    DoubleMu_12_Leg_pass = [True, Eta, Phi]
                elif CalcDR( Eta, Phi, DoubleMu_12_Leg_pass[1], DoubleMu_12_Leg_pass[2] ) > dR_cut:
                    if Pt >= 5 and not DoubleMu_12_5_pass: 
                        DoubleMu_12_5[1] += 1
                        DoubleMu_12_5_pass = True


        if DoubleMu_0_pass != DoubleMu_0_pass_unp:
            print '\n*** Unpacked (emulator) DoubleMu_0 = %s (%s) ***' % (DoubleMu_0_pass_unp, DoubleMu_0_pass)

            print 'Unpacked uGMT output tracks'
            for iTrk in range(unp_tree.nMuons):
                if unp_tree.muonBx[iTrk] != 0: continue
                print 'pT (hw) = %.1f (%d), eta (hw) = %.2f (%d), phi (hw) = %.2f (%d), qual = %d' % (unp_tree.muonEt[iTrk], unp_tree.muonIEt[iTrk],
                                                                                                      unp_tree.muonEta[iTrk], unp_tree.muonIEta[iTrk],
                                                                                                      unp_tree.muonPhi[iTrk], unp_tree.muonIPhi[iTrk],
                                                                                                      unp_tree.muonQual[iTrk])
            print 'Unpacked uGMT input tracks from EMTF'
            for iTrk in range(unp_emtf.nTfMuons):
                if unp_emtf.tfMuonBx[iTrk] != 0: continue
                print 'pT (hw) = (%d), eta (hw) = (%d), phi (hw) = %.2f (%d), qual = %d' % (unp_emtf.tfMuonHwPt[iTrk], unp_emtf.tfMuonHwEta[iTrk],
                                                                                            unp_emtf.tfMuonGlobalPhi[iTrk], unp_emtf.tfMuonHwPhi[iTrk],
                                                                                            unp_emtf.tfMuonHwQual[iTrk])
            print 'Emulator uGMT output tracks'
            for iTrk in range(emu_tree.nMuons):
                if emu_tree.muonBx[iTrk] != 0: continue
                print 'pT (hw) = %.1f (%d), eta (hw) = %.2f (%d), phi (hw) = %.2f (%d), qual = %d' % (emu_tree.muonEt[iTrk], emu_tree.muonIEt[iTrk],
                                                                                                      emu_tree.muonEta[iTrk], emu_tree.muonIEta[iTrk],
                                                                                                      emu_tree.muonPhi[iTrk], emu_tree.muonIPhi[iTrk],
                                                                                                      emu_tree.muonQual[iTrk])
            print 'Emulator uGMT input tracks from EMTF'
            for iTrk in range(emu_emtf.nTfMuons):
                if emu_emtf.tfMuonBx[iTrk] != 0: continue
                print 'pT (hw) = (%d), eta (hw) = (%d), phi (hw) = %.2f (%d), qual = %d' % (emu_emtf.tfMuonHwPt[iTrk], emu_emtf.tfMuonHwEta[iTrk],
                                                                                            emu_emtf.tfMuonGlobalPhi[iTrk], emu_emtf.tfMuonHwPhi[iTrk],
                                                                                            emu_emtf.tfMuonHwQual[iTrk])
           



    print '***************************************************************************'
    print '*******                   uGMT rates: run 279975                    *******'
    print '***************************************************************************'
    print '                  Unpacker   -   Emulator - Unp. frac. x 1000000 - Unp./Emu. ratio'
    print 'Number of events   %7d        %7d          %7d            %.2f'  % (iEvt, iEvt, 1000000, 1)
    print 'SingleMu7          %7d        %7d          %7d            %.2f'  % (SingleMu7[0], SingleMu7[1], 1000000*SingleMu7[0]/iEvt, 1.0*SingleMu7[0]/SingleMu7[1]) 
    print 'SingleMu12         %7d        %7d          %7d            %.2f'  % (SingleMu12[0], SingleMu12[1], 1000000*SingleMu12[0]/iEvt, 1.0*SingleMu12[0]/SingleMu12[1]) 
    print 'SingleMu25         %7d        %7d          %7d            %.2f'  % (SingleMu25[0], SingleMu25[1], 1000000*SingleMu25[0]/iEvt, 1.0*SingleMu25[0]/SingleMu25[1]) 
    print 'DoubleMuOpen_Leg   %7d        %7d          %7d            %.2f'  % (DoubleMuOpen_Leg[0], DoubleMuOpen_Leg[1], 1000000*DoubleMuOpen_Leg[0]/iEvt, 1.0*DoubleMuOpen_Leg[0]/DoubleMuOpen_Leg[1]) 
    print 'DoubleMu_0_Leg     %7d        %7d          %7d            %.2f'  % (DoubleMu_0_Leg[0], DoubleMu_0_Leg[1], 1000000*DoubleMu_0_Leg[0]/iEvt, 1.0*DoubleMu_0_Leg[0]/DoubleMu_0_Leg[1]) 
    print 'DoubleMu_3p5_Leg   %7d        %7d          %7d            %.2f'  % (DoubleMu_3p5_Leg[0], DoubleMu_3p5_Leg[1], 1000000*DoubleMu_3p5_Leg[0]/iEvt, 1.0*DoubleMu_3p5_Leg[0]/DoubleMu_3p5_Leg[1]) 
    print 'DoubleMu_5_Leg     %7d        %7d          %7d            %.2f'  % (DoubleMu_5_Leg[0], DoubleMu_5_Leg[1], 1000000*DoubleMu_5_Leg[0]/iEvt, 1.0*DoubleMu_5_Leg[0]/DoubleMu_5_Leg[1]) 
    print 'DoubleMu_10_Leg    %7d        %7d          %7d            %.2f'  % (DoubleMu_10_Leg[0], DoubleMu_10_Leg[1], 1000000*DoubleMu_10_Leg[0]/iEvt, 1.0*DoubleMu_10_Leg[0]/DoubleMu_10_Leg[1]) 
    print 'DoubleMu_12_Leg    %7d        %7d          %7d            %.2f'  % (DoubleMu_12_Leg[0], DoubleMu_12_Leg[1], 1000000*DoubleMu_12_Leg[0]/iEvt, 1.0*DoubleMu_12_Leg[0]/DoubleMu_12_Leg[1]) 
    print 'DoubleMuOpen       %7d        %7d          %7d            %.2f'  % (DoubleMuOpen[0], DoubleMuOpen[1], 1000000*DoubleMuOpen[0]/iEvt, 1.0*DoubleMuOpen[0]/DoubleMuOpen[1]) 
    print 'DoubleMu_0         %7d        %7d          %7d            %.2f'  % (DoubleMu_0[0], DoubleMu_0[1], 1000000*DoubleMu_0[0]/iEvt, 1.0*DoubleMu_0[0]/DoubleMu_0[1]) 
    print 'DoubleMu_12_5      %7d        %7d          %7d            %.2f'  % (DoubleMu_12_5[0], DoubleMu_12_5[1], 1000000*DoubleMu_12_5[0]/iEvt, 1.0*DoubleMu_12_5[0]/DoubleMu_12_5[1]) 


    out_file.cd()

    h_phi_SingleMu25_unp.SetLineWidth(2)
    h_phi_SingleMu25_unp.SetLineColor(kBlack)
    h_phi_SingleMu25_unp.Write()
    h_phi_SingleMu25_emu.SetLineWidth(2)
    h_phi_SingleMu25_emu.SetLineColor(kRed)
    h_phi_SingleMu25_emu.Write()
    h_eta_SingleMu25_unp.SetLineWidth(2)
    h_eta_SingleMu25_unp.SetLineColor(kBlack)
    h_eta_SingleMu25_unp.Write()
    h_eta_SingleMu25_emu.SetLineWidth(2)
    h_eta_SingleMu25_emu.SetLineColor(kRed)
    h_eta_SingleMu25_emu.Write()
    h_qual_SingleMu25_unp.SetLineWidth(2)
    h_qual_SingleMu25_unp.SetLineColor(kBlack)
    h_qual_SingleMu25_unp.Write()
    h_qual_SingleMu25_emu.SetLineWidth(2)
    h_qual_SingleMu25_emu.SetLineColor(kRed)
    h_qual_SingleMu25_emu.Write()
    h_pT_SingleMu25_unp.SetLineWidth(2)
    h_pT_SingleMu25_unp.SetLineColor(kBlack)
    h_pT_SingleMu25_unp.Write()
    h_pT_SingleMu25_emu.SetLineWidth(2)
    h_pT_SingleMu25_emu.SetLineColor(kRed)
    h_pT_SingleMu25_emu.Write()

    h_eta_2D_DoubleMu0_unp.Write()
    h_eta_2D_DoubleMu0_emu.Write()

    out_file.Close()

if __name__ == '__main__':
    main()
