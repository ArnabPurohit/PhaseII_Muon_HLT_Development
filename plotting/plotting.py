from tools import algorithmic_efficiency, plot_entries
import dask
from dask.distributed import Client
from functools import partial
import time
import argparse


xaxis_bins = {
    'eta': [-2.4, -2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4],
    'pt': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
}

# Phase 2
#in_path = '/mnt/hadoop/store/user/dkondrat/muonHLT_phase2_DYToLL_test/DYToLL_M-50_TuneCP5_14TeV-pythia8/muonHLT_phase2_DYToLL_test/201210_144844/0000/muonNtuple_phase2_MC_*.root'
# Run 2
in_path = '/mnt/hadoop/store/user/dkondrat/muonHLTtest_DYJets_dkondra_0hitless1hitbased_doublets_test/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/muonHLTtest_DYJets_dkondra_0hitless1hitbased_doublets_test/201209_033033/0000/muonNtuple_test_MC_*'

out_path = '/home/dkondra/muon-hlt-phase2/CMSSW_11_1_2_patch3/src/PhaseII_Muon_HLT_Development/plots/'

x_vars = ['eta', 'pt']

argsets = [
    {
        'reference': 'L2muons',  # L2 muons
        'target': 'muons',       # L3 muons
        'path': in_path,
        'label': 'full HLT',
        'xaxis_opts': x_vars,
        'xaxis_bins': xaxis_bins,
        'match_args': {'dR_cutoff': 0.3},
        'pt_cut': 24
    },
    {
        'reference': 'L2muons',  # L2 muons
        'target': 'hltOImuons',  # L3 muons
        'path': in_path,
        'label': 'only OI',
        'xaxis_opts': x_vars,
        'xaxis_bins': xaxis_bins,
        'match_args': {'dR_cutoff': 0.3},
        'pt_cut': 24
    },
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dask", action='store_true')
    args = parser.parse_args()

    tick = time.time()

    # Get data for efficiency plots
    if args.dask:
        n = 4
        print(f'Using Dask with {n} local workers')
        client = dask.distributed.Client(
            processes=True,
            n_workers=n,
            threads_per_worker=1,
            memory_limit='1GB'
        )
        entries = client.gather(
            client.map(algorithmic_efficiency, argsets)
        )
    else:
        entries = []
        for a in argsets:
            entries.append(algorithmic_efficiency(a, progress_bar=True))

    # Make plots
    plot_entries(
        entries,
        x_vars,
        name_prefix='l3_algo_eff_vs_',  # after this, either 'eta' or 'pt' will be inserted 
        ymin=0.8,
        ymax=1.1,
        out_path=out_path
    )

    tock = time.time()
    print(f'Completed in {tock-tick} s.')
