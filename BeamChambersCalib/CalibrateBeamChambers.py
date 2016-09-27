#! /usr/bin/env python

import sys
import argparse

import numpy as np

from ROOT import gROOT, kGray, gStyle, TColor, TFile, TChain, TH1F, TH2F, TCanvas, TGraph, TF1
from root_numpy import root2array, tree2array, fill_hist


# Joakim Olsson, UChicago (joakim.olsson@cern.ch)
# Created 2016-10-22

# Usage:
# python CalibrateBeamChambers.py -bc BC_NUMBER -r LEFT_UP_CALIB_RUN CENTER_CALIB_RUN RIGHT_DOWN_CALIB_RUN --plots
#
# Example:
# python CalibrateBeamChambers.py -bc 1 -r 611274 611276 611278 --path tiletb_September2016 --plots

def main():

    # Parse input arguments
    parser = argparse.ArgumentParser(description = 'Perform beam chamber calibration')
    parser.add_argument('-bc', '--beam_chamber', dest='bc', required=True, type=int, choices=[1,2],
                        default = 1, help='Specify the beam chamber to calibrate')
    parser.add_argument('-r', '--runs', dest='runs', nargs=3, required=True, type=int,
                        default = [611274, 611276, 611278], help='List of calibration runs to process (LEFT_UP CENTER RIGHT_DOWN')
    parser.add_argument('-n', '--nevents', dest='nevents', type=int,
                        default = -1, help='Number of events to process')
    parser.add_argument('--plots', action = 'store_true', default = False, help='Save calibration plots')
    parser.add_argument('--test_calib', action = 'store_true', default = False, help='Test calibration')
    parser.add_argument('-p', '--path', dest='input_path', default='./',
                        help='Path to input files')
    parser.add_argument('-t', '--tree', dest='treename', default='h1000',
                        help='Name of input TTree')
    parser.add_argument('--verbose', '-v', action='count')

    if len(sys.argv) < 2:
        parser.print_help()
        print('\nexample: python CalibrateBeamChambers.py -bc 1 -r 611274 611276 611278 --path tiletb_September2016 --plots\n')
        sys.exit(1)

    args = parser.parse_args()

    debug = 0
    if (args.verbose > 0):
        debug = args.verbose

    if args.test_calib:
        test_calib()
        # TODO Add code to test applying the calibration

    else:

        # calibration of BC
        pos_leftup = get_calib_pos(args.runs[0], args.bc, args.nevents, args.treename,
                                   args.input_path, args.plots, debug)
        pos_center = get_calib_pos(args.runs[1], args.bc, args.nevents, args.treename,
                                   args.input_path, args.plots, debug)
        pos_rightdown = get_calib_pos(args.runs[2], args.bc, args.nevents, args.treename,
                                      args.input_path, args.plots, debug)

        if debug:
            print '\n----> Calibration positions'
            print 'Left/Up (run {}):'.format(args.runs[0])
            print pos_leftup
            print 'Center (run {}):'.format(args.runs[1])
            print pos_center
            print 'Right/Down (run {}):'.format(args.runs[2])
            print pos_rightdown

        runs_tag = ''

        for i,run in enumerate(args.runs):
            if (i < len(args.runs)-1):
                runs_tag += '{:d}_'.format(run)
            else:
                runs_tag += '{:d}'.format(run)
        calib = get_calib(pos_leftup, pos_center, pos_rightdown, args.bc, runs_tag, args.plots, debug)

        print '\n----> Results of the calibration for BC{}\n'.format(args.bc)
        print 'Horizontal slope = {0:2f}'.format(float(calib['x_slope']))
        print 'Horizontal offset = {}\n'.format(calib['x_offset'])
        print 'Vertical slope = {}'.format(calib['y_slope'])
        print 'Vertical offset = {}\n'.format(calib['y_offset'])

def get_calib_pos(run, bc = 1, nevents = -1, treename = 'h1000', input_path = './', save_plots = False, debug = 0):

    if (bc < 1 or bc > 2):
        print('ERROR: Invalid BC#, must be either 1 or 2')

    # mapping : BC1 : left = 0, right = 1, up = 2, down = 3
    #           BC2 : left = 4, right = 5, up = 6, down = 7
    l = 0; r = 1; u = 2; d = 3
    if bc == 2:
        l = 4; r = 5; u = 6; d = 7
    if debug == 2:
        print 'Running calibration for BC{}'.format(bc)

    chain = TChain(treename)
    chain.Add(input_path+'/tiletb_{}.root'.format(run))

    bc_array = tree2array(chain, branches=['btdc1'], start=0, stop=nevents)

    cut_min = 0
    cut_max = 10000

    if save_plots:
       h = HistogramManager('run_{}_bc_{}'.format(run, bc))
       h.add_h1('sumx', 'sumx', 100, -5000, 5000)
       h.add_h1('sumy', 'sumy', 100, -5000, 5000)
       h.add_h1('deltax', 'deltax', 100, -500, 500)
       h.add_h1('deltay', 'deltay', 100, -500, 500)
       h.add_h2('deltay_vs_deltax', '#Delta t (right-left)', 100, -250, 250, '#Delta t (up-down)', 100, -250, 250)

    deltax = np.zeros(len(bc_array))
    deltay = np.zeros(len(bc_array))
    for i_i, bc_pos_i in np.ndenumerate(bc_array):
        i = i_i[0]
        bc_pos = bc_pos_i[0]
        sumx = bc_pos[r]+bc_pos[l]
        sumy = bc_pos[u]+bc_pos[d]
        deltax_tmp = bc_pos[r]-bc_pos[l]
        deltay_tmp = bc_pos[u]-bc_pos[d]
        if save_plots:
            h.fill_1d('sumx', sumx)
            h.fill_1d('sumy', sumy)
        pass_x_cut = cut_min < sumx and sumx < cut_max
        pass_y_cut = cut_min < sumy and sumy < cut_max
        if pass_x_cut:
            deltax[i] = deltax_tmp
            h.fill_1d('deltax', deltax_tmp)
        if pass_x_cut:
            deltay[i] = deltay_tmp
            h.fill_1d('deltay', deltay_tmp)
        if pass_x_cut and pass_y_cut:
            h.fill_2d('deltay_vs_deltax', deltax_tmp, deltay_tmp)

    deltax_avg = np.mean(deltax)
    deltax_std = np.std(deltax)
    deltax_rms = np.sqrt(np.mean(np.square(deltax)))
    deltay_avg = np.mean(deltay)
    deltay_std = np.std(deltay)
    deltay_rms = np.sqrt(np.mean(np.square(deltay)))

    if debug == 2:
        print 'x-axis: avg = {}, std = {}, rms = {}'.format(deltax_avg, deltax_std, deltax_rms)
        print 'y-axis: avg = {}, std = {}, rms = {}'.format(deltay_avg, deltay_std, deltay_rms)

    if save_plots:
        gStyle.SetGridColor(kGray+1)
        gStyle.SetGridStyle(7)
        gStyle.SetGridWidth(2)
        c1 = TCanvas()
        c1.Divide(2,2)
        c1.cd(1)
        h.hists['sumx'].Draw('hist')
        c1.cd(2)
        h.hists['sumy'].Draw('hist')
        c1.cd(3)
        h.hists['deltax'].Draw('hist')
        c1.cd(4)
        h.hists['deltay'].Draw('hist')
        c1.SaveAs('calibration_pos_bc_{}_run_{}.pdf'.format(bc, run))
        c2 = TCanvas()
        c2.SetLeftMargin(0.12)
        c2.SetRightMargin(0.15)
        c2.SetTopMargin(0.08)
        c2.SetBottomMargin(0.15)
        c2.SetGridx(1)
        c2.SetGridy(1)
        c2.SetTickx()
        c2.SetTicky()
        h.hists['deltay_vs_deltax'].SetTitle('')
        h.hists['deltay_vs_deltax'].Draw('colz')
        c2.SaveAs('calibration_pos_deltay_vs_deltax_bc_{}_run_{}.pdf'.format(bc, run))

    return { 'x' : deltax_avg, 'xerr' : deltax_std, 'y' : deltay_avg, 'yerr' : deltay_std }

def get_calib(pos_leftup, pos_center, pos_rightdown, bc, runs_tag, save_plots = False, debug = 0):

    fix_pts_x = np.array([-30, 0, 30])
    fix_pts_y = np.array([30, 0, -30])
    x = np.array([pos_leftup['x'], pos_center['x'], pos_rightdown['x']])
    y = np.array([pos_leftup['y'], pos_center['y'], pos_rightdown['y']])

    # fit line to points
    x_fit = np.poly1d(np.polyfit(x, fix_pts_x, 1))
    y_fit = np.poly1d(np.polyfit(y, fix_pts_y, 1))

    if save_plots:

        import matplotlib.pyplot as plt
        import pylab as pl
        title_font = {'size':'18', 'weight':'normal'}
        axis_font = {'size':'16'}
        label_font = {'size':'20'}

        t = np.arange(-200, 200, 0.1)
        plt.figure(figsize=(11,5))
        plt.subplot(1,2,1)
        plt.plot(x, fix_pts_x, 'o', markersize=12, label='calibration points')
        plt.plot(t, x_fit(t), '-', linewidth=2, color='red', label='linear fit')
        plt.xlabel('$\Delta t$ (right-left) [ns]', **axis_font)
        plt.ylabel('[mm]', **axis_font)
        plt.xlim([-200,200])
        plt.ylim([-35,35])
        # plt.grid()
        pl.figtext(0.15, 0.26, 'Horizontal', **label_font)
        pl.figtext(0.15, 0.20, 'Slope = {:.4f}'.format(x_fit[1]), **label_font)
        pl.figtext(0.15, 0.14, 'Offset = {:.4f}'.format(x_fit[0]), **label_font)
        # plt.legend()
        labels = ['L/U', 'C', 'R/D']
        for label, xi, yi in zip(labels, x, fix_pts_x):
            plt.annotate(
                label,
                xy = (xi, yi), xytext = (20, 20),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5))
        plt.subplot(1,2,2)
        plt.plot(y, fix_pts_y, 'o', markersize=12, label='calibration points')
        plt.plot(t, y_fit(t), '-', linewidth=2, color='red', label='linear fit')
        plt.xlabel('$\Delta t$ (up-down) [ns]', **axis_font)
        plt.xlim([-200,200])
        plt.ylim([-35,35])
        # plt.grid()
        pl.figtext(0.58, 0.26, 'Vertical', **label_font)
        pl.figtext(0.58, 0.20, 'Slope = {:.4f}'.format(y_fit[1]), **label_font)
        pl.figtext(0.58, 0.15, 'Offset = {:.4f}'.format(y_fit[0]), **label_font)

        plt.legend(bbox_to_anchor=(1.25, 1.1))
        plt.suptitle('Calibration fits for beam chamber #{:d}'.format(bc), **title_font)
        for label, xi, yi in zip(labels, x, fix_pts_x):
            plt.annotate(
                label,
                xy = (xi, yi), xytext = (20, 20),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5))
        plt.savefig('calibration_fit_bc_{:d}_runs_{}.pdf'.format(bc, runs_tag))

    return {'x_offset': x_fit[0], 'x_slope': x_fit[1],
            'y_offset': y_fit[0], 'y_slope': y_fit[1]}

def test_calib():
    print 'Function not implemented yet'

class HistogramManager:

    def __init__(self, tag = ''):
        self.tag = tag
        self.hists = {}

    def add_h1(self, name,
                xlabel, xbins, xlow, xhigh):
        title = name
        fullname = name
        if self.tag != '':
            fullname = self.tag+'_'+name
        hist = TH1F(fullname, title,
                    xbins, xlow, xhigh)
        hist.GetXaxis().SetTitle(xlabel);
        hist.Sumw2()
        self.hists[name] = hist

    def add_h2(self, name,
                xlabel, xbins, xlow, xhigh,
                ylabel, ybins, ylow, yhigh):
        title = name
        fullname = name
        if self.tag != '':
            fullname = self.tag+'_'+name
        hist = TH2F(fullname, title,
                    xbins, xlow, xhigh,
                    ybins, ylow, yhigh)
        hist.GetXaxis().SetTitle(xlabel);
        hist.GetYaxis().SetTitle(ylabel);
        hist.Sumw2()
        self.hists[name] = hist

    def add_h3(self, name,
               xlabel, xbins, xlow, xhigh,
               ylabel, ybins, ylow, yhigh,
               zlabel, zbins, zlow, zhigh):
        title = name
        fullname = name
        if self.tag != '':
            fullname = self.tag+'_'+name
        hist = TH3F(fullname, title,
                    xbins, xlow, xhigh,
                    ybins, ylow, yhigh,
                    zbins, zlow, zhigh)
        hist.GetXaxis().SetTitle(xlabel);
        hist.GetYaxis().SetTitle(ylabel);
        hist.GetZaxis().SetTitle(ylabel);
        hist.Sumw2()
        self.hists[name] = hist

    def add_p(self, name,
                xlabel, xbins, xlow, xhigh,
                ylabel, ybins, ylow, yhigh,
                option):
        title = name
        fullname = name
        if self.tag != '':
            fullname = self.tag+'_'+name
        hist = TProfile(fullname, title,
                    xbins, xlow, xhigh,
                    ybins, ylow, yhigh,
                    option)
        hist.GetXaxis().SetTitle(xlabel);
        hist.GetYaxis().SetTitle(ylabel);
        hist.Sumw2()
        self.hists[name] = hist

    def fill_1d(self, key, x, w = 1.0):
        if key in self.hists:
            self.hists[key].Fill(x, w)

    def fill_2d(self, key, x, y, w = 1.0):
        if key in self.hists:
            self.hists[key].Fill(x, y, w)

    def fill_3d(self, key, x, y, z, w = 1.0):
        if key in self.hists:
            self.hists[key].Fill(x, y, z, w)

    def nhists(self):
        return len(self.hists)

if __name__ == '__main__':
    main()
