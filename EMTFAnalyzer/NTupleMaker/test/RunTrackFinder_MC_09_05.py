
# ## Basic (but usually unnecessary) imports
# import os
# import sys
# import commands

import subprocess

import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('reL1T',eras.Run2_2016)

## Import standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi') ## What does this module do? - AWB 05.09.16
process.load('Configuration.StandardSequences.GeometryRecoDB_cff') ## What does this module do? - AWB 05.09.16
process.load('Configuration.StandardSequences.MagneticField_cff') ## Different than in data ("MagneticField_AutoFromDBCurrent_cff"?)
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullMC_cff') ## Different than in data
process.load('Configuration.StandardSequences.RawToDigi_cff') ## Different than in data ("RawToDigi_Data_cff"?)
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi')

## CSCTF digis, phi / pT LUTs?
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")

## Import RECO muon configurations
process.load("RecoMuon.TrackingTools.MuonServiceProxy_cff")
process.load("RecoMuon.TrackingTools.MuonTrackLoader_cff")

## Message Logger and Event range
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

## Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_v14', '') ## Different than in data ("auto:run2_data"?)

# ## Event Setup Producer
# process.load('L1Trigger.L1TMuonEndCap.fakeEmtfParams_cff') ## Why does this file have "fake" in the name? - AWB 18.04.16
# process.esProd = cms.EDAnalyzer("EventSetupRecordDataGetter",
#                                 toGet = cms.VPSet(
#         ## Apparently L1TMuonEndcapParamsRcd doesn't exist in CondFormats/DataRecord/src/ (Important? - AWB 18.04.16)
#         cms.PSet(record = cms.string('L1TMuonEndcapParamsRcd'),
#                  data = cms.vstring('L1TMuonEndcapParams'))
#         ),
#                                 verbose = cms.untracked.bool(True)
#                                 )

readFiles = cms.untracked.vstring()
process.source = cms.Source(
    'PoolSource',
    fileNames = readFiles
    )

# eos_cmd = '/afs/cern.ch/project/eos/installation/pro/bin/eos.select'

# in_dir_name = '/store/relval/CMSSW_8_0_19/RelValNuGun_UP15/GEN-SIM-DIGI-RECO/PU25ns_80X_mcRun2_asymptotic_2016_TrancheIV_v2_Tr4GT_v2_FastSim-v1/00000/'

# for in_file_name in subprocess.check_output([eos_cmd, 'ls', in_dir_name]).splitlines():
#     if not ('.root' in in_file_name): continue
#     readFiles.extend( cms.untracked.vstring(in_dir_name+in_file_name) )


readFiles.extend([
        'root://eoscms.cern.ch//eos/cms/store/user/wangjian/DsTau3Mu_FullSim_1007/merged_fltr.root'
        ])

process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")


# Path and EndPath definitions

## Defined in Configuration/StandardSequences/python/SimL1EmulatorRepack_FullMC_cff.py
# process.L1RePack_step = cms.Path(process.SimL1Emulator)
SimL1Emulator_AWB = cms.Sequence(process.unpackRPC+process.unpackCSC)
process.L1RePack_step = cms.Path(SimL1Emulator_AWB)

## Defined in Configuration/StandardSequences/python/RawToDigi_cff.py
## Includes L1TRawToDigi, defined in L1Trigger/Configuration/python/L1TRawToDigi_cff.py
# process.raw2digi_step = cms.Path(process.RawToDigi)

# process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi')
# # process.simEmtfDigis.CSCInput = cms.InputTag('simCscTriggerPrimitiveDigis')

process.simCscTriggerPrimitiveDigis.CSCComparatorDigiProducer = cms.InputTag('unpackCSC', 'MuonCSCComparatorDigi' )
process.simCscTriggerPrimitiveDigis.CSCWireDigiProducer       = cms.InputTag( 'unpackCSC', 'MuonCSCWireDigi' )
process.simEmtfDigis.CSCInput = cms.InputTag('simCscTriggerPrimitiveDigis','MPCSORTED')

# process.simEmtfDigis.CSCInput = cms.InputTag('muonCSCDigis', 'MuonCSCCorrelatedLCTDigi')
# process.simEmtfDigis.CSCInputBxShift = cms.untracked.int32(6) ## For muonCSCDigis
# process.simEmtfDigis.RPCInput = cms.InputTag('muonRPCDigis')

# RawToDigi_AWB = cms.Sequence(process.muonCSCDigis+process.muonRPCDigis+process.csctfDigis)
RawToDigi_AWB = cms.Sequence(process.simCscTriggerPrimitiveDigis+process.muonCSCDigis+process.muonRPCDigis+process.csctfDigis+process.simEmtfDigis)
# RawToDigi_AWB = cms.Sequence(process.simMuonCSCDigis+process.cscTriggerPrimitiveDigis+process.muonCSCDigis+process.muonRPCDigis+process.cscTriggerPrimitiveDigis+process.csctfDigis+process.simEmtfDigis)
process.raw2digi_step = cms.Path(RawToDigi_AWB)

## Defined in Configuration/StandardSequences/python/EndOfProcess_cff.py
process.endjob_step = cms.EndPath(process.endOfProcess)

# process.L1TMuonSeq = cms.Sequence(
#     process.muonCSCDigis + ## Unpacked CSC LCTs from TMB
#     process.csctfDigis + ## Necessary for legacy studies, or if you use csctfDigis as input
#     process.muonRPCDigis +
#     ## process.esProd + ## What do we loose by not having this? - AWB 18.04.16
#     process.emtfStage2Digis +
#     process.simEmtfDigis
#     ## process.ntuple
#     )

# process.L1TMuonPath = cms.Path(
#     process.L1TMuonSeq
#     )

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
    'keep *_gmtStage2Digis_*_*',
    'keep *_simGmtStage2Digis_*_*',

    )

process.treeOut = cms.OutputModule("PoolOutputModule", 
                                   # fileName = cms.untracked.string("EMTF_MC_Tree_tau_to_3_mu_pT_0_bug_09_14_debug.root"),
                                   fileName = cms.untracked.string("EMTF_MC_Tree_tau_to_3_mu.root"),
                                   # fileName = cms.untracked.string("EMTF_MC_Tree_RelValNuGun_UP15_1k.root"),
                                   outputCommands = outCommands
                                   )

process.treeOut_step = cms.EndPath(process.treeOut) ## Keep output tree - AWB 08.07.16

# Schedule definition
process.schedule = cms.Schedule(process.L1RePack_step,process.raw2digi_step,process.endjob_step,process.treeOut_step)

# process.output_step = cms.EndPath(process.treeOut)
# process.schedule = cms.Schedule(process.L1TMuonPath)
# process.schedule.extend([process.output_step])

# ## What does this do? Necessary? - AWB 29.04.16
# from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
# process = customise_csc_PostLS1(process)
