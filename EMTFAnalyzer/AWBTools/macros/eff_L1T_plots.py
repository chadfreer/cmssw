#! /usr/bin/env python

###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT
from eff_modules import *

# Root file of Histograms
pt_cut = 'Pt12'
suffix = ''
#suffix = '_sectM6'

# in_file = TFile( 'plots/L1T_eff_%s_297606_dEta_BX0_uGMT_HLT%s.root' % (pt_cut, suffix) )
in_file = TFile( 'plots/L1T_eff_%s_2017B_dEta_BX0_uGMT_HLT%s.root' % (pt_cut, suffix) )

WPs = {}
WPs['SingleMu']  = [kRed]
WPs['SingleMu7'] = [kGreen]
WPs['DoubleMu']  = [kBlue]
WPs['MuOpen']    = [kBlack]

TFs = ['uGMT', 'EMTF']

for TF in TFs: 
    h_pt  = in_file.Get('h_pt_%s' % TF)
    h_eta = in_file.Get('h_eta_%s' % TF)
    h_phi = in_file.Get('h_phi_%s' % TF)

    c_pt  = TCanvas('c_pt')
    c_eta = TCanvas('c_eta')
    c_phi = TCanvas('c_phi')
    
    c_pt.SetGridx()
    c_pt.SetGridy()
    c_eta.SetGridx()
    c_eta.SetGridy()
    c_phi.SetGridx()
    c_phi.SetGridy()
    
    mg_pt  = TMultiGraph()
    mg_eta = TMultiGraph()
    mg_phi = TMultiGraph()

    nWPs = 0
    for WP in WPs.keys():
        nWPs += 1
        key = '%s_%s' % (TF, WP)
        h_pt_trg  = in_file.Get('h_pt_%s' % key)
        h_eta_trg = in_file.Get('h_eta_%s' % key)
        h_phi_trg = in_file.Get('h_phi_%s' % key)

        eff_pt  = TGraphAsymmErrors(h_pt_trg, h_pt, '')
        eff_eta = TGraphAsymmErrors(h_eta_trg, h_eta, '')
        eff_phi = TGraphAsymmErrors(h_phi_trg, h_phi, '')

        eff_pt.SetLineColor(WPs[WP][0])
        eff_pt.SetMarkerColor(WPs[WP][0])
        eff_pt.SetLineWidth(1)
        eff_pt.SetMarkerStyle(23)
        eff_pt.SetMarkerSize(0.8)
        eff_pt.SetTitle(' GeV')
        eff_pt.GetXaxis().SetTitle("p_{T}(Probe Reco #mu)")
        eff_pt.GetYaxis().SetTitle("TF Efficiency")
        eff_pt.GetYaxis().SetTitleOffset(1.35)
        eff_pt.GetXaxis().SetNdivisions(509)
        eff_pt.GetYaxis().SetNdivisions(514)
        eff_pt.SetMinimum(0)
        eff_pt.SetMaximum(1.02)
        mg_pt.Add(eff_pt)

        eff_eta.SetLineColor(WPs[WP][0])
        eff_eta.SetMarkerColor(WPs[WP][0])
        eff_eta.SetLineWidth(1)
        eff_eta.SetMarkerStyle(23)
        eff_eta.SetMarkerSize(0.8)
        eff_eta.SetTitle(' GeV')
        eff_eta.GetXaxis().SetTitle("|#eta(Probe Reco #mu)|")
        eff_eta.GetYaxis().SetTitle("TF Efficiency")
        eff_eta.GetYaxis().SetTitleOffset(1.35)
        eff_eta.GetXaxis().SetNdivisions(509)
        eff_eta.GetYaxis().SetNdivisions(514)
        eff_eta.SetMinimum(0)
        eff_eta.SetMaximum(1.02)
        mg_eta.Add(eff_eta)

        eff_phi.SetLineColor(WPs[WP][0])
        eff_phi.SetMarkerColor(WPs[WP][0])
        eff_phi.SetLineWidth(1)
        eff_phi.SetMarkerStyle(23)
        eff_phi.SetMarkerSize(0.8)
        eff_phi.SetTitle(' GeV')
        eff_phi.GetXaxis().SetTitle("|#phi(Probe Reco #mu)|")
        eff_phi.GetYaxis().SetTitle("TF Efficiency")
        eff_phi.GetYaxis().SetTitleOffset(1.35)
        eff_phi.GetXaxis().SetNdivisions(509)
        eff_phi.GetYaxis().SetNdivisions(514)
        eff_phi.SetMinimum(0)
        eff_phi.SetMaximum(1.02)
        mg_phi.Add(eff_phi)

    c_pt.cd()
    mg_pt.Draw('APLX')  ## APLX
    c_pt. SaveAs('plots/png/%s_eff_pt_%s%s.png' % (TF, pt_cut, suffix))
    c_pt. SaveAs('plots/pdf/%s_eff_pt_%s%s.pdf' % (TF, pt_cut, suffix))
    
    c_eta.cd()
    mg_eta.Draw('APLX')  ## APLX
    c_eta.SaveAs('plots/png/%s_eff_eta_%s%s.png' % (TF, pt_cut, suffix))
    c_eta.SaveAs('plots/pdf/%s_eff_eta_%s%s.pdf' % (TF, pt_cut, suffix))
    
    c_phi.cd()
    mg_phi.Draw('APLX')  ## APLX
    c_phi.SaveAs('plots/png/%s_eff_phi_%s%s.png' % (TF, pt_cut, suffix))
    c_phi.SaveAs('plots/pdf/%s_eff_phi_%s%s.pdf' % (TF, pt_cut, suffix))


# # ===============================================================

# variable_list = [
#     ['hpt_emtf', 'EMTF p_{T}', 50, 0, 150],
#     ['hpt_bmtf', 'BMTF p_{T}', 50, 0, 150],
#     ['hpt_omtf', 'OMTF p_{T}', 50, 0, 150]
#     ]

# def doPlot(variable, xaxis, nbins, bin_low, bin_high):

#     canvas = TCanvas('canvas')
#     hist = in_file.Get(variable)
#     hist.GetXaxis().SetLimits(bin_low, bin_high)
#     hist.GetXaxis().SetTitle(xaxis)

#     hist.SetFillColor(kYellow)
#     hist.SetStats(0)
#     hist.Draw()

#     canvas.SaveAs('plots/pdf/'+variable+'.pdf')
#     canvas.SaveAs('plots/png/'+variable+'.png')

#     canvas.IsA().Destructor(canvas)
#     hist.IsA().Destructor(hist)


#for variable in variable_list:
#    doPlot(variable[0], variable[1], variable[2], variable[3], variable[4])


