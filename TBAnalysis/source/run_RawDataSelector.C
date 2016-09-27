#include <iostream>
#include <TString.h>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "RawDataSelector.h"

/* int run_RawDataSelector() */
int main(int argc, char* argv[])
{
  TString input_file = "/Users/joakim/GoogleDrive/CERN/TileCal-TestBeams/TestBeamAnalysis/ntuples/raw/Data_20160000000000_testbeam_610611.root";
  TString treename = "dataTree";
  TChain *chain = new TChain(treename.Data());
  chain->Add(input_file.Data());
  /* chain->Print();  */
  gROOT->ProcessLine(".L HistogramManager.C");
  /* chain->Process("RawDataSelector.C", "", 1, 1); */
  chain->Process("RawDataSelector.C", "");
  std::cout << "Finished!" << std::endl;

  return 0;
}

//// g++ -o run_RawDataSelector run_RawDataSelector.C `root-config --cflags --glibs`
