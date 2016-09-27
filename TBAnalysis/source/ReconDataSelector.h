//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Sep 14 11:55:33 2016 by ROOT version 6.06/04
// from TTree h1000/TileBEAM-Ntuple
// found on file: ntuples/recon/tiletb_610629.root
//////////////////////////////////////////////////////////

#ifndef ReconDataSelector_h
#define ReconDataSelector_h

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
#include <vector>

using namespace std;

class ReconDataSelector : public TSelector, HistogramManager {
public :
   TTreeReader     fReader;  //!the tree reader
   TTree          *fChain = 0;   //!pointer to the analyzed TTree or TChain
   //
   // // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<Int_t> EvTime = {fReader, "EvTime"};
   TTreeReaderValue<Int_t> Run = {fReader, "Run"};
   TTreeReaderValue<Int_t> Evt = {fReader, "Evt"};
   TTreeReaderValue<Short_t> Trig = {fReader, "Trig"};
   TTreeReaderValue<Int_t> DSPflags = {fReader, "DSPflags"};
   TTreeReaderValue<Short_t> DSPunits = {fReader, "DSPunits"};
   TTreeReaderValue<Short_t> OFLunits = {fReader, "OFLunits"};
   TTreeReaderArray<int> L1ID = {fReader, "L1ID"};
   TTreeReaderArray<int> L1Type = {fReader, "L1Type"};
   TTreeReaderArray<int> EvType = {fReader, "EvType"};
   TTreeReaderArray<int> EvBCID = {fReader, "EvBCID"};
   TTreeReaderArray<int> FrBCID = {fReader, "FrBCID"};
   TTreeReaderValue<Float_t> MuBackHit = {fReader, "MuBackHit"};
   TTreeReaderValue<Float_t> MuBackSum = {fReader, "MuBackSum"};
   TTreeReaderArray<Float_t> MuBack = {fReader, "MuBack"};
   TTreeReaderArray<Int_t> cispar = {fReader, "cispar"};
   TTreeReaderValue<Short_t> S1cou = {fReader, "S1cou"};
   TTreeReaderValue<Short_t> S2cou = {fReader, "S2cou"};
   TTreeReaderValue<Short_t> S3cou = {fReader, "S3cou"};
   TTreeReaderValue<Short_t> Cher1 = {fReader, "Cher1"};
   TTreeReaderValue<Short_t> Cher2 = {fReader, "Cher2"};
   TTreeReaderValue<Short_t> SCalo1 = {fReader, "SCalo1"};
   TTreeReaderValue<Short_t> SCalo2 = {fReader, "SCalo2"};
   // TTreeReaderArray<Int_t> m_btdc1 = {fReader, "btdc1"};
   TTreeReaderValue<Float_t> Xcha1 = {fReader, "Xcha1"};
   TTreeReaderValue<Float_t> Ycha1 = {fReader, "Ycha1"};
   TTreeReaderValue<Float_t> Xcha2 = {fReader, "Xcha2"};
   TTreeReaderValue<Float_t> Ycha2 = {fReader, "Ycha2"};
   // TTreeReaderValue<Float_t> Ximp = {fReader, "Ximp"};
   // TTreeReaderValue<Float_t> Yimp = {fReader, "Yimp"};
   // TTreeReaderValue<Int_t> EvtA01 = {fReader, "EvtA01"};
   // TTreeReaderValue<Short_t> rodBCIDA01 = {fReader, "rodBCIDA01"};
   // TTreeReaderValue<Short_t> SizeA01 = {fReader, "SizeA01"};
   // TTreeReaderArray<Int_t> bcidA01 = {fReader, "BCIDA01"};
   // TTreeReaderArray<UInt_t> DMUheaderA01 = {fReader, "DMUheaderA01"};
   // TTreeReaderArray<Short_t> DMUformatErrA01 = {fReader, "DMUformatErrA01"};
   // TTreeReaderArray<Short_t> DMUparityErrA01 = {fReader, "DMUparityErrA01"};
   // TTreeReaderArray<Short_t> DMUmemoryErrA01 = {fReader, "DMUmemoryErrA01"};
   // TTreeReaderArray<Short_t> DMUSstrobeErrA01 = {fReader, "DMUSstrobeErrA01"};
   // TTreeReaderArray<Short_t> DMUDstrobeErrA01 = {fReader, "DMUDstrobeErrA01"};
   // TTreeReaderArray<Int_t> dmumaskA01 = {fReader, "DMUMaskA01"};
   // TTreeReaderArray<Int_t> crcA01 = {fReader, "SlinkCRCA01"};
   // TTreeReaderArray<Int_t> gainA01 = {fReader, "GainA01"};
   // TTreeReaderArray<Int_t> fe_crcA01 = {fReader, "feCRCA01"};
   // TTreeReaderArray<Int_t> rod_crcA01 = {fReader, "rodCRCA01"};
   // TTreeReaderArray<Float_t> eOptA01 = {fReader, "EoptA01"};
   // TTreeReaderArray<Float_t> tOptA01 = {fReader, "ToptA01"};
   // TTreeReaderArray<Float_t> pedOptA01 = {fReader, "PedoptA01"};
   // TTreeReaderArray<Float_t> chiOptA01 = {fReader, "Chi2optA01"};
   // TTreeReaderValue<Int_t> EvtA02 = {fReader, "EvtA02"};
   // TTreeReaderValue<Short_t> rodBCIDA02 = {fReader, "rodBCIDA02"};
   // TTreeReaderValue<Short_t> SizeA02 = {fReader, "SizeA02"};
   // TTreeReaderArray<Int_t> bcidA02 = {fReader, "BCIDA02"};
   // TTreeReaderArray<UInt_t> DMUheaderA02 = {fReader, "DMUheaderA02"};
   // TTreeReaderArray<Short_t> DMUformatErrA02 = {fReader, "DMUformatErrA02"};
   // TTreeReaderArray<Short_t> DMUparityErrA02 = {fReader, "DMUparityErrA02"};
   // TTreeReaderArray<Short_t> DMUmemoryErrA02 = {fReader, "DMUmemoryErrA02"};
   // TTreeReaderArray<Short_t> DMUSstrobeErrA02 = {fReader, "DMUSstrobeErrA02"};
   // TTreeReaderArray<Short_t> DMUDstrobeErrA02 = {fReader, "DMUDstrobeErrA02"};
   // TTreeReaderArray<Int_t> dmumaskA02 = {fReader, "DMUMaskA02"};
   // TTreeReaderArray<Int_t> crcA02 = {fReader, "SlinkCRCA02"};
   // TTreeReaderArray<Int_t> gainA02 = {fReader, "GainA02"};
   // TTreeReaderArray<Int_t> fe_crcA02 = {fReader, "feCRCA02"};
   // TTreeReaderArray<Int_t> rod_crcA02 = {fReader, "rodCRCA02"};
   // TTreeReaderArray<Float_t> eOptA02 = {fReader, "EoptA02"};
   // TTreeReaderArray<Float_t> tOptA02 = {fReader, "ToptA02"};
   // TTreeReaderArray<Float_t> pedOptA02 = {fReader, "PedoptA02"};
   // TTreeReaderArray<Float_t> chiOptA02 = {fReader, "Chi2optA02"};
   // TTreeReaderValue<Int_t> EvtC01 = {fReader, "EvtC01"};
   // TTreeReaderValue<Short_t> rodBCIDC01 = {fReader, "rodBCIDC01"};
   // TTreeReaderValue<Short_t> SizeC01 = {fReader, "SizeC01"};
   // TTreeReaderArray<Int_t> bcidC01 = {fReader, "BCIDC01"};
   // TTreeReaderArray<UInt_t> DMUheaderC01 = {fReader, "DMUheaderC01"};
   // TTreeReaderArray<Short_t> DMUformatErrC01 = {fReader, "DMUformatErrC01"};
   // TTreeReaderArray<Short_t> DMUparityErrC01 = {fReader, "DMUparityErrC01"};
   // TTreeReaderArray<Short_t> DMUmemoryErrC01 = {fReader, "DMUmemoryErrC01"};
   // TTreeReaderArray<Short_t> DMUSstrobeErrC01 = {fReader, "DMUSstrobeErrC01"};
   // TTreeReaderArray<Short_t> DMUDstrobeErrC01 = {fReader, "DMUDstrobeErrC01"};
   // TTreeReaderArray<Int_t> dmumaskC01 = {fReader, "DMUMaskC01"};
   // TTreeReaderArray<Int_t> crcC01 = {fReader, "SlinkCRCC01"};
   // TTreeReaderArray<Int_t> gainC01 = {fReader, "GainC01"};
   // TTreeReaderArray<Int_t> fe_crcC01 = {fReader, "feCRCC01"};
   // TTreeReaderArray<Int_t> rod_crcC01 = {fReader, "rodCRCC01"};
   // TTreeReaderArray<Float_t> eOptC01 = {fReader, "EoptC01"};
   // TTreeReaderArray<Float_t> tOptC01 = {fReader, "ToptC01"};
   // TTreeReaderArray<Float_t> pedOptC01 = {fReader, "PedoptC01"};
   // TTreeReaderArray<Float_t> chiOptC01 = {fReader, "Chi2optC01"};
   // TTreeReaderValue<Int_t> EvtC02 = {fReader, "EvtC02"};
   // TTreeReaderValue<Short_t> rodBCIDC02 = {fReader, "rodBCIDC02"};
   // TTreeReaderValue<Short_t> SizeC02 = {fReader, "SizeC02"};
   // TTreeReaderArray<Int_t> bcidC02 = {fReader, "BCIDC02"};
   // TTreeReaderArray<UInt_t> DMUheaderC02 = {fReader, "DMUheaderC02"};
   // TTreeReaderArray<Short_t> DMUformatErrC02 = {fReader, "DMUformatErrC02"};
   // TTreeReaderArray<Short_t> DMUparityErrC02 = {fReader, "DMUparityErrC02"};
   // TTreeReaderArray<Short_t> DMUmemoryErrC02 = {fReader, "DMUmemoryErrC02"};
   // TTreeReaderArray<Short_t> DMUSstrobeErrC02 = {fReader, "DMUSstrobeErrC02"};
   // TTreeReaderArray<Short_t> DMUDstrobeErrC02 = {fReader, "DMUDstrobeErrC02"};
   // TTreeReaderArray<Int_t> dmumaskC02 = {fReader, "DMUMaskC02"};
   // TTreeReaderArray<Int_t> crcC02 = {fReader, "SlinkCRCC02"};
   // TTreeReaderArray<Int_t> gainC02 = {fReader, "GainC02"};
   // TTreeReaderArray<Int_t> fe_crcC02 = {fReader, "feCRCC02"};
   // TTreeReaderArray<Int_t> rod_crcC02 = {fReader, "rodCRCC02"};
   // TTreeReaderArray<Float_t> eOptC02 = {fReader, "EoptC02"};
   // TTreeReaderArray<Float_t> tOptC02 = {fReader, "ToptC02"};
   // TTreeReaderArray<Float_t> pedOptC02 = {fReader, "PedoptC02"};
   // TTreeReaderArray<Float_t> chiOptC02 = {fReader, "Chi2optC02"};
   // TTreeReaderValue<Int_t> EvtE03 = {fReader, "EvtE03"};
   // TTreeReaderValue<Short_t> rodBCIDE03 = {fReader, "rodBCIDE03"};
   // TTreeReaderValue<Short_t> SizeE03 = {fReader, "SizeE03"};
   // TTreeReaderArray<Int_t> bcidE03 = {fReader, "BCIDE03"};
   // TTreeReaderArray<UInt_t> DMUheaderE03 = {fReader, "DMUheaderE03"};
   // TTreeReaderArray<Short_t> DMUformatErrE03 = {fReader, "DMUformatErrE03"};
   // TTreeReaderArray<Short_t> DMUparityErrE03 = {fReader, "DMUparityErrE03"};
   // TTreeReaderArray<Short_t> DMUmemoryErrE03 = {fReader, "DMUmemoryErrE03"};
   // TTreeReaderArray<Short_t> DMUSstrobeErrE03 = {fReader, "DMUSstrobeErrE03"};
   // TTreeReaderArray<Short_t> DMUDstrobeErrE03 = {fReader, "DMUDstrobeErrE03"};
   // TTreeReaderArray<Int_t> dmumaskE03 = {fReader, "DMUMaskE03"};
   // TTreeReaderArray<Int_t> crcE03 = {fReader, "SlinkCRCE03"};
   // TTreeReaderArray<Int_t> gainE03 = {fReader, "GainE03"};
   // TTreeReaderArray<Int_t> fe_crcE03 = {fReader, "feCRCE03"};
   // TTreeReaderArray<Int_t> rod_crcE03 = {fReader, "rodCRCE03"};
   // TTreeReaderArray<Float_t> eOptE03 = {fReader, "EoptE03"};
   // TTreeReaderArray<Float_t> tOptE03 = {fReader, "ToptE03"};
   // TTreeReaderArray<Float_t> pedOptE03 = {fReader, "PedoptE03"};
   // TTreeReaderArray<Float_t> chiOptE03 = {fReader, "Chi2optE03"};

   // // NB! 2D arrays are flattened by TTreeReaderArray
   // TTreeReaderArray<Float_t> SampleA01 = {fReader, "SampleA01"};
   // TTreeReaderArray<Float_t> SampleA02 = {fReader, "SampleA02"};
   // TTreeReaderArray<Float_t> SampleC01 = {fReader, "SampleC01"};
   // TTreeReaderArray<Float_t> SampleC02 = {fReader, "SampleC02"};
   // TTreeReaderArray<Float_t> SampleE03 = {fReader, "SampleE03"};

   ReconDataSelector(TTree * /*tree*/ =0) { }
   virtual ~ReconDataSelector() { }
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

   ClassDef(ReconDataSelector,0);

};

#endif

#ifdef ReconDataSelector_cxx
void ReconDataSelector::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t ReconDataSelector::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}


#endif // #ifdef ReconDataSelector_cxx
