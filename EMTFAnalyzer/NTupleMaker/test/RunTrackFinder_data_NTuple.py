## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands
import subprocess
from Configuration.StandardSequences.Eras import eras

process = cms.Process('L1TMuonEmulation')

# ## Verbose printouts of plugins
# process.add_(cms.Service("PrintLoadingPlugins"))

## Import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff') ## Is this appropriate for 2015 data/MC? - AWB 18.04.16
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff') ## Will this work on 0T data? - AWB 18.04.16
process.load('Configuration.StandardSequences.RawToDigi_Data_cff') ## Will this work for MC? - AWB 18.04.16
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# ## Extra tools
# process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
#                                         ignoreTotal = cms.untracked.int32(1),
#                                         monitorPssAndPrivate = cms.untracked.bool(True))
# process.Tracer = cms.Service("Tracer")

## CSCTF digis, phi / pT LUTs?
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")

## Import RECO muon configurations
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

## Lumi JSON tools
import FWCore.PythonUtilities.LumiList as LumiList
# process.source.lumisToProcess = LumiList.LumiList(filename = 'goodList.json').getVLuminosityBlockRange()

## Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.options = cms.untracked.PSet(
    # SkipEvent = cms.untracked.vstring('ProductNotFound')
)

## Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

## Default parameters for firmware version, pT LUT XMLs, and coordinate conversion LUTs
process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_cff') 
# process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_2017_data_cff') 
# process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_2016_data_cff') 

# ## Un-comment out this line to choose the GlobalTag settings rather than fakeEmtfParams settings
# ## Comment out this line to use default FW version rather than true FW version in data
process.es_prefer_GlobalTag = cms.ESPrefer("PoolDBESSource","GlobalTag")
# process.es_prefer_GlobalTag = cms.ESPrefer("PoolDBESSource","emtfParamsSource")


readFiles = cms.untracked.vstring()
secFiles  = cms.untracked.vstring()
process.source = cms.Source(
    'PoolSource',
    fileNames = readFiles,
    secondaryFileNames= secFiles
    #, eventsToProcess = cms.untracked.VEventRange('201196:265380261')
    )

eos_cmd = '/afs/cern.ch/project/eos/installation/ams/bin/eos.select'

## 2017 Collisions, with RPC!
# in_dir_name = '/eos/cms/tier0/store/data/Commissioning2017/L1Accept/RAW/v1/000/293/765/00000/'
# in_dir_name = '/eos/cms/tier0/store/data/Commissioning2017/MinimumBias/RAW/v1/000/293/765/00000/'
# in_dir_name = '/eos/cms/tier0/store/data/Run2017E/DoubleMuon/RAW/v1/000/303/832/00000/'
in_dir_name = '/store/data/Run2017F/SingleMuon/RAW-RECO/ZMu-PromptReco-v1/000/306/091/00000/'

# ## 2017 Cosmics, with RPC!
# in_dir_name = '/store/express/Commissioning2017/ExpressCosmics/FEVT/Express-v1/000/291/622/ 00000/'

# ## ZeroBias, IsolatedBunch data
# in_dir_name = '/store/data/Run2016H/ZeroBiasIsolatedBunch0/RAW/v1/000/282/650/00000/'

# ## SingleMu, Z-->mumu, high pT RECO muon
# in_dir_name = '/store/group/dpg_trigger/comm_trigger/L1Trigger/Data/Collisions/SingleMuon/Skims/200-pt-muon-skim_from-zmumu-skim-cmssw-8013/SingleMuon/'
# in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016B_v1/160710_225040/0000/'
# # in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016B_v2/160710_225006/0000/'
# # in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016C_v2/160710_225057/0000/'
# # in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016C_v2/160710_225057/0001/'
# # in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016D_v2/160710_225023/0000/'

# ## 2017 High-pileup run
# # in_dir_name = '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/'
# in_dir_name = ''

# fileList = [
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/329677A9-6C98-E711-A7B5-02163E01A686.root',
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/34097DB1-6C98-E711-841E-02163E01A6B3.root',
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/385BC298-6C98-E711-9D91-02163E01442C.root',
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/386668AB-6C98-E711-A865-02163E01A20D.root',
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/3A33B6A7-6C98-E711-A159-02163E01A271.root',
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/3E5476AE-6C98-E711-A5EF-02163E011E8C.root',
#     '/store/data/Run2017D/ZeroBiasNominalTrains1/RAW/v1/000/302/674/00000/3EDDDAB1-6C98-E711-9502-02163E01A466.root'
# ]


# # fileList = [
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/306470C1-6C98-E711-8385-02163E019DB9.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/30728BA2-6C98-E711-B322-02163E01A1F3.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/32BACB9F-6C98-E711-B0F8-02163E01A1E4.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/346FD994-6C98-E711-BC0A-02163E014793.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/34ACDAEC-6C98-E711-98F1-02163E012B11.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/36B33EB2-6C98-E711-A8A2-02163E01A2C0.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/36CFD1A3-6C98-E711-BB81-02163E01A710.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/3C9236A8-6C98-E711-8C83-02163E01A2E0.root',
# #     '/store/data/Run2017D/ZeroBiasIsolatedBunches4/RAW/v1/000/302/674/00000/3E755C98-6C98-E711-ABFB-02163E011CF7.root'
# # ]

# # fileList = [
#     # # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/2025A51D-6C98-E711-9701-02163E01A543.root',
#     # # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/227B2527-6C98-E711-9AED-02163E019C71.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/2492C004-6C98-E711-979D-02163E0123C3.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/24E0902C-6C98-E711-BA1F-02163E01459E.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/262A8113-6C98-E711-B9AE-02163E019BBF.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/2659AB1E-6C98-E711-9651-02163E01A1EA.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/28E8541B-6C98-E711-80D7-02163E019E82.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/2C81DF11-6C98-E711-B67E-02163E01459E.root',
#     # '/store/data/Run2017D/ZeroBiasIsolatedBunches1/RAW/v1/000/302/674/00000/2CAAAB2B-6C98-E711-912C-02163E01A61A.root'
#     # ]


iFile = 0
for in_file_name in subprocess.check_output([eos_cmd, 'ls', in_dir_name]).splitlines():
# for in_file_name in fileList:
    if not ('.root' in in_file_name): continue
    iFile += 1
    # if iFile < 10: continue  ## Skip earliest files in run
    if iFile > 31: break
    print in_file_name
    readFiles.extend( cms.untracked.vstring(in_dir_name+in_file_name) )
    # in_dir_name_T0 = in_dir_name.replace('/eos/cms/tier0/', 'root://cms-xrd-tzero.cern.ch//')
    # readFiles.extend( cms.untracked.vstring(in_dir_name_T0+in_file_name) )

# readFiles.extend([
#         #'file:/afs/cern.ch/work/a/abrinke1/public/EMTF/Run2016G/RAW/279024/52622B4D-B265-E611-8099-FA163E326094.root'
#         'root://eoscms.cern.ch//eos/cms/store/user/abrinke1/EMTF/Run2017B/HLTPhysics/298034/52F73C59-4E61-E711-AACA-02163E01A505.root'
#         ])

# secFiles.extend([
#         'root://eoscms.cern.ch//eoscms//eos/cms/store/data/Run2015B/SingleMuon/RAW/v1/000/251/168/00000/382EE8DB-2825-E511-B3E0-02163E013597.root'
#         ])


process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

## Re-emulate CSC LCTs to get full ALCT+CLCT info
process.load('L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi')
process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = cms.InputTag('muonCSCDigis', 'MuonCSCComparatorDigi')
process.cscTriggerPrimitiveDigis.CSCWireDigiProducer       = cms.InputTag('muonCSCDigis', 'MuonCSCWireDigi')
process.cscTriggerPrimitiveDigis.commonParam = cms.PSet(
    isTMB07 = cms.bool(True), ## Default
    isMTCC = cms.bool(False), ## Default
    isSLHC = cms.bool(False), ## Default
    smartME1aME1b = cms.bool(False), ## Default
    gangedME1a = cms.bool(False), ## Changed - why is this not default?
    disableME1a = cms.bool(False), ## Default
    disableME42 = cms.bool(False), ## Default
)

## EMTF Emulator
process.load('EventFilter.L1TRawToDigi.emtfStage2Digis_cfi')
process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi')

process.simEmtfDigis.verbosity = cms.untracked.int32(0)
# process.simEmtfDigis.CSCInput  = cms.InputTag('emtfStage2Digis')
process.simEmtfDigis.CSCInput  = cms.InputTag('cscTriggerPrimitiveDigis','MPCSORTED') ## Re-emulated CSC LCTs
process.simEmtfDigis.CSCInputBXShift = cms.int32(-8) ## Only for re-emulated CSC LCTs (vs. -6 default)
process.simEmtfDigis.RPCInput  = cms.InputTag('muonRPCDigis')


##############################################
###  Settings for 2016 vs. 2017 emulation  ###
##############################################

# ## *** 2016 ***
# ## From python/fakeEmtfParams_cff.py
# process.emtfParams.PtAssignVersion = cms.int32(5)
# process.emtfParams.FirmwareVersion = cms.int32(49999) ## Settings as of end-of-year 2016
# process.emtfParams.PrimConvVersion = cms.int32(0)
# process.emtfForestsDB.toGet = cms.VPSet(
#     cms.PSet(
#         record = cms.string("L1TMuonEndCapForestRcd"),
#         tag = cms.string("L1TMuonEndCapForest_static_2016_mc")
#         )
#     )

# ## From python/simEmtfDigis_cfi.py
# process.simEmtfDigis.RPCEnable                 = cms.bool(False)
# process.simEmtfDigis.spTBParams16.ThetaWindow  = cms.int32(4)
# process.simEmtfDigis.spPCParams16.FixME11Edges = cms.bool(False)
# process.simEmtfDigis.spPAParams16.PtLUTVersion = cms.int32(5)
# process.simEmtfDigis.spPAParams16.BugGMTPhi    = cms.bool(True)


# ## *** 2017 ***
# ## From python/fakeEmtfParams_cff.py
# process.emtfParams.PtAssignVersion = cms.int32(7)
# process.emtfParams.FirmwareVersion = cms.int32(50001) ## Settings as of beginning-of-year 2017
# process.emtfParams.PrimConvVersion = cms.int32(1)
# # process.emtfForestsDB.toGet = cms.VPSet(
# #     cms.PSet(
# #         record = cms.string("L1TMuonEndCapForestRcd"),
# #         tag = cms.string("L1TMuonEndCapForest_static_Sq_20170523_mc")
# #         )
# #     )

# ## From python/simEmtfDigis_cfi.py
# process.simEmtfDigis.RPCEnable                  = cms.bool(True)
# process.simEmtfDigis.spTBParams16.ThetaWindow   = cms.int32(8)
# process.simEmtfDigis.spPCParams16.FixME11Edges  = cms.bool(True)
# process.simEmtfDigis.spPAParams16.PtLUTVersion  = cms.int32(7)
# process.simEmtfDigis.spPAParams16.BugGMTPhi     = cms.bool(False)
# process.simEmtfDigis.spPAParams16.ReadPtLUTFile = cms.bool(False)

process.simEmtfDigis.RPCEnable = cms.bool(True)

# # process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,36,54,96,127) ## v1
# # process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,36,55,94,127) ## v2
# # process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,38,47,90,127) ## v3
# # process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,35,51,97,127) ## v4
# process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,37,48,93,127) ## v5
# process.simEmtfDigis.spPCParams16.UseNewZones    = cms.bool(True)
# process.simEmtfDigis.spPCParams16.ZoneOverlap    = cms.int32(6)
# process.simEmtfDigis.spPCParams16.ZoneOverlapRPC = cms.int32(6)

# process.simEmtfDigis.spPRParams16.SymPatternDefinitions = cms.vstring(
#     # straightness, hits in ME1, hits in ME2, hits in ME3, hits in ME4
#     # ME1 vaues centered at 15, range from 0 - 30
#     # ME2,3,4 values centered at 7, range from 0 - 14
#     "4,15:15:15:15,7:7:7:7,8:7:7:6,8:7:7:6",    ## Widened ME3,4 by one unit in each direction
#     "3,16:16:14:14,7:7:7:7,8:7:7:6,8:7:7:6",    ## Unchanged
#     "2,18:17:13:12,7:7:7:7,10:7:7:4,10:7:7:4",  ## Unchanged
#     "1,22:19:11:8,7:7:7:7,10:7:7:4,10:7:7:4",   ## Narrowed ME3,4 by four units from each direction
#     "0,30:23:7:0,7:7:7:7,14:7:7:0,14:7:7:0",    ## Unchanged
#     )

# ## "v2"
# process.simEmtfDigis.spPRParams16.SymPatternDefinitions = cms.vstring(
#     # straightness, hits in ME1, hits in ME2, hits in ME3, hits in ME4
#     # ME1 vaues centered at 15, range from 0 - 30
#     # ME2,3,4 values centered at 7, range from 0 - 14
#     "6,15:15:15:15,7:7:7:7,8:7:7:6,8:7:7:6",    ## Widened ME3,4 by one unit in each direction
#     "4,16:16:14:14,7:7:7:7,8:7:7:6,8:7:7:6",    ## Unchanged
#     "3,18:17:13:12,7:7:7:7,8:7:7:6,8:7:7:6",    ## Narrowed ME3,4 by two units from each direction
#     "2,22:19:11:8,7:7:7:7,10:7:7:4,10:7:7:4",   ## Narrowed ME3,4 by four units from each direction
#     "0,30:23:7:0,7:7:7:7,14:7:7:0,14:7:7:0",    ## Unchanged
#     )

# ## "v3" (re-narrowed straightest pattern, changed straightness codes w.r.t. v2)
# process.simEmtfDigis.spPRParams16.SymPatternDefinitions = cms.vstring(
#     # straightness, hits in ME1, hits in ME2, hits in ME3, hits in ME4
#     # ME1 vaues centered at 15, range from 0 - 30
#     # ME2,3,4 values centered at 7, range from 0 - 14
#     "5,15:15:15:15,7:7:7:7,7:7:7:7,7:7:7:7",    ## Unchanged
#     "4,16:16:14:14,7:7:7:7,8:7:7:6,8:7:7:6",    ## Unchanged
#     "2,18:17:13:12,7:7:7:7,8:7:7:6,8:7:7:6",    ## Narrowed ME3,4 by two units from each direction
#     "1,22:19:11:8,7:7:7:7,10:7:7:4,10:7:7:4",   ## Narrowed ME3,4 by four units from each direction
#     "0,30:23:7:0,7:7:7:7,14:7:7:0,14:7:7:0",    ## Unchanged
#     )



###################
###  NTuplizer  ###
###################

process.load('EMTFAnalyzer.NTupleMaker.FlatNtuple_cfi')
# process.FlatNtupleData.emtfHitTag = cms.InputTag("simEmtfDigis")

RawToDigi_AWB = cms.Sequence(
    process.muonRPCDigis             + ## Unpacked RPC hits from RPC PAC
    process.muonCSCDigis             + ## Unpacked CSC LCTs (and raw strip and wire?) from TMB
    process.cscTriggerPrimitiveDigis + ## To get re-emulated CSC LCTs
    # process.csctfDigis               + ## Necessary for legacy studies, or if you use csctfDigis as input
    process.emtfStage2Digis          + 
    process.simEmtfDigis             + 
    process.FlatNtupleData
    )

process.raw2digi_step = cms.Path(RawToDigi_AWB)

## Defined in Configuration/StandardSequences/python/EndOfProcess_cff.py
process.endjob_step = cms.EndPath(process.endOfProcess)


# out_dir_name = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/'
out_dir_name = './'

## NTuple output File
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(out_dir_name+'EMTF_ZMu_NTuple_306091_simLCT_test.root')
    )


# outCommands = cms.untracked.vstring('keep *')
outCommands = cms.untracked.vstring(

    'keep recoMuons_muons__*',
    'keep *Gen*_*_*_*',
    'keep *_*Gen*_*_*',
    'keep *gen*_*_*_*',
    'keep *_*gen*_*_*',
    'keep CSCDetIdCSCCorrelatedLCTDigiMuonDigiCollection_*_*_*', ## muonCSCDigis
    'keep RPCDetIdRPCDigiMuonDigiCollection_*_*_*', ## muonRPCDigis
    #'keep CSCCorrelatedLCTDigiCollection_muonCSCDigis_*_*',
    #'keep *_*_*muonCSCDigis*_*',
    #'keep *_*_*_*muonCSCDigis*',
    'keep *_csctfDigis_*_*',
    'keep *_emtfStage2Digis_*_*',
    'keep *_simEmtfDigis_*_*',
    'keep *_simEmtfDigisMC_*_*',
    'keep *_gmtStage2Digis_*_*',
    'keep *_simGmtStage2Digis_*_*',

    )

# process.treeOut = cms.OutputModule("PoolOutputModule", 
#                                    # fileName = cms.untracked.string("EMTF_MC_Tree_RelValNuGun_UP15_1k.root"),
#                                    # fileName = cms.untracked.string("EMTF_MC_Tree_tau_to_3_mu_RPC_debug.root"),
#                                    fileName = cms.untracked.string(out_dir_name+'EMTF_MC_Tree_SingleMu_noRPC_300k.root'),
#                                    outputCommands = outCommands
#                                    )

# process.treeOut_step = cms.EndPath(process.treeOut) ## Keep output tree - AWB 08.07.16

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step)
# process.schedule = cms.Schedule(process.L1RePack_step,process.raw2digi_step,process.endjob_step,process.treeOut_step)

# process.output_step = cms.EndPath(process.treeOut)
# process.schedule = cms.Schedule(process.L1TMuonPath)
# process.schedule.extend([process.output_step])

# ## What does this do? Necessary? - AWB 29.04.16
# from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
# process = customise_csc_PostLS1(process)
