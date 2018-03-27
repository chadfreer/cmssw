
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
# process.load('SimGeneral.MixingModule.mixNoPU_cfi') ## What does this module do? - AWB 05.09.16
process.load('Configuration.StandardSequences.GeometryRecoDB_cff') ## What does this module do? - AWB 05.09.16
process.load('Configuration.StandardSequences.MagneticField_cff') ## Different than in data ("MagneticField_AutoFromDBCurrent_cff"?)
# process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullMC_cff') ## Different than in data
process.load('Configuration.StandardSequences.RawToDigi_Data_cff') ## Different than in MC ("RawToDigi_cff"?)
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
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

## Global Tags
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '') ## Different than in MC ("80X_mcRun2_asymptotic_v14")?


readFiles = cms.untracked.vstring()
process.source = cms.Source(
    'PoolSource',
    fileNames = readFiles
    )

eos_cmd = '/afs/cern.ch/project/eos/installation/pro/bin/eos.select'

in_dir_name = '/store/data/Run2016H/ZeroBiasIsolatedBunch0/RAW/v1/000/282/650/00000/'

out_dir_name = '/afs/cern.ch/work/a/abrinke1/public/EMTF/Analyzer/ntuples/'

for in_file_name in subprocess.check_output([eos_cmd, 'ls', in_dir_name]).splitlines():
    if not ('.root' in in_file_name): continue
    readFiles.extend( cms.untracked.vstring(in_dir_name+in_file_name) )


process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpED = cms.EDAnalyzer("EventContentAnalyzer")
process.dumpES = cms.EDAnalyzer("PrintEventSetupContent")

# Path and EndPath definitions

# L1Unpacker_AWB = cms.Sequence(process.unpackRPC)
# process.L1Unpack_step = cms.Path(L1Unpacker_AWB)

## Defined in Configuration/StandardSequences/python/RawToDigi_cff.py
## Includes L1TRawToDigi, defined in L1Trigger/Configuration/python/L1TRawToDigi_cff.py
# process.raw2digi_step = cms.Path(process.RawToDigi)

process.load('L1Trigger.L1TMuonEndCap.simEmtfDigis_cfi')

process.simEmtfDigis.MinBX = cms.int32(-3)
process.simEmtfDigis.MaxBX = cms.int32(+3)

process.simEmtfDigis.spPCParams16.FixZonePhi     = cms.bool(True)
process.simEmtfDigis.spPCParams16.UseNewZones    = cms.bool(True)
#process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,41,49,87,127)
process.simEmtfDigis.spPCParams16.ZoneBoundaries = cms.vint32(0,36,54,96,127)

process.simEmtfDigis.spPRParams16.UseSymmetricalPatterns = cms.bool(True)

process.simEmtfDigis.spGCParams16.UseSecondEarliest = cms.bool(True)

process.simEmtfDigis.spPAParams16.FixMode15HighPt = cms.bool(True)
process.simEmtfDigis.spPAParams16.Bug9BitDPhi     = cms.bool(False)
process.simEmtfDigis.spPAParams16.BugMode7CLCT    = cms.bool(False)
process.simEmtfDigis.spPAParams16.BugNegPt        = cms.bool(False)

process.simEmtfDigis.CSCInput        = cms.InputTag('emtfStage2Digis')
process.simEmtfDigis.RPCInput        = cms.InputTag('muonRPCDigis')
process.simEmtfDigis.CSCEnable       = cms.bool(True)
process.simEmtfDigis.RPCEnable       = cms.bool(False)
process.simEmtfDigis.CSCInputBXShift = cms.int32(-6)
process.simEmtfDigis.RPCInputBXShift = cms.int32(0)
process.simEmtfDigis.verbosity       = cms.untracked.int32(0)

## NTuplizer
process.ntuple = cms.EDAnalyzer('PtLutInput',
                                isMC          = cms.bool(False),
                                genMuonTag    = cms.InputTag(""),                     ## No GEN muons
                                emtfHitTag    = cms.InputTag("simEmtfDigis"),  ## EMTF input LCTs
                                emtfTrackTag  = cms.InputTag("simEmtfDigis"),  ## EMTF emulator output tracks
                                )


RawToDigi_AWB = cms.Sequence(process.muonRPCDigis+process.emtfStage2Digis+process.simEmtfDigis+process.ntuple)
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


## NTuple output File
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string('EMTF_data_NTuple_ZeroBiasIsolatedBunch_noRPC_10k.root')
    # fileName = cms.string(out_dir_name+'EMTF_data_NTuple_ZeroBiasIsolatedBunch_noRPC_1k.root')
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
#                                    fileName = cms.untracked.string(out_dir_name+'EMTF_data_Tree_ZeroBiasIsolatedBunch_noRPC_1k.root'),
#                                    outputCommands = outCommands
#                                    )

# process.treeOut_step = cms.EndPath(process.treeOut) ## Keep output tree - AWB 08.07.16

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step)
# process.schedule = cms.Schedule(process.L1Unpack_step,process.raw2digi_step,process.endjob_step,process.treeOut_step)

# process.output_step = cms.EndPath(process.treeOut)
# process.schedule = cms.Schedule(process.L1TMuonPath)
# process.schedule.extend([process.output_step])

# ## What does this do? Necessary? - AWB 29.04.16
# from SLHCUpgradeSimulations.Configuration.muonCustoms import customise_csc_PostLS1
# process = customise_csc_PostLS1(process)
