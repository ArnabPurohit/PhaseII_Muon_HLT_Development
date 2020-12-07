# Instruction for Phase-II IterativeL3 (from Federica)
```
cmsrel CMSSW_11_1_2_patch3
cd CMSSW_11_1_2_patch3/src
cmsenv
git cms-addpkg SimMuon/MCTruth
git cms-addpkg Validation/RecoMuon
git clone -b IterL3 https://github.com/kondratyevd/PhaseII_Muon_HLT_Development
scram b -j 10
#Change input file and output dir in step3_HLT_muons_TRK_v6_1.py
cmsRun step3_HLT_muons_TRK_v6_1.py
```
