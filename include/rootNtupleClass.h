//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Dec 28 11:34:16 2020 by ROOT version 6.22/06
// from TChain HighMassDiphoton/
//////////////////////////////////////////////////////////

#ifndef rootNtupleClass_h
#define rootNtupleClass_h

//// Lines added by make_rootNtupleClass.sh - BEGIN 
#include <vector> 
using namespace std; 
//// Lines added by make_rootNtupleClass.sh - END 

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class rootNtupleClass {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Long64_t        run;
   Long64_t        LS;
   Long64_t        evnum;
   Long64_t        processid;
   Long64_t        bx;
   Long64_t        orbit;
   Float_t         ptHat;
   Float_t         alphaqcd;
   Float_t         alphaqed;
   Float_t         qscale;
   Float_t         x1;
   Float_t         x2;
   Float_t         pdf1;
   Float_t         pdf2;
   Float_t         weight0;
   Float_t         weight;
   Float_t         weightPuUp;
   Float_t         weightPu;
   Float_t         weightPuDown;
   Float_t         weightLumi;
   Float_t         weightAll;
   Int_t           interactingParton1PdgId;
   Int_t           interactingParton2PdgId;
   Int_t           pdf_id1;
   Int_t           pdf_id2;
   Int_t           npv_true ;
   Int_t           beamHaloIDLoose;
   Int_t           beamHaloIDTight;
   Int_t           beamHaloIDTight2015;
   Double_t        mgg;
   Double_t        qt;
   Double_t        deltaPhi;
   Double_t        deltaEta;
   Double_t        deltaR;
   Double_t        cosThetaStar;
   Double_t        cosThetaStar_old;
   Double_t        chiDiphoton;
   Bool_t          isEBEB;
   Bool_t          isEBEE;
   Bool_t          isEEEB;
   Bool_t          isEEEE;
   Double_t        mggGen;
   Double_t        Genqt;
   Double_t        GendeltaPhi;
   Double_t        GendeltaEta;
   Double_t        GendeltaR;
   Double_t        GencosThetaStar;
   Double_t        GencosThetaStar_old;
   Double_t        GenchiDiphoton;
   Bool_t          GenisEBEB;
   Bool_t          GenisEBEE;
   Bool_t          GenisEEEB;
   Bool_t          GenisEEEE;
   Int_t           eventClass;

   // List of branches
   TBranch        *b_run;   //!
   TBranch        *b_LS;   //!
   TBranch        *b_evnum;   //!
   TBranch        *b_processid;   //!
   TBranch        *b_bx;   //!
   TBranch        *b_orbit;   //!
   TBranch        *b_ptHat;   //!
   TBranch        *b_alphaqcd;   //!
   TBranch        *b_alphaqed;   //!
   TBranch        *b_qscale;   //!
   TBranch        *b_x1;   //!
   TBranch        *b_x2;   //!
   TBranch        *b_pdf1;   //!
   TBranch        *b_pdf2;   //!
   TBranch        *b_weight0;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_weightPuUp;   //!
   TBranch        *b_weightPu;   //!
   TBranch        *b_weightPuDown;   //!
   TBranch        *b_weightLumi;   //!
   TBranch        *b_weightAll;   //!
   TBranch        *b_interactingParton1PdgId;   //!
   TBranch        *b_interactingParton2PdgId;   //!
   TBranch        *b_pdf_id1;   //!
   TBranch        *b_pdf_id2;   //!
   TBranch        *b_npv_true;   //!
   TBranch        *b_beamHaloIDLoose;   //!
   TBranch        *b_beamHaloIDTight;   //!
   TBranch        *b_beamHaloIDTight2015;   //!
   TBranch        *b_mgg;   //!
   TBranch        *b_qt;   //!
   TBranch        *b_deltaPhi;   //!
   TBranch        *b_deltaEta;   //!
   TBranch        *b_deltaR;   //!
   TBranch        *b_cosThetaStar;   //!
   TBranch        *b_cosThetaStar_old;   //!
   TBranch        *b_chiDiphoton;   //!
   TBranch        *b_isEBEB;   //!
   TBranch        *b_isEBEE;   //!
   TBranch        *b_isEEEB;   //!
   TBranch        *b_isEEEE;   //!
   TBranch        *b_mggGen;   //!
   TBranch        *b_Genqt;   //!
   TBranch        *b_GendeltaPhi;   //!
   TBranch        *b_GendeltaEta;   //!
   TBranch        *b_GendeltaR;   //!
   TBranch        *b_GencosThetaStar;   //!
   TBranch        *b_GencosThetaStar_old;   //!
   TBranch        *b_GenchiDiphoton;   //!
   TBranch        *b_GenisEBEB;   //!
   TBranch        *b_GenisEBEE;   //!
   TBranch        *b_GenisEEEB;   //!
   TBranch        *b_GenisEEEE;   //!
   TBranch        *b_eventClass;   //!

   rootNtupleClass(TTree *tree=0);
   virtual ~rootNtupleClass();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef rootNtupleClass_cxx
rootNtupleClass::rootNtupleClass(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {

#ifdef SINGLE_TREE
      // The following code should be used if you want this class to access
      // a single tree instead of a chain
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("Memory Directory");
      if (!f || !f->IsOpen()) {
         f = new TFile("Memory Directory");
      }
      f->GetObject("HighMassDiphoton",tree);

#else // SINGLE_TREE

      // The following code should be used if you want this class to access a chain
      // of trees.
      TChain * chain = new TChain("HighMassDiphoton","");
      chain->Add("../../diphoton-analysis/input/trees/data_2017.root/HighMassDiphoton");
      tree = chain;
#endif // SINGLE_TREE

   }
   Init(tree);
}

rootNtupleClass::~rootNtupleClass()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t rootNtupleClass::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t rootNtupleClass::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void rootNtupleClass::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("LS", &LS, &b_LS);
   fChain->SetBranchAddress("evnum", &evnum, &b_evnum);
   fChain->SetBranchAddress("processid", &processid, &b_processid);
   fChain->SetBranchAddress("bx", &bx, &b_bx);
   fChain->SetBranchAddress("orbit", &orbit, &b_orbit);
   fChain->SetBranchAddress("ptHat", &ptHat, &b_ptHat);
   fChain->SetBranchAddress("alphaqcd", &alphaqcd, &b_alphaqcd);
   fChain->SetBranchAddress("alphaqed", &alphaqed, &b_alphaqed);
   fChain->SetBranchAddress("qscale", &qscale, &b_qscale);
   fChain->SetBranchAddress("x1", &x1, &b_x1);
   fChain->SetBranchAddress("x2", &x2, &b_x2);
   fChain->SetBranchAddress("pdf1", &pdf1, &b_pdf1);
   fChain->SetBranchAddress("pdf2", &pdf2, &b_pdf2);
   fChain->SetBranchAddress("weight0", &weight0, &b_weight0);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("weightPuUp", &weightPuUp, &b_weightPuUp);
   fChain->SetBranchAddress("weightPu", &weightPu, &b_weightPu);
   fChain->SetBranchAddress("weightPuDown", &weightPuDown, &b_weightPuDown);
   fChain->SetBranchAddress("weightLumi", &weightLumi, &b_weightLumi);
   fChain->SetBranchAddress("weightAll", &weightAll, &b_weightAll);
   fChain->SetBranchAddress("interactingParton1PdgId", &interactingParton1PdgId, &b_interactingParton1PdgId);
   fChain->SetBranchAddress("interactingParton2PdgId", &interactingParton2PdgId, &b_interactingParton2PdgId);
   fChain->SetBranchAddress("pdf_id1", &pdf_id1, &b_pdf_id1);
   fChain->SetBranchAddress("pdf_id2", &pdf_id2, &b_pdf_id2);
   fChain->SetBranchAddress("npv_true ", &npv_true , &b_npv_true);
   fChain->SetBranchAddress("beamHaloIDLoose", &beamHaloIDLoose, &b_beamHaloIDLoose);
   fChain->SetBranchAddress("beamHaloIDTight", &beamHaloIDTight, &b_beamHaloIDTight);
   fChain->SetBranchAddress("beamHaloIDTight2015", &beamHaloIDTight2015, &b_beamHaloIDTight2015);
   fChain->SetBranchAddress("mgg", &mgg, &b_mgg);
   fChain->SetBranchAddress("qt", &qt, &b_qt);
   fChain->SetBranchAddress("deltaPhi", &deltaPhi, &b_deltaPhi);
   fChain->SetBranchAddress("deltaEta", &deltaEta, &b_deltaEta);
   fChain->SetBranchAddress("deltaR", &deltaR, &b_deltaR);
   fChain->SetBranchAddress("cosThetaStar", &cosThetaStar, &b_cosThetaStar);
   fChain->SetBranchAddress("cosThetaStar_old", &cosThetaStar_old, &b_cosThetaStar_old);
   fChain->SetBranchAddress("chiDiphoton", &chiDiphoton, &b_chiDiphoton);
   fChain->SetBranchAddress("isEBEB", &isEBEB, &b_isEBEB);
   fChain->SetBranchAddress("isEBEE", &isEBEE, &b_isEBEE);
   fChain->SetBranchAddress("isEEEB", &isEEEB, &b_isEEEB);
   fChain->SetBranchAddress("isEEEE", &isEEEE, &b_isEEEE);
   fChain->SetBranchAddress("mggGen", &mggGen, &b_mggGen);
   fChain->SetBranchAddress("Genqt", &Genqt, &b_Genqt);
   fChain->SetBranchAddress("GendeltaPhi", &GendeltaPhi, &b_GendeltaPhi);
   fChain->SetBranchAddress("GendeltaEta", &GendeltaEta, &b_GendeltaEta);
   fChain->SetBranchAddress("GendeltaR", &GendeltaR, &b_GendeltaR);
   fChain->SetBranchAddress("GencosThetaStar", &GencosThetaStar, &b_GencosThetaStar);
   fChain->SetBranchAddress("GencosThetaStar_old", &GencosThetaStar_old, &b_GencosThetaStar_old);
   fChain->SetBranchAddress("GenchiDiphoton", &GenchiDiphoton, &b_GenchiDiphoton);
   fChain->SetBranchAddress("GenisEBEB", &GenisEBEB, &b_GenisEBEB);
   fChain->SetBranchAddress("GenisEBEE", &GenisEBEE, &b_GenisEBEE);
   fChain->SetBranchAddress("GenisEEEB", &GenisEEEB, &b_GenisEEEB);
   fChain->SetBranchAddress("GenisEEEE", &GenisEEEE, &b_GenisEEEE);
   fChain->SetBranchAddress("eventClass", &eventClass, &b_eventClass);
   Notify();
}

Bool_t rootNtupleClass::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void rootNtupleClass::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t rootNtupleClass::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef rootNtupleClass_cxx
