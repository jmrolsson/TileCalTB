#! /usr/bin/env python
import numpy as np
from ROOT import TH1F, TH2F

from plot_tools.histogramming import HistogramManager

def process_events(samples, tag = '', options = {}, debug = 0):

    do_avg_sample = False
    if 'do_avg_sample' in options:
        do_avg_sample = options['do_avg_sample']

    nevents = len(samples)
    nchannels = len(samples[0][0])
    nsamples = len([sample for sample in samples[0][0][0] if sample>0])

    if debug:
        if tag != '':
            print 'Tag: ' + tag
        print('Number of events: {}'.format(nevents))
        print('Number of channels: {}'.format(nchannels))
        print('Number of samples: {}'.format(nsamples))

    # Initialize histograms
    n_adc = 500;         min_adc = 0;       max_adc = 500;
    n_ch  = 48;          min_ch  = 0;         max_ch = 47;
    n_drawer = 4;        min_drawer  = 0;     max_drawer = 4;

    hm = HistogramManager(tag)
    hm.add_h2('first_sample_vs_channel', 'adc counts', n_ch, min_ch, max_ch, n_adc, min_adc, max_adc)
    hm.add_h1('avg_channel_first_samples', 'adc counts', n_adc, min_adc, max_adc)
    hm.add_h1('rms_channel_first_samples', 'adc counts', n_adc, min_adc, max_adc)
    if do_avg_sample:
        hm.add_h2('avg_sample_vs_channel', 'adc counts', n_ch, min_ch, max_ch, n_adc, min_adc, max_adc)
        hm.add_h1('avg_channel_avg_samples', 'adc counts', n_adc, min_adc, max_adc)
        hm.add_h1('rms_channel_avg_samples', 'adc counts', n_adc, min_adc, max_adc)

    for evt in xrange(nevents):
        samples_evt = samples[evt][0]

        avg_ch_1st_samp = 0
        rms_ch_1st_samp = 0
        if do_avg_sample:
            avg_ch_avg_samp = 0
            rms_ch_avg_samp = 0

        if debug == 2:
            print('\n ---> Event: {}'.format(evt))
            print(samples_evt)

        for ch in xrange(nchannels):
            samples_ch = samples_evt[ch]
            avg_samples = 0
            for i in xrange(nsamples):
                avg_samples += samples_ch[i]
            avg_samples /= nsamples

            avg_ch_1st_samp += samples_ch[0]
            rms_ch_1st_samp += samples_ch[0]**2
            if do_avg_sample:
                avg_ch_avg_samp += avg_samples
                rms_ch_avg_samp += avg_samples**2

            if debug == 3:
                print('--> Channel: {}'.format(ch))
                print(samples_ch)

            if debug == 4:
                printstr = 'samples = ['
                for i in xrange(nsamples):
                    printstr += ' {}'.format(samples_ch[i])
                    printstr += ']'
                    print printstr

        avg_ch_1st_samp /= nchannels
        rms_ch_1st_samp = np.sqrt(rms_ch_1st_samp/nchannels)
        hm.fill_1d('avg_channel_first_samples', avg_ch_1st_samp)
        hm.fill_1d('rms_channel_first_samples', avg_ch_1st_samp)

        if do_avg_sample:
            avg_ch_avg_samp /= nchannels
            rms_ch_avg_samp = np.sqrt(rms_ch_avg_samp/nchannels)
            hm.fill_1d('avg_channel_avg_samples', avg_ch_avg_samp)
            hm.fill_1d('rms_channel_avg_samples', avg_ch_avg_samp)

    return hm.hists
