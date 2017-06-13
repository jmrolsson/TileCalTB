#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
# sns.set_style("darkgrid")
sns.set_style("whitegrid")

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

def main():

    ns=1e9

    # Plot scope trace of trigger (after 'AND' gate), gate, L1 trigger, and extra delay window
    trig_t, trig_x = np.loadtxt('C1-scope_trig_gate_L1trig_busy.txt', skiprows=5, delimiter=',', unpack=True)
    gate_t, gate_x = np.loadtxt('C2-scope_trig_gate_L1trig_busy.txt', skiprows=5, delimiter=',', unpack=True)
    L1trig_t, L1trig_x = np.loadtxt('C3-scope_trig_gate_L1trig_busy.txt', skiprows=5, delimiter=',', unpack=True)
    window_t, window_x = np.loadtxt('C3window00000.txt', skiprows=5, delimiter=',', unpack=True)
    busy_t, busy_x = np.loadtxt('C4-scope_trig_gate_L1trig_busy.txt', skiprows=5, delimiter=',', unpack=True)

    trig_x = trig_x - np.amax(trig_x) + 0.7
    gate_x = gate_x - np.amax(gate_x) + 0.5
    L1trig_x = L1trig_x - np.amax(L1trig_x) + 0.3
    window_x = window_x - np.amax(window_x) + 0.1
    busy_x = busy_x - np.amax(busy_x)

    shift = 920/ns
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.plot((trig_t+shift)*ns, trig_x, markersize=2, label='Trigger')
    ax1.plot((gate_t+shift)*ns, gate_x, markersize=2, label='Gate (ADC)')
    ax1.plot((L1trig_t+shift)*ns, L1trig_x, markersize=2, label='LEVEL 1 Trigger (LTP)')
    ax1.plot((busy_t+shift)*ns, window_x, markersize=2, label='Extra time window')
    ax1.plot((busy_t+shift)*ns, busy_x, markersize=2, label='Busy')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax1.set_xlabel('Time [ns]')
    # ax1.set_ylabel('Amplitude [V]')
    ax1.set_xlim([0, 1000])
    ax1.set_xticks(np.arange(0,1000,100))
    ax1.get_yaxis().set_visible(False)
    handles, labels = ax1.get_legend_handles_labels()
    lgd = ax1.legend(handles, labels, bbox_to_anchor=(1.3,1.0))
    fig1.savefig('scope_trig_gate_L1trig_window_busy.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig1.savefig('scope_trig_gate_L1trig_window_busy.png', dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

    # Plot scope trace of S1, Cher2, trigger (after 'AND' gate), gate
    s1_t, s1_x = np.loadtxt('C1-scope_s1_cher2_trig_gate.txt', skiprows=5, delimiter=',', unpack=True)
    s1_delay_t, s1_delay_x = np.loadtxt('C2-scope_s1_cher2_trig_gate.txt', skiprows=5, delimiter=',', unpack=True)
    trig_t, trig_x = np.loadtxt('C3-scope_s1_cher2_trig_gate.txt', skiprows=5, delimiter=',', unpack=True)
    gate_t, gate_x = np.loadtxt('C4-scope_s1_cher2_trig_gate.txt', skiprows=5, delimiter=',', unpack=True)

    s1_x = s1_x - np.amax(s1_x) + 0.5
    s1_delay_x = s1_delay_x - np.amax(s1_delay_x) + 0.3
    trig_x = trig_x - np.amax(trig_x) + 0.2
    gate_x = gate_x - np.amax(gate_x)

    shift = 50/ns
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1,1,1)
    ax2.plot((s1_t+shift)*ns, s1_x, markersize=2, label='S1')
    ax2.plot((s1_delay_t+shift)*ns, s1_delay_x, markersize=2, label='Cherenkov 2')
    ax2.plot((trig_t+shift)*ns, trig_x, markersize=2, label='Trigger')
    ax2.plot((gate_t+shift)*ns, gate_x, markersize=2, label='Gate (ADC)')
    ax2.set_xlabel('Time [ns]')
    # ax2.set_ylabel('Amplitude [V]')
    ax2.set_xlim([0, 500])
    ax2.set_xticks(np.arange(0,500,50))
    ax2.get_yaxis().set_visible(False)
    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, bbox_to_anchor=(1.21,1.0))
    fig2.savefig('scope_s1_cher2_trig_gate.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig2.savefig('scope_s1_cher2_trig_gate.png', dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

if __name__ == '__main__':
    main()
