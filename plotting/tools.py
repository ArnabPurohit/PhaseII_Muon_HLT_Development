import os, sys
import glob
import uproot4 as uproot
import awkward1 as ak
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from tqdm import tqdm

from utils import MuCollection, match, delta_r, clopper_pearson


def algorithmic_efficiency(args, progress_bar=False):
    reference = args.pop('reference', None)
    target = args.pop('target', None)
    path = args.pop('path', None)
    match_args = args.pop('match_args', {'dR_cutoff': 0.3})
    xaxis_opts = args.pop('xaxis_opts', ['eta'])
    xaxis_bins = args.pop('xaxis_bins', {})
    label = args.pop('label', 'label')
    pt_cut = args.pop('pt_cut', 24)

    if path is None:
        raise Exception('Please specify input path')
    if (reference is None) or (target is None):
        raise Exception('Reference and target collections must be specified!')

    ref_muons = MuCollection()
    trg_muons = MuCollection()

    # Get muon data
    print(f"Processing {label}")
    loop = tqdm(glob.glob(path)) if progress_bar else glob.glob(path)
    for fname in loop:
        tree = uproot.open(fname)['muonNtuples']['muonTree']['event']
        ref_properties = {
            'pt': tree[f'{reference}.pt'].array(),
            'eta': tree[f'{reference}.eta'].array(),
            'phi': tree[f'{reference}.phi'].array()
        }
        trg_properties = {
            'pt': tree[f'{target}.pt'].array(),
            'eta': tree[f'{target}.eta'].array(),
            'phi': tree[f'{target}.phi'].array()
        }
        ref_muons += MuCollection(**ref_properties)
        trg_muons += MuCollection(**trg_properties)

    # check if a muon from reference collection (e.g. L2)
    # has a match in target collection (e.g. L3)
    ref_is_matched = match(ref_muons, trg_muons, **match_args)
    ref_matched = ref_muons.pt[ref_is_matched]

    ret = {}
    for x in xaxis_opts:
        if x not in xaxis_bins:
            raise Exception(f"Invalid x-axis: {x}")
        bins = xaxis_bins[x]
        ret[x] = {
            label: get_efficiency_hist(
                data=ref_muons,
                x=x,
                bins=bins,
                decision_mask=ref_is_matched,
                pt_cut=pt_cut
            )
        }
    return ret


def get_efficiency_hist(data, x, bins, decision_mask, pt_cut):
    pt = getattr(data, 'pt')
    data = getattr(data, x)
    values = np.array([])
    errors_lo = np.array([])
    errors_hi = np.array([])
    for ibin in range(len(bins)-1):
        bin_min = bins[ibin]
        bin_max = bins[ibin+1]
        cut = (data >= bin_min) & (data < bin_max) & (pt > pt_cut)
        total = ak.count(data[cut], axis=None)
        passed = ak.count(data[cut & decision_mask], axis=None)
        if total == 0:
            value = err_lo = err_hi = 0
        else:
            value = passed / total

            # Clopper-Pearson errors
            lo, hi = clopper_pearson(total, passed, 0.327)
            err_lo = value - lo
            err_hi = hi - value

            # binominal errors
            # err_lo = err_hi = (1 / total) * (np.sqrt(total * value * (1 - value)))

        values = np.append(values, value)
        errors_lo = np.append(errors_lo, err_lo)
        errors_hi = np.append(errors_hi, err_hi)

    ret = {
        'values': values,
        'errors': [
            errors_lo,
            errors_hi
        ],
        'edges': bins
    }
    return ret


def plot_entries(entries, x_vars, **kwargs):
    title = kwargs.pop('title', '')
    name_prefix = kwargs.pop('name_prefix', 'test')
    out_path = kwargs.pop('out_path', './')
    ymin = kwargs.pop('ymin', 0.8)
    ymax = kwargs.pop('ymax', 1.1)

    to_plot = {}
    for x in x_vars:
        to_plot[x] = {}
        for eff in entries:
            to_plot[x].update(eff[x])

    for x, data in to_plot.items():
        plot(
            data,
            title=title,
            name=f"{name_prefix}{x}",
            xlabel=x,
            ymin=ymin,
            ymax=ymax,
            out_path=out_path
        ) 


def plot(data, **kwargs):
    name = kwargs.pop('name', 'test')
    xlabel = kwargs.pop('xlabel', 'xlabel')
    ymin = kwargs.pop('ymin', 0.0)
    ymax = kwargs.pop('ymax', 1.1)
    out_path = kwargs.pop('out_path', './')

    if len(data)==0:
        raise Exception("Nothing to plot!")

    # Prepare canvas
    fig = plt.figure()
    plt.rcParams.update({'font.size': 12})
    data_opts = {'marker': '.', 'markersize': 8}
    fig.clf()
    plotsize = 6
    fig.set_size_inches(plotsize, plotsize)
    plt1 = fig.add_subplot(1, 1, 1)


    for label, hist in data.items():
        bins = np.array(hist['edges'])
        xerr = (bins[1:] - bins[:-1]) / 2.

        # Draw efficiency plot(s)
        ax = hep.histplot(
            hist['values'],
            bins,
            histtype='errorbar',
            xerr=[xerr],
            yerr=[hist['errors']],
            label=label,
            **data_opts
        )

    # Draw line at 1.0
    plt1.plot([bins[0], bins[-1]], [1., 1.], 'b--', linewidth=0.5, zorder=-1)

    # Styling
    lbl = hep.cms.label(ax=plt1, data=False, paper=False, year='')
    plt1.set_ylim(ymin, ymax)
    plt1.set_xlabel(xlabel)
    plt1.legend(prop={'size': 'small'})

    try:
        os.mkdir(out_path)
    except Exception:
        pass

    out_name = f'{out_path}/{name}.png'
    fig.savefig(out_name)
    print(f'Saved: {out_name}')

