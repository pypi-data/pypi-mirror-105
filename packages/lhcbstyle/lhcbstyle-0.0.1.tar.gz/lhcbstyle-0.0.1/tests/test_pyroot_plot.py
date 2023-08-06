###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import ROOT

from lhcbstyle import LHCbStyle

XLOW, XUP = (5.100, 5.460)


def generate_data(nsig=1000, nbkg=1000):
    for _ in range(nsig):
        yield ROOT.gRandom.Gaus(5.280, 0.02)
    for _ in range(nbkg):
        yield ROOT.gRandom.Uniform(XLOW, XUP)


def make_plot():
    hist = ROOT.TH1D("hist", "#it{B}^{0} mass", 36, XLOW, XUP)
    for d in generate_data():
        hist.Fill(d)
    binw = hist.GetXaxis().GetBinWidth(1)
    hist.SetYTitle(f"Candidates / ({binw:.3f} GeV)")
    hist.SetXTitle("#it{m}(#it{B}^{0}) [GeV]")
    return hist


def test_without_lhcbstyle():
    # Plot without LHCbStyle
    can = ROOT.TCanvas()
    hist = make_plot()
    hist.Draw("E1")
    can.SaveAs("hist_plain.png")


def test_with_lhcbstyle():
    # Plot with LHCbStyle
    with LHCbStyle():
        can = ROOT.TCanvas()
        hist = make_plot()
        hist.Draw("E1")
        ROOT.LHCbStyle.lhcbName.Draw("same")
        can.SaveAs("hist_lhcb.png")
