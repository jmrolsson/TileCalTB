#! /usr/bin/env python
from ROOT import TH1F, TH2F, TH3F, TProfile, TFile

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
