import FWCore.ParameterSet.Config as cms

hltFilterToTrackProducer = cms.EDProducer("HLTFilterToTrackProducer", 
                                          filterTag = cms.InputTag("hltL2fL1sMu22or25L1f0L2Filtered10Q")
                                          #trigEvTag = cms.InputTag("hltTriggerSummaryAOD")
                                      )
