# Instruction for L1TKMuonIOL3 (from Minseok)\
cmsrel CMSSW_11_1_4\
cd CMSSW_11_1_4/src\
cmsenv  
git cms-init\
git cms-merge-topic trtomei:Phase2-L1T-HLT-Interface\
scram b -j 10  
cd your-working-directory\
git clone https://github.com/ArnabPurohit/PhaseII_Muon_HLT_Development.git  
cp /afs/cern.ch/user/t/tomei/public/L1TObjScaling.db your-working-directory\
cd PhaseII_Muon_HLT_Development/example_cfgs\
cmsRun HLT_Phase2_L3MuonFromL1TkMuon.py\

# Instruction for Phase-II IterativeL3 (from Federica)\
cmsrel CMSSW_11_1_2_patch3\
cd CMSSW_11_1_2_patch3/src\
git clone https://github.com/ArnabPurohit/PhaseII_Muon_HLT_Development.git\
scram b -j 10\
Change input file and output dir in step3_HLT_muons_TRK_v6_1.py\
cmsRun step3_HLT_muons_TRK_v6_1.py\
