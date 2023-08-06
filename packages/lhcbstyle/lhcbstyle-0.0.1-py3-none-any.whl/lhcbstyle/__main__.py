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
import argparse
import importlib.resources
import os
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("--macro-dir", default=None)
    install_parser.set_defaults(func=lambda a: install(a.macro_dir))

    args = parser.parse_args()
    args.func(args)


def install(macro_dir):
    if not macro_dir:
        macro_dir = os.environ.get("ROOT_MACRO_DIR")
    if not macro_dir:
        import ROOT

        macro_dir = str(ROOT.gROOT.GetMacroDir())
    macro_dir = Path(macro_dir)

    print(f"Writing lhcbStyle.C to {macro_dir}")
    macro_dir.mkdir(exist_ok=True, parents=True)
    with importlib.resources.path("lhcbstyle", "lhcbStyle.C") as path:
        (macro_dir / "lhcbStyle.C").write_text(path.read_text())


if __name__ == "__main__":
    parse_args()  # pragma: no cover
