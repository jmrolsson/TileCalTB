#define RawDataSelector_cxx
// The class definition in RawDataSelector.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("RawDataSelector.C")
// root> T->Process("RawDataSelector.C","some options")
// root> T->Process("RawDataSelector.C+")
//


#include "RawDataSelector.h"
#include <TH2.h>
#include <TStyle.h>

void RawDataSelector::Begin(TTree * /*tree*/)
{
  // The Begin() function is called at the start of the query.
  // When running with PROOF Begin() is only called on the client.
  // The tree argument is deprecated (on PROOF 0 is passed).

  int nADC_hi = 200; float minADC_hi = 262; float maxADC_hi = 272;
  int nADC_lo = 200; float minADC_lo = 255; float maxADC_lo = 265;
  int nADC = 200; float minADC = 255; float maxADC = 265;
  int nCH  = 48;  float minCH  = 0;   float maxCH = 47;
  int nDrawer  = 4;  float minDrawer  = 0;   float maxDrawer = 4;

  h_avg_samples_channel_hi = book("h_avg_samples_channel_hi", "avg_samples_channel_hi", "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_avg_samples_channel_lo = book("h_avg_samples_channel_lo", "avg_samples_channel_lo", "adc counts", nADC_lo, minADC_lo, maxADC_lo);

  h_avg_samples_hi_vs_channel = book("h_avg_samples_hi_vs_channel", "avg_samples_hi_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_avg_samples_lo_vs_channel = book("h_avg_samples_lo_vs_channel", "avg_samples_lo_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", nADC_lo, minADC_lo, maxADC_lo);

  h_avg_samples_RMS_channels_hi = book("h_avg_samples_RMS_channels_hi", "avg_samples_RMS_channels_hi", "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_avg_samples_RMS_channels_lo = book("h_avg_samples_RMS_channels_lo", "avg_samples_RMS_channels_lo", "adc counts", nADC_lo, minADC_lo, maxADC_lo);

  h_RMS_samples_hi_vs_channel = book("h_RMS_samples_hi_vs_channel", "RMS_samples_hi_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_RMS_samples_lo_vs_channel = book("h_RMS_samples_lo_vs_channel", "RMS_samples_lo_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", nADC_lo, minADC_lo, maxADC_lo);

  p_RMS_samples_hi_vs_channel = book("p_RMS_samples_hi_vs_channel", "RMS_samples_hi_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", minADC_hi, maxADC_hi);
  p_RMS_samples_lo_vs_channel = book("p_RMS_samples_lo_vs_channel", "RMS_samples_lo_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", minADC_lo, maxADC_lo);

  h_avg_samples_RMS_drawers_hi_vs_drawer = book("h_avg_samples_RMS_drawers_hi_vs_drawer", "avg_samples_RMS_drawers_hi_vs_drawer", "drawer", nDrawer, minDrawer, maxDrawer, "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_avg_samples_RMS_drawers_lo_vs_drawer = book("h_avg_samples_RMS_drawers_lo_vs_drawer", "avg_samples_RMS_drawers_lo_vs_drawer", "drawer", nDrawer, minDrawer, maxDrawer, "adc counts", nADC_lo, minADC_lo, maxADC_lo);

  p_avg_samples_RMS_drawers_hi_vs_drawer = book("p_avg_samples_RMS_drawers_hi_vs_drawer", "p_avg_samples_RMS_drawers_hi_vs_drawer", "drawer", nDrawer, minDrawer, maxDrawer, "adc counts", minADC_hi, maxADC_hi);
  p_avg_samples_RMS_drawers_lo_vs_drawer = book("p_avg_samples_RMS_drawers_lo_vs_drawer", "p_avg_samples_RMS_drawers_lo_vs_drawer", "drawer", nDrawer, minDrawer, maxDrawer, "adc counts", minADC_lo, maxADC_lo);

  h_sigma_channels_hi = book("h_sigma_channels_hi", "sigma_channels_hi", "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_sigma_channels_lo = book("h_sigma_channels_lo", "sigma_channels_lo", "adc counts", nADC_lo, minADC_lo, maxADC_lo);

  h_sigma_samples_hi_vs_channel = book("h_sigma_samples_hi_vs_channel", "sigma_samples_hi_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", nADC_hi, minADC_hi, maxADC_hi);
  h_sigma_samples_lo_vs_channel = book("h_sigma_samples_lo_vs_channel", "sigma_samples_lo_vs_channel", "channel", nCH, minCH, maxCH, "adc counts", nADC_lo, minADC_lo, maxADC_lo);

}

void RawDataSelector::SlaveBegin(TTree * /*tree*/)
{
  // The SlaveBegin() function is called after the Begin() function.
  // When running with PROOF SlaveBegin() is called on each slave server.
  // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

}

Bool_t RawDataSelector::Process(Long64_t entry)
{
  // The Process() function is called for each entry in the tree (or possibly
  // keyed object in the case of PROOF) to be processed. The entry argument
  // specifies which entry in the currently loaded tree is to be processed.
  // When processing keyed objects with PROOF, the object is already loaded
  // and is available via the fObject pointer.
  //
  // This function should contain the \"body\" of the analysis. It can contain
  // simple or elaborate selection criteria, run algorithms on the data
  // of the event and typically fill histograms.
  //
  // The processing can be stopped by calling Abort().
  //
  // Use fStatus to set the return value of TTree::Process().
  //
  // The return value is currently not used.

  fReader.SetEntry(entry);
  /* cout << "entry: " << entry << endl; */
  /* cout << "----> Loop over samples" << endl; */
  if (entry%1000 == 0 && entry>0) 
    cout << "Finished processing " << entry << " events" << endl;

  int sample = 0;
  int channel = 0;
  int drawer = 0;
  int n_samples = 0;
  float sum_samples_hi = 0;
  float sum_samples_lo = 0;
  float sumsq_samples_hi = 0;
  float sumsq_samples_lo = 0;
  float sum_channels_hi = 0;
  float sum_channels_lo = 0;
  float sumsq_channels_hi = 0;
  float sumsq_channels_lo = 0;
  float sumsq_drawers_hi = 0;
  float sumsq_drawers_lo = 0;

  int len = samples_hi.GetSize();
  if (len != samples_lo.GetSize()) {
    cout << "ERROR: samples_hi and samples_low are of different lengths" << endl;
    std::exit(1);
  }
  for (int i=0; i<len; i++) {
    if (samples_hi[i] > 0 && samples_lo[i] > 0) {
      n_samples++;
      sum_samples_hi += samples_hi[i];
      sum_samples_lo += samples_lo[i];
      sumsq_samples_hi += TMath::Power(((float)samples_hi[i]),2);
      sumsq_samples_lo += TMath::Power(((float)samples_lo[i]),2);
    }
    // keep track of the number of samples (128 in ttree) per channel (48)
    sample++;
    if (sample % 127 == 0) {
      // fill histos for samples vs channel
      h_avg_samples_hi_vs_channel -> Fill(channel, sum_samples_hi/n_samples);
      h_avg_samples_lo_vs_channel -> Fill(channel, sum_samples_lo/n_samples);
      h_RMS_samples_hi_vs_channel -> Fill(channel, TMath::Sqrt((float)sumsq_samples_hi/n_samples));
      h_RMS_samples_lo_vs_channel -> Fill(channel, TMath::Sqrt((float)sumsq_samples_lo/n_samples));
      p_RMS_samples_hi_vs_channel -> Fill(channel, TMath::Sqrt((float)sumsq_samples_hi/n_samples));
      p_RMS_samples_lo_vs_channel -> Fill(channel, TMath::Sqrt((float)sumsq_samples_lo/n_samples));
      // take the average of the samples in each channel
      sum_channels_hi += sum_samples_hi/n_samples;
      sum_channels_lo += sum_samples_lo/n_samples;
      sumsq_channels_hi += TMath::Power((float)sum_samples_hi/n_samples,2);
      sumsq_channels_lo += TMath::Power((float)sum_samples_lo/n_samples,2);
      sumsq_drawers_hi += TMath::Power((float)sum_samples_hi/n_samples,2);
      sumsq_drawers_lo += TMath::Power((float)sum_samples_lo/n_samples,2);
      // reset samples for next channel
      n_samples = 0;
      sum_samples_hi = 0;
      sum_samples_lo = 0;
      sumsq_samples_hi = 0;
      sumsq_samples_lo = 0;
      sample = 0;
      if ((channel+1) % 12 == 0) {
        h_avg_samples_RMS_drawers_hi_vs_drawer -> Fill(drawer, TMath::Sqrt((float)sumsq_drawers_hi/12));
        h_avg_samples_RMS_drawers_lo_vs_drawer -> Fill(drawer, TMath::Sqrt((float)sumsq_drawers_lo/12));
        p_avg_samples_RMS_drawers_hi_vs_drawer -> Fill(drawer, TMath::Sqrt((float)sumsq_drawers_hi/12));
        p_avg_samples_RMS_drawers_lo_vs_drawer -> Fill(drawer, TMath::Sqrt((float)sumsq_drawers_lo/12));
        sumsq_drawers_hi = 0;
        sumsq_drawers_lo = 0;
        drawer++;
      }
      channel++;
    }
  }

  h_avg_samples_channel_hi -> Fill(sum_channels_hi/48);
  h_avg_samples_channel_lo -> Fill(sum_channels_lo/48);
  h_avg_samples_RMS_channels_hi -> Fill(TMath::Sqrt(sumsq_channels_hi/48));
  h_avg_samples_RMS_channels_lo -> Fill(TMath::Sqrt(sumsq_channels_lo/48));

  return kTRUE;
}

void RawDataSelector::SlaveTerminate()
{
  // The SlaveTerminate() function is called after all entries or objects
  // have been processed. When running with PROOF SlaveTerminate() is called
  // on each slave server.

}

void RawDataSelector::Terminate()
{
  // The Terminate() function is the last function to be called during
  // a query. It always runs on the client, it can be used to present
  // the results graphically or save the results to file.

  if (fOption != NULL)
    SaveHistsToFile(fOption);
}
