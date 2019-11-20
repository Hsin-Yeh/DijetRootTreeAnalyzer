#ifndef analysisClass_h
#define analysisClass_h

#include "baseClass.h"
#include <iostream>
#include <string>
#include <fstream>
#include <stdio.h>
#include <iomanip>
#include <memory>

#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/Selector.hh"
#include "fastjet/PseudoJet.hh"

#include <boost/shared_ptr.hpp>

#include "IOV.h" // For interval-of-validity JEC

// typedefs
typedef boost::shared_ptr<fastjet::ClusterSequence>  ClusterSequencePtr;
typedef boost::shared_ptr<fastjet::JetDefinition>    JetDefPtr;
// For JECs
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"

using namespace std;

class analysisClass : public baseClass {
public :
  analysisClass(string * inputList, string * cutFile, string * treeName,  string *outputFileName=0, string * cutEfficFile=0);
  virtual ~analysisClass();
  void Loop();
private :
  double bTagEventWeight(const vector<double>& SFsForBTaggedJets, const unsigned int nBTags);
  void fillTriggerPlots(TH1F* h_mjj_HLTpass[], double MJJWide);

  ClusterSequencePtr  fjClusterSeq, fjClusterSeq_shift;
  JetDefPtr           fjJetDefinition;
  // For JECs
  JetCorrectorParameters *L1Par;
  JetCorrectorParameters *L2Par;
  JetCorrectorParameters *L3Par;
  JetCorrectorParameters *L1DATAPar;
  JetCorrectorParameters *L2DATAPar;
  JetCorrectorParameters *L3DATAPar;
  JetCorrectorParameters *L2L3Residual;
  JetCorrectorParameters *L1DATAHLTPar;
  JetCorrectorParameters *L2DATAHLTPar;
  JetCorrectorParameters *L3DATAHLTPar;
  JetCorrectorParameters *L2L3ResidualHLT;
  FactorizedJetCorrector *JetCorrector;
  FactorizedJetCorrector *JetCorrector_data;
  FactorizedJetCorrector *JetCorrector_dataHLT;
  JetCorrectionUncertainty *unc;
  BTagCalibration        *bcalib94XDeepCSV;
  BTagCalibration        *bcalib94XCSVv2;
  BTagCalibration        *bcalib94XDeepJet;

  BTagCalibrationReader  *breader_Bloose_CSVv294X;
  BTagCalibrationReader  *breader_Bmedium_CSVv294X;
  BTagCalibrationReader  *breader_Btight_CSVv294X;
  BTagCalibrationReader  *breader_Bloose_DeepCSV94X;
  BTagCalibrationReader  *breader_Bmedium_DeepCSV94X;
  BTagCalibrationReader  *breader_Btight_DeepCSV94X;

  BTagCalibrationReader  *breader_Cloose_CSVv294X;
  BTagCalibrationReader  *breader_Cmedium_CSVv294X;
  BTagCalibrationReader  *breader_Ctight_CSVv294X;
  BTagCalibrationReader  *breader_Cloose_DeepCSV94X;
  BTagCalibrationReader  *breader_Cmedium_DeepCSV94X;
  BTagCalibrationReader  *breader_Ctight_DeepCSV94X;

  BTagCalibrationReader  *breader_Bloose_DeepJet94X;
  BTagCalibrationReader  *breader_Bmedium_DeepJet94X;
  BTagCalibrationReader  *breader_Btight_DeepJet94X;
  BTagCalibrationReader  *breader_Cloose_DeepJet94X;
  BTagCalibrationReader  *breader_Cmedium_DeepJet94X;
  BTagCalibrationReader  *breader_Ctight_DeepJet94X;

  jec::IOV *iov;
};

#endif

#ifdef analysisClass_cxx

#endif // #ifdef analysisClass_cxx
