#ifndef HistogramManager_cxx
#define HistogramManager_cxx

#include "HistogramManager.h"

/* constructors and destructors */
HistogramManager::HistogramManager(std::string name, std::string detailStr):
  m_name(name),
  m_detailStr(detailStr)
{

  // if last character of name is a alphanumeric add a / so that
  // in the output file, a TDirectory is created with the histograms inside
  if( isalnum( m_name.back() ) && !ispunct( m_name.back() ) ) {
    m_name += "/";
    //Info("HistogramManager()", "Adding slash to put hists in TDirectories: %s",m_name.c_str());
  }

}

HistogramManager::~HistogramManager() {

  for( auto hist : m_allHists ){
    delete hist;
  }
}

/* Main book() functions for 1D, 2D, 3D histograms */
TH1F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, double xlow, double xhigh)
{
  TH1F* tmp = new TH1F(name.c_str(), title.c_str(), xbins, xlow, xhigh);
  SetLabel(tmp, xlabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TH2F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, double xlow, double xhigh,
                             std::string ylabel, int ybins, double ylow, double yhigh)
{
  TH2F* tmp = new TH2F(name.c_str(), title.c_str(), xbins, xlow, xhigh, ybins, ylow, yhigh);
  SetLabel(tmp, xlabel, ylabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TH3F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, double xlow, double xhigh,
                             std::string ylabel, int ybins, double ylow, double yhigh,
                             std::string zlabel, int zbins, double zlow, double zhigh)
{
  TH3F* tmp = new TH3F(name.c_str(), title.c_str(), xbins, xlow, xhigh, ybins, ylow, yhigh, zbins, zlow, zhigh);
  SetLabel(tmp, xlabel, ylabel, zlabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TProfile* HistogramManager::book(std::string name, std::string title,
				 std::string xlabel, int xbins, double xlow, double xhigh,
				 std::string ylabel, double ylow, double yhigh, 
				 std::string option)
{
  TProfile* tmp = new TProfile(name.c_str(), title.c_str(), xbins, xlow, xhigh, ylow, yhigh, option.c_str());
  SetLabel(tmp, xlabel, ylabel);
  //this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}


/////// Variable Binned Histograms ///////
TH1F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, const Double_t* xbinArr)
{
  TH1F* tmp = new TH1F(name.c_str(), title.c_str(), xbins, xbinArr);
  SetLabel(tmp, xlabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TH2F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, const Double_t* xbinArr,
                             std::string ylabel, int ybins, double ylow, double yhigh)
{
  TH2F* tmp = new TH2F(name.c_str(), title.c_str(), xbins, xbinArr, ybins, ylow, yhigh);
  SetLabel(tmp, xlabel, ylabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TH2F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, double xlow, double xhigh,
                             std::string ylabel, int ybins, const Double_t* ybinArr)
{
  TH2F* tmp = new TH2F(name.c_str(), title.c_str(), xbins, xlow, xhigh, ybins, ybinArr);
  SetLabel(tmp, xlabel, ylabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TH2F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, const Double_t* xbinArr,
                             std::string ylabel, int ybins, const Double_t* ybinArr)
{
  TH2F* tmp = new TH2F(name.c_str(), title.c_str(), xbins, xbinArr, ybins, ybinArr);
  SetLabel(tmp, xlabel, ylabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

TH3F* HistogramManager::book(std::string name, std::string title,
                             std::string xlabel, int xbins, const Double_t* xbinArr,
                             std::string ylabel, int ybins, const Double_t* ybinArr,
                             std::string zlabel, int zbins, const Double_t* zbinArr)
{
  TH3F* tmp = new TH3F(name.c_str(), title.c_str(), xbins, xbinArr, ybins, ybinArr, zbins, zbinArr);
  SetLabel(tmp, xlabel, ylabel, zlabel);
  this->Sumw2(tmp);
  this->record(tmp);
  return tmp;
}

/* Helper functions */
void HistogramManager::Sumw2(TH1* hist, bool flag /*=true*/) {
  hist->Sumw2(flag);
}

void HistogramManager::record(TH1* hist) {
  m_allHists.push_back( hist );
}

void HistogramManager::SaveHistsToFile(TString filename) {
  TFile *f = new TFile(filename.Data(), "RECREATE");
  for( auto hist : m_allHists ){
    hist->Write();
  }
  f->Close();
  delete f;
}

void HistogramManager::PrintHistsList() {
  std::cout << "List of current histograms: " << std::endl;
  for( auto hist : m_allHists ){
    std::cout << hist->GetTitle() << std::endl;
  }
}

void HistogramManager::SetLabel(TH1* hist, std::string xlabel)
{
  hist->GetXaxis()->SetTitle(xlabel.c_str());
}

void HistogramManager::SetLabel(TH1* hist, std::string xlabel, std::string ylabel)
{
  hist->GetYaxis()->SetTitle(ylabel.c_str());
  this->SetLabel(hist, xlabel);
}

void HistogramManager::SetLabel(TH1* hist, std::string xlabel, std::string ylabel, std::string zlabel)
{
  hist->GetZaxis()->SetTitle(zlabel.c_str());
  this->SetLabel(hist, xlabel, ylabel);
}

#endif
