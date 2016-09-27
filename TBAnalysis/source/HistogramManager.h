#ifndef HistogramManager_h
#define HistogramManager_h

/** @file HistogramManager.h
 *  @brief Manage your histograms
 *  @author Code from xAH, see https://github.com/UCATLAS/xAODAnaHelpers
 *  @bug No known bugs
 */

#include <iostream>
#include <string>
#include <ctype.h>
#include <TH1.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TH3F.h>
#include <TProfile.h>
#include <TFile.h>

/**
    @brief This is used by any class extending to pre-define a set of histograms to book by default.
    @rst
        .. note:: The expectation is that the user does not directly use this class but rather inherits from it.

    @endrst
 */
class HistogramManager {

  public:
    HistogramManager(std::string name = "", std::string detailStr = "");
    virtual ~HistogramManager();

  protected:
    /** @brief generically the main name assigned to all histograms */
    std::string m_name;
    /** @brief a detail level in the form of a string */
    std::string m_detailStr;
    /** @brief a container holding all generated histograms */
    std::vector< TH1* > m_allHists; 

  public:

    TH1F* book(std::string name, std::string title,
               std::string xlabel, int xbins, double xlow, double xhigh);

    /**
     * @overload
     */
    TH2F* book(std::string name, std::string title,
               std::string xlabel, int xbins, double xlow, double xhigh,
               std::string xyabel, int ybins, double ylow, double yhigh);

    /**
     * @overload
     */
    TH3F* book(std::string name, std::string title,
               std::string xlabel, int xbins, double xlow, double xhigh,
               std::string ylabel, int ybins, double ylow, double yhigh,
               std::string zlabel, int zbins, double zlow, double zhigh);

    /**
     * @overload
     */
    TH1F* book(std::string name, std::string title,
               std::string xlabel, int xbins, const Double_t* xbinsArr);

    /**
     * @overload
     */
    TH2F* book(std::string name, std::string title,
               std::string xlabel, int xbins, const Double_t* xbinsArr,
               std::string ylabel, int ybins, double ylow, double yhigh);

    /**
     * @overload
     */
    TH2F* book(std::string name, std::string title,
               std::string xyabel, int xbins, double xlow, double xhigh,
               std::string ylabel, int ybins, const Double_t* ybinsArr);

    /**
     * @overload
     */
    TH2F* book(std::string name, std::string title,
               std::string xyabel, int xbins, const Double_t* xbinsArr,
               std::string ylabel, int ybins, const Double_t* ybinsArr);

    /**
     * @overload
     */
    TH3F* book(std::string name, std::string title,
               std::string xlabel, int xbins, const Double_t* xbinsArr,
               std::string ylabel, int ybins, const Double_t* ybinsArr,
               std::string zlabel, int zbins, const Double_t* zbinsArr);

    /**
     * @overload
     */
    TProfile* book(std::string name, std::string title,
		   std::string xlabel, int xbins, double xlow, double xhigh,
		   std::string ylabel, double ylow, double yhigh, 
		   std::string option = "");

    /**
     * @brief save all histograms from HistogramManager#m_allHists to an output file
     * @param filename Name of output root file 
     */
    void SaveHistsToFile(TString filename); 

    /**
     * @brief Print a list of all histograms currently stored in HistogramManager#m_allHists
     */
    void PrintHistsList(); 

    /**
     * @brief save all histograms from HistogramManager#m_allHists to an output file 
     */
    // void save_to_file(TFile *f);

  private:
    /**
     * @brief Turn on Sumw2 for the histogram
     *
     * @param hist      The histogram to modify
     * @param flag      Pass in whether to turn on Sumw2 or not
     */
    void Sumw2(TH1* hist, bool flag=true);

    /**
     * @brief Push the new histogram to HistogramManager#m_allHists
     */
    void record(TH1* hist);

    /**
     * @brief Set the labels on a histogram
     *
     * @param hist      The histogram to set the labels on
     * @param xlabel    The xlabel to set
     * @param ylabel    The ylabel to set
     * @param zlabel    The zlabel to set
     */
    void SetLabel(TH1* hist, std::string xlabel);
    /**
     * @overload
     */
    void SetLabel(TH1* hist, std::string xlabel, std::string ylabel);
    /**
     * @overload
     */
    void SetLabel(TH1* hist, std::string xlabel, std::string ylabel, std::string zlabel);

};

#endif
