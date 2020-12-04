# Instruction for Phase-II IterativeL3 (from Federica)
cmsrel CMSSW_11_1_2_patch3\
cd CMSSW_11_1_2_patch3/src\
git clone -b IterL3 https://github.com/ArnabPurohit/PhaseII_Muon_HLT_Development.git\
scram b -j 10\
#Change input file and output dir in step3_HLT_muons_TRK_v6_1.py\
cmsRun step3_HLT_muons_TRK_v6_1.py