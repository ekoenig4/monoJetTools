from ROOT import *
from sys import argv

fn_unknown = TFile.Open(argv[1])
fn_known = TFile.Open(argv[2])

c_unknown = fn_unknown.Get("h_cutflow")
c_known = fn_known.Get("h_cutflow")
ibin=1
print fn_unknown.GetName(),c_unknown[ibin]
print fn_known.GetName(),c_known[ibin]
print 'ratio',c_unknown[ibin]/c_known[ibin]

