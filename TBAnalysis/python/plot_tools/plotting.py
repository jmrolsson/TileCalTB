import os
import sys
import io
import re
import math

import numpy as np
from decimal import Decimal
from array import array

from ROOT import *
from eophelper.util import *

class PlotOptions:
    """ Set plot style options"""

    def __init__(self,
                 plot_name,
                 options = "",
                 do_data = False,
                 do_ratio = False,
                 do_norm = False,
                 do_norm_mc_to_data = False,
                 do_auto_scale = False,
                 draw_style = "hist",
                 marker_type = "data_mc",
                 leg_labels = [],
                 plot_tags = [],
                 atlas_label = "Internal",
                 lumi_label = "#sqrt{s} = 13 TeV, x fb_{-1}"
                 ):

        """ Inits PlotOptions with common parameters"""

        self.plot_name = plot_name

        self.do_data = do_data
        self.do_ratio = do_ratio
        self.do_norm = do_norm
        self.do_norm_mc_to_data = do_norm_mc_to_data
        self.do_auto_scale = do_auto_scale

        self.leg_labels = leg_labels
        self.plot_tags = plot_tags
        self.plot_cuts = []

        self.draw_style = draw_style
        self.marker_type = marker_type

        self.avg_ratio_x = 0.08
        self.avg_ratio_y = 0.50
        self.avg_ratio_txt = avg_ratio_txt

        self.title = ""
        self.xtitle = ""
        self.ytitle = "Events"
        if self.do_norm:
            self.ytitle = "Fraction of events"
        self.show_ytitle_res = False
        self.ztitle = ""

        self.unit = ""

        self.do_varbins = False
        self.rebin = 1
        self.rebinx = 1
        self.rebiny = 1
        self.scale = 1.
        self.gridx = False
        self.gridy = False
        self.ratio_gridx = False
        self.ratio_gridy = True
        self.logx = False
        self.logy = False
        self.logz = False
        self.logx = False
        self.logy = False
        self.logz = False

        self.c_widthx = 800
        self.c_widthy = 600

        self.ratio_label = "MC/Data"
        self.set_ratio_min_max = True
        self.ratio_min = 0.2
        self.ratio_max = 1.8
        self.ratio_logy = False
        self.ratio_logx = False

        self.legy = 0.90
        self.legx = 0.48
        self.legwx = 0.50
        self.legwy = 0.045
        self.leg_ncol = 1

        self.legcutsy = 0.80
        if not self.do_data:
            self.legcutsy = 0.85
        self.legcutsx = 0.1855
        self.legcutswx = 0.45
        self.legcutswy = 0.040


        self.atlasx = 0.19
        self.atlasy = 0.90
        self.atlas_label = atlas_label

        self.lumix = 0.19
        self.lumiy = 0.85
        self.lumi_label = lumi_label

        self.top_padding = 0.9
        self.logy_padding = 1e5
        if ("pileup" in options):
            self.logy_padding = 1e3

        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.zmin = 0
        self.zmax = 0

        self.color_alpha = 0.9

        self.auto_scale_ratio = False
        self.auto_scale_err = False

        self.x_ndivisions = None
        self.y_ndivisions = None
        self.y_ndivisions_ratio = 805

        self.profilex = False
        self.profiley = False

        self.do_custom_bin_labels = False
        self.custom_bin_labels = []

        #### Custom parameters for specific plot names ####

def colors(i, color_type = None):
    """ Provides a list of pretty plot colors"""

##http://www.colorcombos.com/color-schemes/4291/ColorCombo4291.html
#    colors_sig = [
#        TColor.GetColor(238,61,17), # orange red
#        TColor.GetColor(184,158,56), # dark yellow
#        TColor.GetColor(19,196,113), # light greenish
#        TColor.GetColor(12,169,198), # light blue
#        TColor.GetColor(147,100,141), # purpule
#        TColor.GetColor(64,64,64), # black
#    ]
    colors_sig = [
        TColor.GetColor(57,106,177), # blue
        TColor.GetColor(218,124,48), # orange
        TColor.GetColor(62,150,81), # green
        TColor.GetColor(204,37,41), # red
        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow

        ## EXTRA COLORS
        TColor.GetColor(114,147,203), # blue
        TColor.GetColor(255,151,76), # orange
        TColor.GetColor(132,186,91), # green
        TColor.GetColor(211,94,96), # red
        TColor.GetColor(128,133,133), # gray
        TColor.GetColor(144,103,167), # purple
        TColor.GetColor(171,104,87), # brown
        TColor.GetColor(204,194,16), # yellow

        ## REPEAT COLORS
        TColor.GetColor(114,147,203), # blue
        TColor.GetColor(255,151,76), # orange
        TColor.GetColor(132,186,91), # green
        TColor.GetColor(211,94,96), # red
        TColor.GetColor(128,133,133), # gray
        TColor.GetColor(144,103,167), # purple
        TColor.GetColor(171,104,87), # brown
        TColor.GetColor(204,194,16), # yellow

        TColor.GetColor(57,106,177), # blue
        TColor.GetColor(218,124,48), # orange
        TColor.GetColor(62,150,81), # green
        TColor.GetColor(204,37,41), # red
        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow
    ]

    colors_sig_red_first = [
        TColor.GetColor(204,37,41), # red
        TColor.GetColor(57,106,177), # blue
        TColor.GetColor(218,124,48), # orange
        TColor.GetColor(62,150,81), # green
        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow
    ]

    colors_sig_light = [
        TColor.GetColor(114,147,203), # blue
        TColor.GetColor(255,151,76), # orange
        TColor.GetColor(132,186,91), # green
        TColor.GetColor(211,94,96), # red
        TColor.GetColor(128,133,133), # gray
        TColor.GetColor(144,103,167), # purple
        TColor.GetColor(171,104,87), # brown
        TColor.GetColor(204,194,16), # yellow

        ## EXTRA COLORS
        TColor.GetColor(57,106,177), # blue
        TColor.GetColor(218,124,48), # orange
        TColor.GetColor(62,150,81), # green
        TColor.GetColor(204,37,41), # red
        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow

        ## REPEAT COLORS
        TColor.GetColor(114,147,203), # blue
        TColor.GetColor(255,151,76), # orange
        TColor.GetColor(132,186,91), # green
        TColor.GetColor(211,94,96), # red
        TColor.GetColor(128,133,133), # gray
        TColor.GetColor(144,103,167), # purple
        TColor.GetColor(171,104,87), # brown
        TColor.GetColor(204,194,16), # yellow

        TColor.GetColor(57,106,177), # blue
        TColor.GetColor(218,124,48), # orange
        TColor.GetColor(62,150,81), # green
        TColor.GetColor(204,37,41), # red
        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow

    ]
    colors_bkgd = [
        kBlack, # black
        TColor.GetColor(204, 0, 0), # red
        TColor.GetColor(51, 102, 153), # blue
        TColor.GetColor(44, 103, 0), # green
        TColor.GetColor(255, 153, 0), # orange
        TColor.GetColor(141, 89, 36) #brown
    ]

    colors_print = [
        kBlack,
        #TColor.GetColor(228,26,28),
        #TColor.GetColor(55,126,184),
        #TColor.GetColor(77,175,74),
        #TColor.GetColor(152,78,163),
        #TColor.GetColor(255,127,0),
        #TColor.GetColor("#332288"),
        #TColor.GetColor("#88CCEE"),
        #TColor.GetColor("#44AA99"),
        #TColor.GetColor("#117733"),
        #TColor.GetColor("#999933"),
        #TColor.GetColor("#DDCC77"),
        #TColor.GetColor("#CC6677"),
        #TColor.GetColor("#882255"),
        #TColor.GetColor("#AA4499"),

        # https://#font[50]{p}ersonal.sron.nl/~pault/colourschemes.pdf
        #TColor.GetColor("#332288"),
        #TColor.GetColor("#117733"),
        #TColor.GetColor("#CC6677"),
        #TColor.GetColor("#DDCC77"),

        #TColor.GetColor("#88CCEE"),
        #TColor.GetColor("#CC6677"),
        #TColor.GetColor("#117733"),

        #TColor.GetColor("#88CCEE"),
        #TColor.GetColor("#999933"),
        #TColor.GetColor("#882255"),
        TColor.GetColor("#003366"),
        TColor.GetColor("#E6642C"),
        TColor.GetColor("#91BD61"),
        TColor.GetColor("#D92120"),
        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow
    ]
    colors_print_sig_only = [
        #TColor.GetColor("#404096"),
        #TColor.GetColor("#529DB7"),
        #TColor.GetColor("#7DB874"),
        #TColor.GetColor("#E39C37"),
        #TColor.GetColor("#D92120"),

        #TColor.GetColor("#332288"),
        #TColor.GetColor("#88CCEE"),
        #TColor.GetColor("#117733"),
        #TColor.GetColor("#DDCC77"),
        #TColor.GetColor("#CC6677"),

        #TColor.GetColor("#8C2D04"),
        #TColor.GetColor("#CC4C02"),
        #TColor.GetColor("#EC7014"),
        #TColor.GetColor("#FB9A29"),
        #TColor.GetColor("#FEC44F"),

        #TColor.GetColor("#4065B1"),
        #TColor.GetColor("#529DB7"),
        #TColor.GetColor("#91BD61"),
        #TColor.GetColor("#E6642C"),
        #TColor.GetColor("#D92120"),
        #TColor.GetColor("#AA7744"),

        TColor.GetColor("#003366"),
        TColor.GetColor("#529DB7"),
        TColor.GetColor("#91BD61"),
        TColor.GetColor("#E6642C"),
        TColor.GetColor("#D92120"),

        TColor.GetColor("#4065B1"),
        TColor.GetColor("#E6642C"),
        TColor.GetColor("#91BD61"),
        TColor.GetColor("#529DB7"),
        TColor.GetColor("#D92120"),
        TColor.GetColor("#AA7744"),

        TColor.GetColor(83,81,84), # gray
        TColor.GetColor(107,76,154), # purple
        TColor.GetColor(146,36,40), # brown
        TColor.GetColor(148,139,61), # yellow
    ]
    colors_print_sig_only_3 = [
        TColor.GetColor("#003366"),
        TColor.GetColor("#3883fa"),
        TColor.GetColor("#529DB7"),
        #kGreen+2,
        #TColor.GetColor("#91BD61"),
    ]

    colors = []
    if (color_type == "data_mc"):
        colors = [kBlack]
        colors.extend(colors_sig)
    if (color_type == "data_mc_red_first"):
        colors = [kBlack]
        colors.extend(colors_sig_red_first)
    if (color_type == "sig_only"):
        colors = colors_sig
    if (color_type == "sig_light_only"):
        colors = colors_sig_light
    elif (color_type == "bkgd_only"):
        colors = colors_bkgd
    elif (color_type == "1bkgd"):
        colors.append(colors_bkgd[0])
        colors.extend(colors_sig)
    elif (color_type == "2bkgd"):
        colors.extend(colors_bkgd[0:2])
        colors.extend(colors_sig)
    elif (color_type == "3bkgd"):
        colors.extend(colors_bkgd[0:3])
        colors.extend(colors_sig)
    elif (color_type == "1bkgd_light"):
        colors.append(colors_bkgd[0])
        colors.extend(colors_sig_light)
    elif (color_type == "2bkgd_light"):
        colors.extend(colors_bkgd[0:2])
        colors.extend(colors_sig_light)
    elif (color_type == "3bkgd_light"):
        colors.extend(colors_bkgd[0:3])
        colors.extend(colors_sig_light)
    elif (color_type == "4bkgd_light"):
        colors.extend(colors_bkgd[0:4])
        colors.extend(colors_sig_light)
    elif (color_type == "bkgd"):
        colors.extend(colors_bkgd)
    elif (color_type == "default_light"):
        colors.append(TColor.GetColor(64,64,64))
        colors.extend(colors_sig_light)
    elif (color_type == "box2D"):
        colors.append(kRed)
        colors.extend(colors_sig)
    elif (color_type == "from_max"):
        colors.append(kBlack)
        colors.append(kViolet+9)
        colors.append(kTeal-5)
        colors.append(kRed+2)
        colors.append(kMagenta+3);
    elif (color_type == "print"):
        colors.extend(colors_print)
    elif (color_type == "print_sig_only_3"):
        colors.extend(colors_print_sig_only_3)
    elif (color_type == "print_sig_only"):
        colors.extend(colors_print_sig_only)

    # Default colors
    else:
        colors.append(kBlack)
        colors.extend(colors_sig)

    return colors[i % len(colors)]

# Provides a list of nice markers
def markers(i, marker_type = None):
    """ Provides a list of good looking markers """

    # Data/MC
    if ("data_mc" in marker_type):
        markers = [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # MC
    if (marker_type == "mc"):
        markers = [
            21, 22, 23, 24, 25, 26, 32, 27, 28, 30
        ]
    # Background
    elif (marker_type == "bkgd"):
        markers = [
            20, 21, 22, 23, 33, 29, 34
        ]
    # 1 background, the rest signal
    elif (marker_type == "1bkgd"):
        markers = [
            21, 24, 25, 26, 27, 32, 28, 30
        ]
    # 2 background, the rest signal
    elif (marker_type == "2bkgd"):
        markers = [
            21, 22, 24, 25, 26, 27, 32, 28, 30
        ]
    # 3 background, the rest signal
    elif (marker_type == "3bkgd"):
        markers = [
            21, 22, 23, 24, 25, 26, 27, 32, 28, 30
        ]
    # Signal
    elif (marker_type == "sig"):
        markers = [
            24, 25, 26, 32, 27
        ]
    # Alternating solid and hollow markers
    elif (marker_type == "sh"):
        markers = [
            20, 24, 21, 25, 22, 26, 23, 32, 33, 27, 29, 30, 34, 28
        ]
    # Default markers
    else:
        markers = [
            20, 21, 22, 23, 24, 25, 26, 32, 27, 28, 30, 33, 34
        ]

    return markers[i % len(markers)]

# Provides a list of dashed and dotted line styles
def lines(i):
    styles = [
        1, 7, 5, 2, 10, 9, 6, 8, 4
    ]
    return styles[i % len(styles)]

def setup_canvas(name, title, gridx, gridy, logx, logy, logz, widthx = 600, widthy = 600, left_margin = 0.1499436, right_margin = 0.1273957):
    """ Initialize a canvas with appropriate settings """

    gStyle.SetOptStat(0)
    gStyle.SetTextAlign(21)
    #gStyle.SetGridColor(kBlack)
    gStyle.SetGridColor(kGray+1)
    gStyle.SetGridStyle(7)
    gStyle.SetGridWidth(2)
    gStyle.SetHatchesLineWidth(1)
    gStyle.SetHatchesSpacing(0.7)

    #Set Canvas sizes
    gStyle.SetCanvasDefW(widthx);
    gStyle.SetCanvasDefH(widthy);

    # Create a canvas if one does not already exist
    if ("TCanvas" not in str(gROOT.FindObject(name))):
        c1 = TCanvas(name, title)
    else:
        c1 = gROOT.FindObject(name)

    c1.Clear()
    # c1.Range(-7.074883, -13.91156, 6.762871, 12.07483)
    c1.Range(-10, -10, 10, 10)
    c1.SetFillColor(kWhite)
    c1.SetBorderMode(0)
    c1.SetBorderSize(2)
    #c1.SetLineColor(kGray+2)
    c1.SetGridx(gridx)
    c1.SetGridy(gridy)
    c1.SetLogx(logx)
    c1.SetLogy(logy)
    c1.SetLogz(logz)
    c1.SetTickx()
    c1.SetTicky()
    c1.SetLeftMargin(left_margin)
    c1.SetRightMargin(right_margin)
    # c1.SetTopMargin(0.07984293)
    # c1.SetBottomMargin(0.1505236)
    c1.SetTopMargin(0.08)
    c1.SetBottomMargin(0.15)

    return c1

def setup_legend(nentries, ncol, x_left, y_top, x_width, y_width, do_alpha = False):
    """ Initialize a legend with appropriate settings """

    if (nentries > 4 and ncol != 1):
        x_right  = x_left + ncol*0.5*x_width
        y_bottom = y_top - y_width*((nentries)*0.5)
    else:
        x_right  = x_left + x_width
        y_bottom = y_top - y_width*(nentries)

    leg = TLegend(x_left, y_bottom, x_right, y_top, "", "NB NDC")
    #pave = TPave(x_left, y_bottom, x_right, y_top, 0, "NB NDC ARC")

    if (nentries > 2):
        leg.SetNColumns(ncol)

    leg.SetLineColor(kWhite)
    leg.SetLineStyle(0)
    leg.SetLineWidth(0)
    leg.SetFillColor(kWhite)
    leg.SetBorderSize(0)
    leg.SetTextColor(1)
    leg.SetTextFont(42)
    if do_alpha:
        leg.SetFillStyle(1001)
        leg.SetFillColorAlpha(kGray, 0.95)
    else:
        leg.SetFillStyle(0)

    #pave.SetLineColor(kWhite)
    #pave.SetLineStyle(0)
    #pave.SetLineWidth(0)
    #pave.SetBorderSize(0)
    #pave.SetFillStyle(1001)
    #pave.SetFillColorAlpha(kGray, 0.7)
    #pave.SetCornerRadius(0.05)

    return leg #, pave

def save_hists_overlay(hlist, plot_opts, plot_output_path):
    """ overlay multiple plots on one canvas and save as pdf and/or svg """

    print "Saving plot: ", plot_output_path

    c1 = setup_canvas("c1", "canvas1",
                     plot_opts.gridx,  plot_opts.gridy,
                     plot_opts.logx, plot_opts.logy, plot_opts.logz,
                     plot_opts.c_widthx, plot_opts.c_widthy)

    leg = setup_legend(len(plot_opts.leg_labels)+len(plot_opts.plot_tags), 1,
                        plot_opts.legx, plot_opts.legy,
                        plot_opts.legwx, plot_opts.legwy)
    leg_cuts = setup_legend(len(plot_opts.plot_cuts), 1,
                        plot_opts.legcutsx, plot_opts.legcutsy,
                        plot_opts.legcutswx, plot_opts.legcutswy)

    for tag in plot_opts.plot_tags:
        leg.AddEntry("NULL", tag, "h")
    for tag in plot_opts.plot_cuts:
        leg_cuts.AddEntry("NULL", tag, "h")

    # scale and rebin
    for i,h in enumerate(hlist):

        h.GetXaxis().SetMoreLogLabels(True);
        h.GetXaxis().SetNoExponent(True);
        if (plot_opts.do_varbins and len(plot_opts.varbins) > 0):
            hlist[i] = h.Rebin(len(plot_opts.varbins)-1, "hnew", array('d', plot_opts.varbins))
        else:
            h.Rebin(plot_opts.rebin)
        h.Scale(plot_opts.scale)
        if plot_opts.do_norm:
            if (h.Integral() != 0):
                h.Scale(1./h.Integral())
        if plot_opts.do_norm_mc_to_data and i > 0:
            if (h.Integral() != 0):
                h.Scale(hlist[0].Integral()/h.Integral())

    # find maximum in plots
    if plot_opts.do_auto_scale:
        h_max = 0
        for h in hlist:
            max_bin = h.GetMaximumBin()
            tmp_max = h.GetBinContent(max_bin)
            if (plot_opts.auto_scale_err):
                tmp_max += h.GetBinError(max_bin)
            if h_max < tmp_max:
                h_max = tmp_max

    if plot_opts.do_ratio:
        # top pad
        ratio = 0.35
        epsilon = 0.05
        pad1 = TPad("pad1","pad1",0,ratio-epsilon,1,1)
        pad1.SetFillColor(kWhite)
        # pad1.SetTopMargin(.095)
        pad1.SetBottomMargin(epsilon)
        pad1.SetLeftMargin(.15)
        pad1.SetRightMargin(.1)
        pad1.SetLogx(plot_opts.logx)
        pad1.SetLogy(plot_opts.logy)
        pad1.SetBorderMode(0)
        pad1.SetBorderSize(2)
        pad1.SetTickx()
        pad1.SetTicky()
        pad1.SetGrid(plot_opts.gridx, plot_opts.gridy)
        pad1.Draw()

        # bottom pad
        pad2 = TPad("pad2","pad2",0,0,1,ratio*(1-epsilon))
        pad2.SetFillColor(0)
        pad2.SetFillStyle(0)
        pad2.SetTopMargin(epsilon)
        pad2.SetBottomMargin(0.35)
        pad2.SetLeftMargin(.15)
        pad2.SetRightMargin(.1)
        pad2.SetLogx(plot_opts.ratio_logx)
        pad2.SetLogy(plot_opts.ratio_logy)
        pad2.SetBorderMode(0)
        pad2.SetBorderSize(2)
        pad2.SetTickx()
        pad2.SetTicky()
        pad2.SetGrid(plot_opts.ratio_gridx, plot_opts.ratio_gridy)
        pad2.Draw()

    else:
        # only one pad
        pad = TPad("pad","pad",0,0,1,1)
        pad.SetTopMargin(0.04)
        pad.SetBottomMargin(0.17)
        pad.SetLeftMargin(.15)
        pad.SetRightMargin(.1)
        pad.SetFillColor(kWhite)
        pad.SetLogx(plot_opts.logx)
        pad.SetLogy(plot_opts.logy)
        pad.SetBorderMode(0)
        pad.SetBorderSize(2)
        pad.SetTickx()
        pad.SetTicky()
        pad.SetGrid(plot_opts.gridx, plot_opts.gridy)
        pad.Draw()

    # for drawing average line
    avg_lines = []
    avg_lines_txt = []
    avg_ratio_txt = []

    # overlay the plots
    for i, h in enumerate(hlist):

        # set maximum in x
        if (plot_opts.xmax != 0):
            h.GetXaxis().SetRangeUser(plot_opts.xmin, plot_opts.xmax)

        # set maximum in y
        if (plot_opts.ymax != 0):
            h.GetYaxis().SetRangeUser(plot_opts.ymin, plot_opts.ymax)

        # auto scaling
        if plot_opts.do_auto_scale:
            if plot_opts.logy: h.SetMaximum(h_max*plot_opts.logy_padding)
            else: h.SetMaximum(h_max*(1+plot_opts.top_padding))

        h.SetTitle(plot_opts.title)
        h.GetYaxis().SetDecimals(True)
        h.GetXaxis().SetTitle(plot_opts.xtitle)
        if plot_opts.show_ytitle_res:
            nbinsx = h.GetXaxis().GetNbins()
            rangex = h.GetXaxis().GetXmax() - h.GetXaxis().GetXmin()
            resx = rangex/nbinsx
            if resx == 1.0:
                resx_txt = " / "
            elif resx.is_integer():
                resx_txt = " / %d" % (resx)
            else:
                resx_txt = " / %.2f" % (resx)
            resx_txt += " " + plot_opts.unit
            h.GetYaxis().SetTitle(plot_opts.ytitle+resx_txt)
        else:
            h.GetYaxis().SetTitle(plot_opts.ytitle)

        h.SetLineStyle(lines(i))
        h.SetLineStyle(1)
        h.SetLineColorAlpha(colors(i, plot_opts.marker_type), plot_opts.color_alpha)
        h.SetLineWidth(2)

        h.SetMarkerColorAlpha(colors(i, plot_opts.marker_type), plot_opts.color_alpha)

        h.SetFillStyle(0)
        h.SetFillColor(0)
        h.SetMarkerSize(0)

        h.SetStats(0)

        if plot_opts.do_custom_bin_labels:
            for j,label in enumerate(plot_opts.custom_bin_labels):
                h.GetXaxis().SetBinLabel(j+1, label)
                h.GetXaxis().LabelsOption("v")

        if plot_opts.do_ratio:
            h.GetXaxis().SetLabelSize(0.00)
            # h.GetYaxis().SetLabelSize(0.0)
            h.GetYaxis().SetLabelSize(0.075)
            h.GetXaxis().SetTitleSize(0.00)
            # h.GetYaxis().SetTitleSize(0.0)
            h.GetYaxis().SetTitleSize(0.065)
            h.GetYaxis().SetTitleOffset(1.0)
            h.GetYaxis().SetDecimals(True)
        else:
            h.GetXaxis().SetLabelSize(0.050)
            h.GetYaxis().SetLabelSize(0.050)
            h.GetXaxis().SetTitleSize(0.050)
            h.GetYaxis().SetTitleSize(0.050)
            h.GetYaxis().SetTitleOffset(1.4)
            h.GetYaxis().SetDecimals(True)

        if plot_opts.x_ndivisions is not None:
            h.GetXaxis().SetNdivisions(plot_opts.x_ndivisions)

        # new hist for errorbars
        h2 = h.Clone()
        h2.SetFillStyle(3356)
        h2.SetFillColorAlpha(colors(i, plot_opts.marker_type),1.)
        h2.SetMarkerColorAlpha(colors(i, plot_opts.marker_type),0.)
        h2.SetMarkerStyle(0)
        h2.SetLineColorAlpha(colors(i, plot_opts.marker_type),1.)
        h2.SetLineStyle(1)
        h2.SetLineWidth(2)

        # draw on top pad
        if plot_opts.do_ratio:
            pad1.cd()
        else:
            pad.cd()
        if i == 0:
            if plot_opts.do_data:
                h.SetLineStyle(1)
                h.SetLineWidth(2)
                h.SetLineColor(kBlack)
                h.SetMarkerColor(kBlack)
                h.SetFillStyle(0)
                h.SetFillColor(0)
                h.SetMarkerStyle(20)
                h.SetMarkerSize(1.0)
                # h_data = h
                h.Draw("E")
                leg.AddEntry(h, plot_opts.leg_labels[i], "lep")
            else:
                h.Draw(plot_opts.draw_style)
                leg.AddEntry(h, plot_opts.leg_labels[i], "lpf")
        else:
            h2.SetFillStyle(3356)
            h2.SetFillColorAlpha(colors(i, plot_opts.marker_type),1.)
            h2.SetMarkerColorAlpha(colors(i, plot_opts.marker_type),0.)
            h2.SetMarkerStyle(0)
            h2.SetLineColorAlpha(colors(i, plot_opts.marker_type),1.)
            h2.SetLineStyle(1)
            h2.SetLineWidth(2)
            h2.Draw("E2 same")
            # h.SetLineStyle(lines(i))
            h.SetLineStyle(0)
            h.SetLineColorAlpha(colors(i, plot_opts.marker_type), 1.0)
            h.SetMarkerColorAlpha(colors(i, plot_opts.marker_type), 1.0)
            h.SetFillStyle(0)
            h.SetFillColor(0)
            h.Draw(plot_opts.draw_style+" same")
            leg.AddEntry(h, plot_opts.leg_labels[i], "lpf")

        # if plot_opts.do_data:
            # h_data.Draw("EX1 same")

        if plot_opts.draw_avg:
            if plot_opts.draw_avg_g0:
                zerobin = h.GetXaxis().FindBin(0)
                h.GetXaxis().SetRange(zerobin+1, h.GetXaxis().GetNbins())
                # print h.GetBinLowEdge(zerobin+1)
                # print zerobin+1
                # print h.GetXaxis().GetNbins()
            xmin = h.GetMean()
            # Restore default range
            h.GetXaxis().SetRange(1, h.GetXaxis().GetNbins())
            if (plot_opts.xmax != 0):
                h.GetXaxis().SetRangeUser(plot_opts.xmin, plot_opts.xmax)
            xmax = xmin
            ymin = h.GetMinimum()
            ymax = h.GetBinContent(h.GetMaximumBin())
            avg_line = TLine(xmin, ymin, xmax, ymax)
            avg_line.SetLineWidth(1)
            avg_line.SetLineStyle(lines(i)+1)
            avg_line.SetLineColorAlpha(colors(i, plot_opts.marker_type),1.)
            avg_lines.append(avg_line)
            # avg_line.Draw()

            if i == 0:
                if plot_opts.logy:
                    if 1e-4*ymax > 1e1*ymin:
                        avg_txt = TLatex(xmin+1.0, 1e-5*ymax, plot_opts.avg_txt.format(xmin))
                    else:
                        avg_txt = TLatex(xmin+1.0, 2e0*ymin, plot_opts.avg_txt.format(xmin))
                else:
                    avg_txt = TLatex(xmin+1.5, 0.8*ymax, plot_opts.avg_txt.format(xmin))
                # avg_txt.SetNDC()
                avg_txt.SetTextColorAlpha(colors(i, plot_opts.marker_type),1.)
                avg_txt.SetTextSize(0.08)
                avg_txt.SetTextFont(42)
                avg_txt.SetTextAngle(0)
                avg_lines_txt.append(avg_txt)
                # avg_txt.Draw()

        c1.cd()
        if plot_opts.do_ratio and i > 0:
            ratio = h.Clone("ratio")
            ratio.Divide(hlist[0])
            ratio.SetMarkerSize(0.5)

            # ratio.SetLineStyle(lines(i))
            ratio.SetLineStyle(0)
            ratio.SetLineColorAlpha(colors(i, plot_opts.marker_type), 1.0)
            ratio.SetLineWidth(2)
            ratio.SetMarkerSize(1.0)
            ratio.SetMarkerColorAlpha(colors(i, plot_opts.marker_type), 1.0)
            ratio.SetFillStyle(0)
            ratio.SetFillColor(0)

            if plot_opts.set_ratio_min_max:
                ratio.SetMinimum(plot_opts.ratio_min)
                ratio.SetMaximum(plot_opts.ratio_max)

            ratio.SetTitle('')
            ratio.GetXaxis().SetTitle(plot_opts.xtitle)
            ratio.GetYaxis().SetTitle("")
            ratio.GetXaxis().SetLabelSize(.15)
            ratio.GetYaxis().SetLabelSize(.15)
            ratio.GetXaxis().SetLabelOffset(.004)
            ratio.GetYaxis().SetLabelOffset(.009)
            ratio.GetXaxis().SetTitleSize(.16)
            ratio.GetYaxis().SetTitleSize(.16)
            ratio.GetXaxis().SetTitleOffset(1.0)
            ratio.GetYaxis().SetTitleOffset(1.0)
            if plot_opts.x_ndivisions != None:
                ratio.GetXaxis().SetNdivisions(plot_opts.x_ndivisions)
            if plot_opts.y_ndivisions_ratio != None:
                ratio.GetYaxis().SetNdivisions(plot_opts.y_ndivisions_ratio)
            ratio.GetYaxis().SetDecimals(True)
            ratio.GetXaxis().SetDecimals(True)
            ratio.GetXaxis().SetTickLength(.1)
            ratio.GetYaxis().SetTickLength(.03)

            # color_combo = TColor.GetColor("#ee422e")
            #color_combo = TColor.GetColor("#FFCC00")
            color_combo = colors(i, plot_opts.marker_type)
            ratio.SetMarkerColorAlpha(color_combo,0.)
            ratio.SetMarkerStyle(0)
            ratio.SetLineColorAlpha(color_combo,1.)
            ratio.SetLineStyle(1)
            ratio.SetLineWidth(2)
            ratio.SetFillStyle(0)
            ratio.SetFillColorAlpha(color_combo,0.)

            # Tot. uncert.
            ratio2 = ratio.Clone()
            ratio2.SetFillStyle(3356)
            ratio2.SetLineWidth(4)
            ratio2.SetFillColorAlpha(color_combo,1.)
            ratio2.SetMarkerColorAlpha(color_combo,0.)
            ratio2.SetMarkerStyle(0)
            ratio2.SetLineColorAlpha(color_combo,1.)
            ratio2.SetLineStyle(1)
            ratio2.SetLineWidth(2)


            # draw on bottom pad
            pad2.cd()

            if i == 1:
                ratio2.DrawCopy("E2")
                ratio.DrawCopy(plot_opts.draw_style+"same")
            else:
                ratio2.DrawCopy("E2 same")
                ratio.DrawCopy(plot_opts.draw_style+"same")

            if plot_opts.draw_avg_ratio:
                # nbinsx = ratio.GetNbinsX()
                # print ratio.GetNbinsX()
                # print ratio.GetXaxis().GetFirst()
                # print ratio.GetXaxis().GetLast()
                minbin = ratio.GetXaxis().GetFirst()
                maxbin = ratio.GetXaxis().GetLast()
                nbinsx = 0
                binsum = 0
                binsumsq = 0
                binerrsumsq = 0
                for j in range(minbin,maxbin+1):
                    if ratio.GetBinContent(j) != 0:
                        nbinsx += 1
                        binsum += ratio.GetBinContent(j)
                        binsumsq += ratio.GetBinContent(j)**2
                        binerrsumsq += ratio.GetBinError(j)**2
                        # print "j:{}, nbinsx: {:.5f}, binsum: {:.5f}".format(j, nbinsx, binsum)
                # print "After --> j:{}, nbinsx: {:.5f}, binsum: {:.5f}".format(j, nbinsx, binsum)
                if nbinsx != 0:
                    avgratio = binsum/nbinsx
                    # print avgratio
                    avgerr = np.sqrt((binsumsq/nbinsx-avgratio**2)/nbinsx)
                    avgerr2 = np.sqrt(binerrsumsq)/nbinsx
                    toterr = np.sqrt(avgerr**2 + avgerr2**2)
                    if len(plot_opts.avg_ratio_txt) > 0:
                        avg_ratio_txt.append(TLatex(plot_opts.avg_ratio_x+i*0.30, plot_opts.avg_ratio_y, plot_opts.avg_ratio_txt[i-1]+" = {:.4f}#pm{:.4f}".format(avgratio, toterr)))
                    else:
                        avg_ratio_txt.append(TLatex(plot_opts.avg_ratio_x+i*0.30, plot_opts.avg_ratio_y, "#LTMC/Data#GT = {:.4f}#pm{:.4f}".format(avgratio, toterr)))
                    # print avgratio
                    avg_ratio_txt[-1].SetNDC()
                    avg_ratio_txt[-1].SetTextColorAlpha(colors(i, plot_opts.marker_type),1.)
                    avg_ratio_txt[-1].SetTextSize(0.10)
                    avg_ratio_txt[-1].SetTextFont(42)
                    avg_ratio_txt[-1].SetTextAngle(0)
                    # print
                    # print plot_opts.plot_name
                    # print avg_txt
                    avg_ratio_txt[-1].Draw()


        c1.cd()

        # set ratio y label
        if plot_opts.do_ratio and plot_opts.ratio_label != None:
            l = TLatex(0.06, 0.22, plot_opts.ratio_label)
            l.SetNDC()
            l.SetTextSize(0.043)
            l.SetTextFont(42)
            l.SetTextAngle(90)
            l.Draw()

        leg.Draw()
        leg_cuts.Draw()


    pad1.cd()
    for avg_line in avg_lines:
        avg_line.Draw()
    for avg_txt in avg_lines_txt:
        avg_txt.Draw()

    c1.cd()
    draw_atlas_label(plot_opts.atlasx, plot_opts.atlasy, plot_opts.atlas_label)
    if plot_opts.do_data:
        draw_latex(plot_opts.lumix, plot_opts.lumiy, plot_opts.lumi_label, 0.04)

    c1.SaveAs(plot_output_path+".pdf")
    # c1.SaveAs(plot_output_path+".svg")
    # c1.SaveAs(plot_output_path+".eps")
    # c1.SaveAs(plot_output_path+".png")

def save_hist(h, plot_opts, plot_output_path):
    """ save one histogram as pdf and/or svg """

    c1 = setup_canvas("c1", "canvas1",
                     plot_opts.gridx,  plot_opts.gridy,
                     plot_opts.logx, plot_opts.logy, plot_opts.logz,
                     plot_opts.c_widthx, plot_opts.c_widthy)

    h.SetTitle(plot_opts.title)
    h.GetXaxis().SetTitle(plot_opts.xtitle)
    h.GetYaxis().SetTitle(plot_opts.ytitle)

    h.GetXaxis().SetLabelSize(0.05)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetTitleOffset(1.4)
    # h.GetYaxis().SetMoreLogLabels(True);
    # h.GetXaxis().SetMoreLogLabels(True);
    # h.GetYaxis().SetNoExponent(True);
    # h.GetXaxis().SetNoExponent(True);

    if plot_opts.do_custom_bin_labels:
        for j,label in enumerate(plot_opts.custom_bin_labels):
            h.GetXaxis().SetBinLabel(j+1, label)
            h.GetXaxis().LabelsOption("v")

    if (plot_opts.rebin != 0):
        if ("vs" not in plot_output_path):
            h.Rebin(plot_opts.rebin)
        else:
            h.Rebin2D(plot_opts.rebinx,plot_opts.rebiny)

    if plot_opts.profilex:
        h_profile = h.ProfileX()
        h_profile.SetMarkerStyle(20)
        h_profile.SetMarkerSize(1.5)
        h_profile.SetMarkerColor(kBlack)
        h_profile.SetLineColor(kBlack)
        h_profile.SetLineWidth(2)

        h_profile2 = h_profile.Clone()
        h_profile2.SetMarkerStyle(20)
        h_profile2.SetMarkerSize(1.0)
        h_profile2.SetMarkerColor(kWhite)

    # maximum in x
    if (plot_opts.xmax != 0):
        h.GetXaxis().SetRangeUser(plot_opts.xmin, plot_opts.xmax)

    # maximum in y
    if (plot_opts.ymax != 0):
        h.GetYaxis().SetRangeUser(plot_opts.ymin, plot_opts.ymax)

    leg = setup_legend(len(plot_opts.leg_labels)+len(plot_opts.plot_tags), 1,
                        plot_opts.legx, plot_opts.legy,
                        plot_opts.legwx, plot_opts.legwy)

    h.SetLineColor(kRed+1)
    h.SetLineStyle(2)
    h.SetLineWidth(2)
    h.SetFillColor(kRed+1)
    h.SetFillStyle(0)

    h.SetMarkerColor(kRed+1)
    h.SetMarkerStyle(24)
    h.SetMarkerSize(1.5)

    h.SetTitle(plot_opts.title)
    h.GetXaxis().SetTitle(plot_opts.xtitle)
    h.GetYaxis().SetTitle(plot_opts.ytitle)

    for tag in plot_opts.plot_tags:
        leg.AddEntry("NULL", tag, "h")

    if "TH1" in str(type(h)):
        h.Draw("lpE0")
        leg.Draw()
    else:
        h.Draw("COLZ")
        leg.Draw()

    if plot_opts.profilex:
        h_profile.Draw("E same")
        h_profile2.Draw("L same")


    draw_atlas_label(plot_opts.atlasx, plot_opts.atlasy, plot_opts.atlas_label)
    if plot_opts.do_data:
        draw_latex(plot_opts.lumix, plot_opts.lumiy, plot_opts.lumi_label, 0.04)

    c1.SaveAs(plot_output_path+".pdf")
    # c1.SaveAs(plot_output_path+".svg")
    # c1.SaveAs(plot_output_path+".eps")
    # c1.SaveAs(plot_output_path+".png")

