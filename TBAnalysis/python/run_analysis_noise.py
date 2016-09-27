#! /usr/bin/env python

import sys
import argparse
import time

from ROOT import TChain, TFile
from root_numpy import root2array, tree2array, fill_hist

# Joakim Olsson (joakim.olsson@cern.ch)

def main(argv):

    start_time = time.time()

    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nevents', dest='nevents', required=False, type=int,
                        default = -1, help='Number of events to process')
    parser.add_argument('-r', '--runs', dest='runs', nargs='*', required=False, type=int,
                        default = [610611], help='List of runs to process')
    parser.add_argument('-p', '--path', dest='input_path', default='/Users/joakim/GoogleDrive/CERN/TileCal-TestBeams/TestBeamAnalysis/ntuples/raw/',
                        help='Path to input files')
    parser.add_argument('-o', '--output', dest='output_file', default='output.root',
                        help='Name of output root file')
    parser.add_argument('-t', '--tree', dest='treename', default='dataTree',
                        help='Name of input TTree')
    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args()
    nevents = args.nevents
    runs = args.runs
    input_path = args.input_path
    treename = args.treename
    output_file = args.output_file

    options = {'do_avg_sample': False}

    # Analyze TTrees
    debug = 0
    if (args.verbose > 0):
        debug = args.verbose

    chain = TChain(args.treename)
    for run in runs:
        chain.Add(input_path+'/Data_20160000000000_testbeam_{}.root'.format(run))

    if debug:
        print('\n----> Converting ttree to numpy array')
    samples_hi = tree2array(chain, branches=['samples_hi'], start=0, stop=nevents)
    samples_lo = tree2array(chain, branches=['samples_lo'], start=0, stop=nevents)
    if debug:
        print('Done converting ttree, elapsed time: %s seconds ---' % (time.time() - start_time))

    if debug:
        print('\n----> Running analysis')
    from analysis_noise import process_events
    hists_hi = process_events(samples_hi, 'hi', options, debug)
    hists_lo = process_events(samples_lo, 'lo', options, debug)
    if debug:
        print('Done running analysis, elapsed time: %s seconds ---' % (time.time() - start_time))

    if debug:
        print('\n----> Writing histograms to file')
    output = TFile.Open(output_file, "RECREATE")
    for name, hist in hists_hi.iteritems():
        hist.Write()
    for name, hist in hists_lo.iteritems():
        hist.Write()
    output.Close()

    if debug:
        print('\n--- Done! Run time: %s seconds ---' % (time.time() - start_time))

if __name__ == '__main__':
    main(sys.argv)
