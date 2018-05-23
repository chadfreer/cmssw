#! /usr/bin/env python

import ROOT

def main():
    
    print 'Inside Draw_MuGun_RPC.py'
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    
    print 'Accessing files'
    file_name = 'plots/MuGun_RPC_SingleMu_eff.root'
    in_file = ROOT.TFile.Open(file_name)

    out_png = 'plots/png/'
    out_pdf = 'plots/pdf/'
    
    ## Import Thomas Reis' global style settings
    font = 42
    fontSize = 0.04
    set_root_style(font)
    
    for iMode in ['SingleMu', 'mode_15']:
        
        canv = ROOT.TCanvas('c_%s' % iMode)
        canv.cd()
        canv.SetTopMargin(0.08)
        canv.SetBottomMargin(0.12)
        
        h_eff_CSC = in_file.Get('h_eta_eff_%s_pt_10_200_noRPC' % iMode) 
        h_eff_RPC = in_file.Get('h_eta_eff_%s_pt_10_200_RPC' % iMode) 

        for i in range(h_eff_CSC.GetNbinsX()):
            if ( h_eff_CSC.GetBinContent(i+1) + h_eff_CSC.GetBinError(i+1) > 1 ):
                h_eff_CSC.SetBinError( i+1, 1 - h_eff_CSC.GetBinContent(i+1) )
            if ( h_eff_RPC.GetBinContent(i+1) + h_eff_RPC.GetBinError(i+1) > 1 ):
                h_eff_RPC.SetBinError( i+1, 1 - h_eff_RPC.GetBinContent(i+1) )
                
        leg = ROOT.TLegend(0.65, 0.15, 0.885, 0.35)
        
        ###################################################
        ###  Histogram style settings from Thomas Reis  ###
        ###################################################
        
        h_eff_CSC.GetXaxis().SetTitleFont(font)
        h_eff_CSC.GetXaxis().SetLabelFont(font)
        h_eff_CSC.GetXaxis().SetLabelSize(fontSize)
        h_eff_CSC.GetXaxis().SetNoExponent()
        h_eff_CSC.GetYaxis().SetTitleOffset(1.5)
        h_eff_CSC.GetYaxis().SetTitleFont(font)
        h_eff_CSC.GetYaxis().SetLabelFont(font)
        h_eff_CSC.GetYaxis().SetLabelSize(fontSize)


        #################################################
        ###  Histogram drawing by Andrew Brinkerhoff  ###
        #################################################

        h_eff_CSC.SetLineWidth(2)
        h_eff_CSC.SetLineColor(ROOT.kBlack)
        h_eff_CSC.SetMarkerStyle(8)
        h_eff_CSC.SetMarkerSize(0.95)
        h_eff_CSC.SetMarkerColor(ROOT.kBlack)
        h_eff_RPC.SetLineWidth(2)
        h_eff_RPC.SetLineColor(ROOT.kRed)
        h_eff_RPC.SetMarkerStyle(8)
        h_eff_RPC.SetMarkerSize(0.7)
        h_eff_RPC.SetMarkerColor(ROOT.kRed)

        if (iMode == 'SingleMu'):
            h_eff_CSC.SetTitle('EMTF Single Muon reconstruction efficiency')
        if (iMode == 'mode_15'):
            h_eff_CSC.SetTitle('EMTF 4-station reconstruction efficiency')
        h_eff_CSC.GetYaxis().SetTitle('Efficiency')
        h_eff_CSC.GetXaxis().SetTitle('Muon |#eta|')

        ROOT.gStyle.SetTitleH(0.065)
        ROOT.gStyle.SetTitleW(0.8)
        h_eff_CSC.GetYaxis().SetTitleSize(0.045)
        h_eff_CSC.GetXaxis().SetTitleSize(0.05)
        h_eff_CSC.GetYaxis().SetTitleOffset(0.80)
        h_eff_CSC.GetXaxis().SetTitleOffset(0.90)
        
        leg.AddEntry(h_eff_CSC, 'CSC-only')
        leg.AddEntry(h_eff_RPC, 'CSC+RPC')


        h_eff_CSC.GetXaxis().SetRangeUser(1.20, 2.40)

        if (iMode == 'SingleMu'):
            h_eff_CSC.GetYaxis().SetRangeUser(0.48, 1.15)
            h_eff_CSC.Draw('e1')
            h_eff_RPC.Draw('e1same')
        if (iMode == 'mode_15'):
            h_eff_CSC.GetYaxis().SetRangeUser(0.0, 1.08)
            h_eff_CSC.Draw('histe1')
            h_eff_RPC.Draw('histe1same')

        leg.Draw()


        ############################################
        ###  CMS text settings from Thomas Reis  ###
        ############################################
        
        cmsText = "CMS"
        cmsTextFont = 61
        cmsTextSize = 0.05
        
        extraText   = "Preliminary"
        extraTextFont = 52
        extraOverCmsTextSize = 0.8

        if (iMode == 'SingleMu'):
            y1 = 1.111
            y2 = 1.068
        if (iMode == 'mode_15'):
            y1 = 1.015
            y2 = 0.950

        tex = ROOT.TLatex()
        tex.SetTextFont(cmsTextFont)
        tex.SetTextSize(cmsTextSize)
        # tex.DrawLatex(0.14, 0.93, cmsText)
        tex.DrawLatex(2.04, y1, cmsText)
        tex.SetTextFont(extraTextFont)
        tex.SetTextSize(cmsTextSize*extraOverCmsTextSize)
        # tex.DrawLatex(0.26, 0.93, extraText)
        tex.DrawLatex(2.16, y1, extraText)
        tex.SetTextFont(font)
        tex.SetTextAlign(31)
        tex.DrawLatex(2.38, y2, 'Simulation (13 TeV)')

        ROOT.gPad.SetGridx(True)
        ROOT.gPad.SetGridy(True)

        ## Save out the canvas
        canv.SaveAs(out_png+'MuGun_RPC_%s.png' % iMode)
        canv.SaveAs(out_pdf+'MuGun_RPC_%s.pdf' % iMode)

        
    ## End loop: for iMode in ['SingleMu', 'mode_15']:
        
## End function: def main()

def set_root_style(font):
    ROOT.gStyle.SetTitleFont(font)
    ROOT.gStyle.SetStatFont(font)
    ROOT.gStyle.SetTextFont(font)
    ROOT.gStyle.SetLabelFont(font)
    ROOT.gStyle.SetLegendFont(font)
    ROOT.gStyle.SetMarkerStyle(20)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    # ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetNumberContours(99)
    # ROOT.gPad.SetTopMargin(0.08)
    # ROOT.gPad.SetLeftMargin(0.14)
    # ROOT.gPad.SetRightMargin(0.10)
    # ROOT.gPad.SetTickx(1)
    # ROOT.gPad.SetTicky(1)
    # ROOT.gPad.SetGridx(True)
    # ROOT.gPad.SetGridy(True)
        


if __name__ == '__main__':
    main()



    
