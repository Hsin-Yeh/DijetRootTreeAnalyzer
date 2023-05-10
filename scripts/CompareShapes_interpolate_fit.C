#include "diphoton-analysis/Tools/interface/sampleList.hh"
#include "diphoton-analysis/Tools/interface/utilities.hh"
#include "diphoton-analysis/RooUtils/interface/RooDCBShape.h"
#include <string>
#include <deque>
//RooFit
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooFitResult.h"
#include "RooStats/HLFactory.h"
#include "RooPlot.h"
#include "RooGenericPdf.h"
#include "RooFFTConvPdf.h"
#include "RooDataHist.h"
#include "RooBinning.h"
#include "RooVoigtian.h"
#include "RooExtendPdf.h"

//ROOT
#include "TCanvas.h"
#include "TString.h"
#include "TH1.h"
#include "TFile.h"
#include "TPaveText.h"
#include "TLatex.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TGraphErrors.h"

using namespace RooFit;
using namespace RooStats;

void CompareShapes_interpolate_fit(int mass){

        string year="2017";
        string ws = "../../output/" + year + "/FinalParametricShape/workspaces";
        string method = "full";
        string cat = "EBEB";
        string coup = "kMpl001";
        string outDir = "./";

        string filename = ws + "/SignalParametricShapes_ws_" + coup + ".root";
        TFile* fparamshape = new TFile(filename.c_str());
        RooWorkspace* wsparamshape = (RooWorkspace*)fparamshape->Get("ws_inputs");
        // # RooRealVar x{"x", "x", 1.0, binEdges[0], binEdges.back()};
        RooRealVar* mgg = wsparamshape->var("mgg");
        RooRealVar* MH  = wsparamshape->var("MH");
        MH->setVal(mass);
        // varbin = RooBinning(len(binBoundaries[options.coup])-1, array('d', binBoundaries[options.coup]))
        // # tbins = RooBinning(12);
        // # p = mgg.frame()
        RooPlot* p = mgg->frame(0,1000,125);
        RooAbsPdf* shape = wsparamshape->pdf(Form("SignalShape_%s_EBEB",coup.c_str()));
        shape->plotOn(p,LineColor(2),Name("Parameterization"));

        // # #Now to the interpolated shape
        TFile* tfileRes = new TFile(Form("/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/DijetShapeInterpolator/%s/ResonanceShapes_InputShapes_RSGravitonToGammaGamma_%s_%s_%s_finebinned.root",method.c_str(),coup.c_str(),cat.c_str(),year.c_str()) , "read");
        tfileRes->cd();

        TH1D* hist_mass_list_rsg = (TH1D*)tfileRes->Get(Form("h_gg_%i",mass));
        p->addTH1(hist_mass_list_rsg,"HISTsame");
        // h = RooDataHist("h","h",RooArgList(mgg),RooFit.Import(hist_mass_list_rsg)) ;
        // h.plotOn(p,RooFit.DrawOption("B"),RooFit.XErrorSize(0))

        TCanvas* canvas = new TCanvas();
        // canvas->SetFillColor(0);
        // canvas->SetBorderMode(0);
        // canvas->SetFrameFillStyle(0);
        // canvas->SetFrameBorderMode(0);
        // canvas->SetLeftMargin(0->05+ L/W );
        // canvas->SetRightMargin( R/W );
        // canvas->SetTopMargin( T/H );
        // canvas->SetBottomMargin( B/H );
        // canvas->SetTickx();
        // canvas->SetTicky();
        canvas->cd();



        TLegend* leg = new TLegend(0.65,0.45,0.95,0.6);
        leg->SetBorderSize(0);
        leg->SetLineColor(0);
        leg->SetFillColor(0);
        leg->SetFillStyle(0);
        leg->SetLineWidth(0);
        leg->SetTextFont(42);
        leg->SetTextAlign(23);

        p->SetLineColor(1);
        p->GetXaxis()->SetRangeUser(500, 800);
        p->GetXaxis()->SetTitle("DiPhoton mass [GeV]");
        p->GetYaxis()->SetTitle("Normalized yield/bin width");
        p->Draw("HIST");

        leg->AddEntry("Parameterization","Parameterization","l");
        leg->AddEntry(hist_mass_list_rsg,"Interpolated Shape","l");
        leg->Draw();

        canvas->SaveAs(Form("%s/test.png",outDir.c_str()) );
}
