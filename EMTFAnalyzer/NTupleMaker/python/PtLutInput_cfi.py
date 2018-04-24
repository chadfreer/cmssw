import FWCore.ParameterSet.Config as cms

PtLutInputMC = cms.EDAnalyzer('PtLutInput',
                              isMC          = cms.bool(True),
                              genMuonTag    = cms.InputTag("genParticles"),
                              emtfHitTag    = cms.InputTag("simEmtfDigisMC"),
                              emtfTrackTag  = cms.InputTag("simEmtfDigisMC"),
                              )

PtLutInputData = cms.EDAnalyzer('PtLutInput',
                                isMC          = cms.bool(False),
                                genMuonTag    = cms.InputTag(""),
                                emtfHitTag    = cms.InputTag("simEmtfDigisData"),
                                emtfTrackTag  = cms.InputTag("simEmtfDigisData"),
                                )

