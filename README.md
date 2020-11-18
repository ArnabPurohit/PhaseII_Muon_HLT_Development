cmsrel CMSSW_11_1_4
cd CMSSW_11_1_4/src
cmsenv

git cms-init
git cms-merge-topic trtomei:Phase2-L1T-HLT-Interface

scram b -j 10


cd your-working-directory
git clone https://github.com/ArnabPurohit/PhaseII_Muon_HLT_Development.git
cp /afs/cern.ch/user/t/tomei/public/L1TObjScaling.db your-working-directory
cd PhaseII_Muon_HLT_Development/example_cfgs
cmsRun HLT_Phase2_L3MuonFromL1TkMuon.py
