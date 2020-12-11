import numpy as np
import awkward1 as ak
import scipy


class MuCollection:
    def __init__(self, **kwargs):
        self.pt = kwargs.pop('pt', ak.highlevel.Array([]))
        self.eta = kwargs.pop('eta', ak.highlevel.Array([]))
        self.phi = kwargs.pop('phi', ak.highlevel.Array([]))

    def __iadd__(self, other):
        if self.pt is None:
            self.pt = other.pt
            self.eta = other.eta
            self.phi = other.phi
        else:
            self.pt = ak.concatenate([self.pt, other.pt])
            self.eta = ak.concatenate([self.eta, other.eta])
            self.phi = ak.concatenate([self.phi, other.phi])
        return self


def match(first, second, **kwargs):
    if 'dR_cutoff' not in kwargs:
        raise Exception("Please specify dR cutoff for matching!")
    dR_cutoff = kwargs.pop('dR_cutoff', 0.3)
    etas = ak.cartesian(
        {'first': first.eta, 'second': second.eta},
        axis=1,
        nested=True
    )
    phis = ak.cartesian(
        {'first': first.phi, 'second': second.phi},
        axis=1,
        nested=True
    )
    dR = delta_r(etas['first'], etas['second'], phis['first'], phis['second'])
    return ak.any(dR < dR_cutoff, axis=2)


def delta_r(eta1, eta2, phi1, phi2):
    deta = abs(eta1 - eta2)
    dphi = abs(np.mod(phi1 - phi2 + np.pi, 2*np.pi) - np.pi)
    dr = np.sqrt(deta**2 + dphi**2)
    return dr


def clopper_pearson(total, passed, level):
    alpha = (1.0 - level) / 2
    if total == passed:
        hi = 1.0
    else:
        hi = scipy.stats.beta.ppf(1 - alpha, passed + 1, total - passed)
    if passed == 0:
        lo = 0.0
    else:
        lo = scipy.stats.beta.ppf(alpha, passed, total - passed + 1.0)
    return lo, hi
