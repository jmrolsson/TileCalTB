//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Aug 30 10:42:09 2016 by ROOT version 6.06/04
// from TTree dataTree/dataTree
// found on file: Data_20160000000000_testbeam_610611.root
//////////////////////////////////////////////////////////

#ifndef RawDataSelector_h
#define RawDataSelector_h

#include <TROOT.h>
#include <TChain.h>
#include <TMath.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "HistogramManager.h"

// Headers needed by this particular selector

using namespace std;


class RawDataSelector : public TSelector, HistogramManager {

public :

   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain = 0;   //!pointer to the analyzed TTree or TChain

   // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<UInt_t> run = {fReader, "run"};
   TTreeReaderValue<UInt_t> runType = {fReader, "runType"};
   TTreeReaderValue<UInt_t> moduleID = {fReader, "moduleID"};
   TTreeReaderValue<UInt_t> BCID = {fReader, "BCID"};
   TTreeReaderValue<UInt_t> L1ID = {fReader, "L1ID"};
   TTreeReaderValue<Int_t> evt = {fReader, "evt"};
   TTreeReaderValue<Int_t> evtime = {fReader, "evtime"};
   TTreeReaderValue<Int_t> cap = {fReader, "cap"};
   TTreeReaderValue<Int_t> charge = {fReader, "charge"};
   TTreeReaderArray<Int_t> ped_hi = {fReader, "ped_hi"};
   TTreeReaderArray<Int_t> ped_lo = {fReader, "ped_lo"};
   TTreeReaderArray<Int_t> samples_hi = {fReader, "samples_hi"};
   TTreeReaderArray<Int_t> samples_lo = {fReader, "samples_lo"};


   RawDataSelector(TTree * /*tree*/ =0) { }
   virtual ~RawDataSelector() { }
   virtual Int_t   Version() const { return 2; }
   virtual void    Begin(TTree *tree);
   virtual void    SlaveBegin(TTree *tree);
   virtual void    Init(TTree *tree);
   virtual Bool_t  Notify();
   virtual Bool_t  Process(Long64_t entry);
   virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void    SetOption(const char *option) { fOption = option; }
   virtual void    SetObject(TObject *obj) { fObject = obj; }
   virtual void    SetInputList(TList *input) { fInput = input; }
   virtual TList  *GetOutputList() const { return fOutput; }
   virtual void    SlaveTerminate();
   virtual void    Terminate();

   // Histograms
   TH1F *h_avg_samples_channel_hi;
   TH1F *h_avg_samples_channel_lo;
   TH2F *h_avg_samples_hi_vs_channel;
   TH2F *h_avg_samples_lo_vs_channel;
   TH1F *h_avg_samples_RMS_channels_hi;
   TH1F *h_avg_samples_RMS_channels_lo;
   TH2F *h_RMS_samples_hi_vs_channel;
   TH2F *h_RMS_samples_lo_vs_channel;
   TProfile *p_RMS_samples_hi_vs_channel;
   TProfile *p_RMS_samples_lo_vs_channel;
   TH2F *h_avg_samples_RMS_drawers_hi_vs_drawer;
   TH2F *h_avg_samples_RMS_drawers_lo_vs_drawer;
   TProfile *p_avg_samples_RMS_drawers_hi_vs_drawer;
   TProfile *p_avg_samples_RMS_drawers_lo_vs_drawer;
   TH1F *h_sigma_channels_hi;
   TH1F *h_sigma_channels_lo;
   TH2F *h_sigma_samples_hi_vs_channel;
   TH2F *h_sigma_samples_lo_vs_channel;

   ClassDef(RawDataSelector,0);


};

#endif

#ifdef RawDataSelector_cxx
void RawDataSelector::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t RawDataSelector::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}


#endif // #ifdef RawDataSelector_cxx
