#! /usr/bin/env python

import sys
import math
from ROOT import *
import numpy as np
from array import *
# from eff_modules import *

def main():

    out_file = TFile('plots/HLT_muon_rate.root', 'recreate')

    # ########################################################################
    # ###  Rates taken from run 283964, LS 20 - 380, in prescale column 8  ###
    # ########################################################################
    # ## Fill 5448:    https://vocms0186.cern.ch/cmsdb/servlet/FillReport?FILL=5448
    # ## Run summary:  https://vocms0186.cern.ch/cmsdb/servlet/RunSummary?RUN=283964
    # ## Trigger menu: https://vocms0186.cern.ch/cmsdb/servlet/TriggerMode?KEY=l1_hlt_collisions2016/v451
    # ## L1 rates:     https://vocms0186.cern.ch/cmsdb/servlet/L1Summary?RUN=283964&KEY=collisions2016_TSC/v178
    # ## HLT rates:    https://vocms0186.cern.ch/cmsdb/servlet/HLTSummary?RUN=283964&NAME=/cdaq/physics/Run2016/25ns15e33/v4.2.3/HLT/V2

    # nSeconds   = 23.3 * 360
    
    # # ## All data points
    # # pt_vals    = [   8.0,   17.0,   20.0,   27.0,  50.0,  55.0]
    # # pt_errs    = [   0.0,    0.0,    0.0,    0.0,   0.0,   0.0]
    # # raw_rates  = [0.9027, 1.7536, 1.0625, 1.2755, 17.38, 11.82]
    # # PS_vals    = [70*313,  140*4,  1*438,  1*140,   1*1,   1*1]

    # # ## Removing anomalous HLT_Mu_20
    # # pt_vals    = [   8.0,   17.0,   27.0,  50.0,  55.0]
    # # pt_errs    = [   0.0,    0.0,    0.0,   0.0,   0.0]
    # # raw_rates  = [0.9027, 1.7536, 1.2755, 17.38, 11.82]
    # # PS_vals    = [70*313,  140*4,  1*140,   1*1,   1*1]

    # # ## Removing HLT_Mu_8
    # # pt_vals    = [  17.0,   20.0,   27.0,  50.0,  55.0]
    # # pt_errs    = [   0.0,    0.0,    0.0,   0.0,   0.0]
    # # raw_rates  = [1.7536, 1.0625, 1.2755, 17.38, 11.82]
    # # PS_vals    = [ 140*4,  1*438,  1*140,   1*1,   1*1]

    # ## Removing high-pT bins
    # pt_vals    = [   8.0,   17.0,   20.0,   27.0]
    # pt_errs    = [   0.0,    0.0,    0.0,    0.0]
    # raw_rates  = [0.9027, 1.7536, 1.0625, 1.2755]
    # PS_vals    = [70*313,  140*4,  1*438,  1*140]


    # true_rates = []
    # rate_errs  = []
    # for i in range(len(pt_vals)):
    #     true_rates.append( raw_rates[i] * PS_vals[i] )
    #     rate_errs.append( true_rates[i] / math.sqrt(raw_rates[i] * nSeconds) )
    #     print 'For pT > %2d, rate = %8.2f +/- %7.3f (%.2f percent)' % ( pt_vals[i], true_rates[i], rate_errs[i], 
    #                                                                     100.*rate_errs[i]/true_rates[i] ) 

    ##################################################
    ###  Rates taken from TDR plot from Khristian  ###
    ##################################################

    # ## Full pT range
    # pt_vals    = [   3.0,    5.0,   9.0, 12.0, 16.0, 20.0, 26.0, 33.0, 38.0, 48.0]
    # pt_errs    = [   0.0,    0.0,   0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    # true_rates = [480000, 100000, 10000, 3000, 1000,  500,  200,  100,   60,   20]

    # ## Low pT
    # pt_vals    = [   3.0,    5.0,   9.0, 12.0]
    # pt_errs    = [   0.0,    0.0,   0.0,  0.0]
    # true_rates = [480000, 100000, 10000, 3000]

    # ## Medium pT
    # pt_vals    = [12.0, 16.0, 20.0, 26.0]
    # pt_errs    = [ 0.0,  0.0,  0.0,  0.0]
    # true_rates = [3000, 1000,  500,  200]
    
    ## High pT
    pt_vals    = [26.0, 33.0, 38.0, 48.0]
    pt_errs    = [ 0.0,  0.0,  0.0,  0.0]
    true_rates = [ 200,  100,   60,   20]

    # ## Removing high pT muons
    # pt_vals    = [   3.0,    5.0,   9.0, 12.0, 16.0, 20.0, 26.0]
    # pt_errs    = [   0.0,    0.0,   0.0,  0.0,  0.0,  0.0,  0.0]
    # true_rates = [480000, 100000, 10000, 3000, 1000,  500,  200]

    
    rate_errs  = []
    for i in range(len(pt_vals)):
        rate_errs.append( true_rates[i] / 10. )
        print 'For pT > %2d, rate = %8.2f +/- %7.3f (%.2f percent)' % ( pt_vals[i], true_rates[i], rate_errs[i], 
                                                                        100.*rate_errs[i]/true_rates[i] ) 


    #######################################
    ###  Plotting and fitting of rates  ###
    #######################################

    pt_vals    = array('d', pt_vals)
    pt_errs    = array('d', pt_errs)
    true_rates = array('d', true_rates)
    rate_errs  = array('d', rate_errs)

    out_file.cd()

    g_rate_vs_threshold = TGraphErrors(len(pt_vals), pt_vals, true_rates, pt_errs, rate_errs)
    g_rate_vs_threshold.SetName('g_rate_vs_threshold')
    g_rate_vs_threshold.Write()

    ROOT.Math.MinimizerOptions.SetDefaultTolerance(0.001)

    # ## Basic fit
    # fit1 = TF1('fit1', '[0]*pow(x - [1], -1.*[2])')
    # fit1.SetParameter(0, 30000000)
    # fit1.SetParameter(1, 1.0)
    # ## fit1.FixParameter(1, 0.0)
    # fit1.SetParameter(2, 3.5)
    # g_rate_vs_threshold.Fit(fit1)
    # fit1.Write()

    # c0 = fit1.GetParameter(0)
    # c1 = fit1.GetParameter(1)
    # c2 = fit1.GetParameter(2)
    # print '\nBest-fit parameters for c0*(pT - c1)^(-c2) are c0 = %.0f, c1 = %.2f, c2 = %.2f\n' % ( c0, c1, c2 )
    # for i in range(len(pt_vals)):
    #     print 'True rate for pT > %2d = %8.2f, predicted = %8.2f, ratio = %.3f' % ( pt_vals[i], true_rates[i], c0*pow(pt_vals[i] - c1, -1.*c2),
    #                                                                               c0*pow(pt_vals[i] - c1, -1.*c2) / true_rates[i] )


    ## More complex, pT-dependent fit
    fit1 = TF1('fit1', '[0]*pow(x - [1], -1.*([2] + [3]*pow(x - [1], [4])))')
    fit1.SetParameter(0, 30000000)
    fit1.SetParameter(1, 1.0)
    fit1.SetParameter(2, 3.5)
    fit1.SetParameter(3, 0.0)
    fit1.SetParameter(4, -1.0)
    fit1.FixParameter(4, -1.0)
    # fit1.SetParLimits(4, -1.2, -0.8)
    g_rate_vs_threshold.Fit(fit1)
    fit1.Write()

    c0 = fit1.GetParameter(0)
    c1 = fit1.GetParameter(1)
    c2 = fit1.GetParameter(2)
    c3 = fit1.GetParameter(3)
    c4 = fit1.GetParameter(4)
    print '\nBest-fit parameters for c0*(pT - c1)^(-(c2 + c3*(x - c1)^c4)) are c0 = %.0f, c1 = %.2f, c2 = %.2f, c3 = %.2f, c4 = %.2f\n' % ( c0, c1, c2, c3, c4 )
    for i in range(len(pt_vals)):
        print 'True rate for pT > %2d = %8.2f, predicted = %8.2f, ratio = %.3f' % ( pt_vals[i], true_rates[i], 
                                                                                    c0*pow(pt_vals[i] - c1, -1.*(c2 + c3*pow(pt_vals[i] - c1, c4))),
                                                                                    c0*pow(pt_vals[i] - c1, -1.*(c2 + c3*pow(pt_vals[i] - c1, c4))) / true_rates[i] )

    can1 = TCanvas('c1')
    can1.cd()
    # g_rate_vs_threshold.SetMarkerStyle(8)
    # g_rate_vs_threshold.SetMarkerColor(1)
    # g_rate_vs_threshold.SetMarkerSize(10)
    g_rate_vs_threshold.Draw('AL')
    can1.SetLogy()
    can1.SaveAs('plots/png/rate_vs_threshold_fit1.png')
    

    fit2 = TF1('fit2', '[0]*exp(-1.0*[1]*x)')
    fit2.SetParameter(0, 80000)
    fit2.SetParameter(1, 0.2)
    g_rate_vs_threshold.Fit(fit2)
    fit2.Write()

    d0 = fit2.GetParameter(0)
    d1 = fit2.GetParameter(1)

    print '\nBest-fit parameters for d0*e^(-d1*x) are d0 = %.0f, d1 = %.2f\n' % ( d0, d1 )
    for i in range(len(pt_vals)):
        print 'True rate for pT > %2d = %8.2f, predicted = %8.2f, ratio = %.3f' % ( pt_vals[i], true_rates[i], d0*math.exp(-1.0*d1*pt_vals[i]),
                                                                                    d0*math.exp(-1.0*d1*pt_vals[i]) / true_rates[i] )

    can2 = TCanvas('c2')
    can2.cd()
    g_rate_vs_threshold.Draw('AL')
    can2.SetLogy()
    can2.SaveAs('plots/png/rate_vs_threshold_fit2.png')


    # ## Complex exponential
    # fit3 = TF1('fit3', '[0]*exp(-1.0*[1]*pow(x, [2]))')
    # fit3.SetParameter(0, 80000)
    # fit3.SetParameter(1, 0.2)
    # fit3.SetParameter(2, -1.0)
    # g_rate_vs_threshold.Fit(fit3)
    # fit3.Write()

    # e0 = fit3.GetParameter(0)
    # e1 = fit3.GetParameter(1)
    # e2 = fit3.GetParameter(2)

    # print '\nBest-fit parameters for e0*e^(-e1*(x^e2)) are e0 = %.0f, e1 = %.2f, e2 = %.2f\n' % ( e0, e1, e2 )
    # for i in range(len(pt_vals)):
    #     print 'True rate for pT > %2d = %8.2f, predicted = %8.2f, ratio = %.3f' % ( pt_vals[i], true_rates[i], e0*math.exp(-1.0*e1*pow(pt_vals[i], e2)),
    #                                                                                 e0*math.exp(-1.0*e1*pow(pt_vals[i], e2)) / true_rates[i] )

    # can3 = TCanvas('c3')
    # can3.cd()
    # g_rate_vs_threshold.Draw('AL')
    # can3.SetLogy()
    # can3.SaveAs('plots/png/rate_vs_threshold_fit3.png')



    # ## More complex, pT-dependent fit + exponential
    # fit4 = TF1('fit4', '( [0]*pow(x - [1], -1.*([2] + [3]*pow(x - [1], [4]))) )*(x < 30) + ( [5]*exp(-1.0*[6]*x) )*(x >= 30)')
    # fit4.SetParameter(0, 30000000)
    # fit4.SetParameter(1, 1.0)
    # fit4.SetParameter(2, 3.5)
    # fit4.SetParameter(3, 0.0)
    # fit4.SetParameter(4, -1.0)
    # fit4.FixParameter(4, -1.0)
    # # fit4.SetParLimits(4, -1.2, -0.8)
    # fit4.SetParameter(5, 80000)
    # fit4.SetParameter(6, 0.2)
    # g_rate_vs_threshold.Fit(fit4)
    # fit4.Write()

    # f0 = fit4.GetParameter(0)
    # f1 = fit4.GetParameter(1)
    # f2 = fit4.GetParameter(2)
    # f3 = fit4.GetParameter(3)
    # f4 = fit4.GetParameter(4)
    # f5 = fit4.GetParameter(5)
    # f6 = fit4.GetParameter(6)
    # print '\nBest-fit parameters for f0*(pT - f1)^(-(f2 + f3*(x - f1)^f4)) are f0 = %.0f, f1 = %.2f, f2 = %.2f, f3 = %.2f, f4 = %.2f\n' % ( f0, f1, f2, f3, f4 )
    # print '\nBest-fit parameters for f5*e^(-f6*x) are f5 = %.0f, f6 = %.2f\n' % ( f5, f6 )
    # for i in range(len(pt_vals)):
    #     print 'True rate for pT > %2d = %8.2f, predicted = %8.2f, ratio = %.3f' % ( pt_vals[i], true_rates[i], 
    #                                                                                 f0*pow(pt_vals[i] - f1, -1.*(f2 + f3*pow(pt_vals[i] - c1, f4)))*(pt_vals[i] < 30) +
    #                                                                                 f5*math.exp(-1.0*f6*pt_vals[i])*(pt_vals[i] >= 30),
    #                                                                                 ( f0*pow(pt_vals[i] - f1, -1.*(f2 + f3*pow(pt_vals[i] - c1, f4)))*(pt_vals[i] < 30) +
    #                                                                                   f5*math.exp(-1.0*f6*pt_vals[i])*(pt_vals[i] >= 30) ) / true_rates[i] )

    # can4 = TCanvas('c4')
    # can4.cd()
    # g_rate_vs_threshold.Draw('AL')
    # can4.SetLogy()
    # can4.SaveAs('plots/png/rate_vs_threshold_fit4.png')

    
    ## Get a nice description with the following stitching:
    ## pT < 27: 35 + 28596*(pT - 0.68)^(-1.0*(2.03 - 12.49*(pT - 0.68)^-1.0))
    ## pT > 27: 3124*e^(-0.1*pT)

        

    out_file.Close()

if __name__ == '__main__':
    main()

