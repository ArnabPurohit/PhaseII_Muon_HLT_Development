import sys


from CRABClient.UserUtilities import config

config = config()

config.JobType.pluginName   = 'Analysis'
config.JobType.outputFiles  = ['muonNtuple_phase2_MC.root']

config.Data.unitsPerJob     = 10
config.Data.totalUnits      = 1000

config.Data.splitting       = 'EventAwareLumiBased'

config.Data.useParent       = True #!!!!
#config.Data.useParent       = False #!!!!

config.Site.storageSite     = 'T2_US_Purdue'
config.JobType.numCores     = 1
config.JobType.maxMemoryMB  = 2500
config.JobType.allowUndistributedCMSSW = True
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

tag = "muonHLT_phase2_DYToLL_test"

config.General.workArea   = tag
config.Data.outLFNDirBase = '/store/user/dkondrat/' + tag

config.JobType.psetName    = 'cfgs/step3_HLT_muons_TRK_v6_1.py'
config.General.requestName = tag
config.General.transferLogs = True

#config.Data.inputDataset = '/DYToLL_M-50_TuneCP5_14TeV-pythia8/PhaseIITDRSpring19DR-PU140_pilot_106X_upgrade2023_realistic_v3-v1/AODSIM'
config.Data.inputDataset = '/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRWinter20RECOMiniAOD-PU140_pilot_110X_mcRun4_realistic_v3-v2/MINIAODSIM'

#config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'

config.Data.outputDatasetTag   = tag

