## 11.02.16: Copied from https://raw.githubusercontent.com/dcurry09/EMTF8/master/L1Trigger/L1TMuonEndCap/test/runMuonEndCap.py

import FWCore.ParameterSet.Config as cms
import os
import sys
import commands
import subprocess
from Configuration.StandardSequences.Eras import eras

process = cms.Process('L1TMuonEmulation')

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
# process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",ignoreTotal = cms.untracked.int32(1))

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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.options = cms.untracked.PSet(
    # SkipEvent = cms.untracked.vstring('ProductNotFound')
)

## Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '') ## Good for 2015/2016 data/MC? - AWB 18.04.16
# process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '') ## Used for anything? - AWB 18.04.16

## Event Setup Producer
process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_cff') ## Why does this file have "fake" in the name? - AWB 18.04.16
process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
                                toGet = cms.VPSet(
        ## Apparently L1TMuonEndcapParamsRcd doesn't exist in CondFormats/DataRecord/src/ (Important? - AWB 18.04.16)
        cms.PSet(record = cms.string('L1TMuonEndcapParamsRcd'),
                 data = cms.vstring('L1TMuonEndcapParams'))
        ),
                                verbose = cms.untracked.bool(True)
                                )


readFiles = cms.untracked.vstring()
secFiles  = cms.untracked.vstring()
process.source = cms.Source(
    'PoolSource',
    fileNames = readFiles,
    secondaryFileNames= secFiles
    #, eventsToProcess = cms.untracked.VEventRange('201196:265380261')
    )

## Last run in CMSSW < 8_0_9 (CMSSW_8_0_8_patch2) is 274443
## First run with fixed unpacked EMTF input hits is 276215, corresponding to RAW_RECO_756.root in 2016C_v2/160710_225057/0000/

# in_dir_name = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Run2016B/Trees/ZMu_200_RAW-RECO_B/'
# for in_file_name in os.listdir(in_dir_name):
#     if not '.root' in in_file_name: continue
#     # if not 'highPt200MuonSkim_RAW_RECO_1' in in_file_name and not 'highPt200MuonSkim_RAW_RECO_2' in in_file_name:
#     readFiles.extend( cms.untracked.vstring('file:'+in_dir_name+in_file_name) )

eos_cmd = '/afs/cern.ch/project/eos/installation/pro/bin/eos.select'
in_dir_name = '/store/group/dpg_trigger/comm_trigger/L1Trigger/Data/Collisions/SingleMuon/Skims/200-pt-muon-skim_from-zmumu-skim-cmssw-8013/SingleMuon/'
# in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016B_v1/160710_225040/0000/'
# in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016B_v2/160710_225006/0000/'
# in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016C_v2/160710_225057/0000/'
in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016C_v2/160710_225057/0001/'
# in_dir_name = in_dir_name+'crab_200-pt-muon-skim_from-zmumu-skim-cmssw-8013__SingleMuon_ZMu-2016D_v2/160710_225023/0000/'
for in_file_name in subprocess.check_output([eos_cmd, 'ls', in_dir_name]).splitlines():
    if not ('.root' in in_file_name): continue
    # if not ('0.root' in in_file_name or '1.root' in in_file_name or '2.root' in in_file_name or '3.root' in in_file_name): continue
    # if not ('4.root' in in_file_name or '5.root' in in_file_name or '6.root' in in_file_name): continue
    # if not ('7.root' in in_file_name or '8.root' in in_file_name or '9.root' in in_file_name): continue
    # if ( int(in_file_name.split('RECO_')[1].split('.roo')[0]) < 755 ): continue
    readFiles.extend( cms.untracked.vstring(in_dir_name+in_file_name) )

# readFiles.extend([

#         # ## file run=276282 dataset=/DoubleMuon/Run2016C-v2/RAW
#         # 'root://cms-xrd-global.cern.ch//store/data/Run2016C/DoubleMuon/RAW/v2/000/276/282/00000/12F0BEEC-5541-E611-8A6C-02163E0141D7.root',

#         # 'root://eoscms.cern.ch//eos/cms/store/data/Run2016B/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/274/442/00000/18C0720A-D62D-E611-BD56-02163E0134DB.root',

#         # '/store/data/Run2016B/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/274/442/00000/4298EB7A-EA2D-E611-B7D3-02163E0136B5.root',

#         # 'root://eoscms.cern.ch//eos/cms/store/data/Run2016B/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/274/442/00000/501B475E-E32D-E611-8412-02163E0144D7.root',

#        ])

# secFiles.extend([
#         'root://eoscms.cern.ch//eoscms//eos/cms/store/data/Run2015B/SingleMuon/RAW/v1/000/251/168/00000/382EE8DB-2825-E511-B3E0-02163E013597.root'
#         ])


process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

# ## EMTF Emulator
process.load('EventFilter.L1TRawToDigi.emtfStage2Digis_cfi')
process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi') 
process.simEmtfDigis.CSCInput = cms.InputTag('emtfStage2Digis') ## Can also use ('csctfDigis') or ('simCscTriggerPrimitiveDigis', 'MPCSORTED')
## process.simEmtfDigis.CSCInput = cms.InputTag('csctfDigis') 
process.simEmtfDigis.CSCInputBxShift = cms.untracked.int32(0)
process.simEmtfDigis.RPCInput = cms.InputTag('muonRPCDigis') ## Can also use ('csctfDigis') or ('simCscTriggerPrimitiveDigis', 'MPCSORTED')

## NTuplizer
process.ntuple = cms.EDAnalyzer('NTupleMaker',
                                muonsTag     = cms.InputTag("muons"),               ## RECO muons
                                vertexTag    = cms.InputTag("offlinePrimaryVertices"), ## Primary vertices (for muon quality)
                                genTag       = cms.InputTag("genParticles"),        ## GEN muons
                                cscSegTag    = cms.InputTag("cscSegments"),         ## RECO CSC segments
                                ## rpcClustTag  = cms.InputTag("muonRPCDigis"),        ## Use these (or RecHits?) like CSC segments
                                csctfTag     = cms.InputTag("csctfDigis"),          ## CSCTF output tracks
                                cscTPTag     = cms.InputTag("csctfDigis"),          ## CSCTF input LCTs
                                emtfTag      = cms.InputTag("simEmtfDigis", ""),    ## EMTF emulator output tracks
                                emtfTPTag    = cms.InputTag("simEmtfDigis", "CSC"), ## EMTF input LCTs
                                emtfTPTagRPC = cms.InputTag("simEmtfDigis", "RPC"), ## EMTF input RPC clusters
                                unp_emtfTag  = cms.InputTag("emtfStage2Digis"),     ## Unpacked EMTF output tracks
                                ## leg_gmtTag   = cms.InputTag("gtDigis"),             ## Legacy GMT tracks (2015 only)
                                isMC         = cms.untracked.int32(0),
                                NoTagAndProbe= cms.untracked.bool(True),
                                printLevel   = cms.untracked.int32(0), 
                                outputDIR   = cms.string('')
                                )

process.L1TMuonSeq = cms.Sequence(
    process.csctfDigis + ## Necessary for legacy studies, or if you use csctfDigis as input
    process.muonRPCDigis +
    ## process.esProd + ## What do we loose by not having this? - AWB 18.04.16
    process.emtfStage2Digis +
    process.simEmtfDigis +
    process.ntuple
    )

process.L1TMuonPath = cms.Path(
    process.L1TMuonSeq
    )

## Output File
process.TFileService = cms.Service(
    "TFileService",
    # fileName = cms.string("EMTF_NTuple_ZMu_274442_emtfStage2Digis_1k.root")
    # fileName = cms.string("EMTF_NTuple_ZMu_275375_emtfStage2Digis_1k.root")
    # fileName = cms.string("EMTF_NTuple_ZMu_276092_emtfStage2Digis_debug.root")
    # fileName = cms.string("EMTF_NTuple_ZMu_276282_emtfStage2Digis_debug.root")
    fileName = cms.string("EMTF_NTuple_highPt200MuonSkim_emtfStage2Digis_post_276215_outlierFix2_2016C_v2_02.root")
    )

# outCommands = cms.untracked.vstring('keep *')
outCommands = cms.untracked.vstring(

    'keep recoMuons_muons__*',
    'keep *_csctfDigis_*_*',
    'keep *_emtfStage2Digis_*_*',
    'keep *_simEmtfDigis_*_*',
    'keep *_gmtStage2Digis_*_*',
    'keep *_simGmtStage2Digis_*_*',

    )


process.out = cms.OutputModule("PoolOutputModule", 
                               # fileName = cms.untracked.string("EMTF_Tree_ZMu_274442_emtfStage2Digis_1k.root"),
                               # fileName = cms.untracked.string("EMTF_Tree_ZMu_275375_emtfStage2Digis_1k.root"),
                               # fileName = cms.untracked.string("EMTF_Tree_ZMu_276092_emtfStage2Digis_debug.root"),
                               # fileName = cms.untracked.string("EMTF_Tree_ZMu_276282_emtfStage2Digis_debug.root"),
                               fileName = cms.untracked.string("EMTF_Tree_highPt200MuonSkim_emtfStage2Digis_post_276215_outlierFix2_2016C_v2_02.root"),
                               outputCommands = outCommands
                               )

process.output_step = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.L1TMuonPath)

process.schedule.extend([process.output_step])

## What does this do? Necessary? - AWB 29.04.16
from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
process = customise_csc_PostLS1(process)
