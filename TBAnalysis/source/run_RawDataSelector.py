#! /usr/bin/env python

from ROOT import gROOT, TChain

# Joakim Olsson (joakim.olsson@cern.ch)

def main():

    input_path = "/Users/joakim/GoogleDrive/CERN/TileCal-TestBeams/TestBeamAnalysis/ntuples/raw/"
    input_files = ["Data_20160000000000_testbeam_610611.root"]
    treename = "dataTree"
    chain = TChain(treename)
    for input_file in input_files:
        print "Adding file: " + input_file
        chain.Add(input_path+"/"+input_file)
    print "----> Begin processing chain"
    gROOT.ProcessLine(".L HistogramManager.C")
    chain.Process("RawDataSelector.C", "tiletb_raw.root")
    # chain.Process("RawDataSelector.C", "tiletb_raw.root", 1, 1)

if __name__ == "__main__":
    main()
