#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <map>

//ROOT
#include "TCanvas.h"
#include "TString.h"
#include "TH1.h"
#include "TFile.h"
#include "TLegend.h"
#include "TGraphErrors.h"
#include "TPaveText.h"
#include "TStyle.h"
#include "TGraphAsymmErrors.h"
#include "TLatex.h"
#include "TF1.h"

//-----------------------------------------------------------------------------------
struct xsec{

  std::string name;
  double coup;
  std::string M_bins;
  double val;
  double error ;

};

//-----------------------------------------------------------------------------------
void plotLimit(string year, string signame, string coupling, bool unblind) {
  string inputfileName = "finalResults_" + year + "_" + signame + "_" + coupling;

  TStyle* m_gStyle = new TStyle();
  m_gStyle->SetOptFit(0);
  gSystem->Exec(Form("wc -l %s | awk '{print $1}' > pptt", inputfileName.c_str() )); // wc -l Prints the number of lines in a file --> count how many mass points; awk simply cuts the unnecessary part of the wc -l outcome;
  std::ifstream numPoin("pptt");
  int NumPunkte = 0;//221;
  numPoin >> NumPunkte;
  std::cout<< NumPunkte << std::endl;
  std::vector<double> mass, obs, exp, expP1s, expP2s, expM1s, expM2s;
  std::vector<double> exp_diff;
  mass.resize(NumPunkte);
  obs.resize(NumPunkte);
  exp.resize(NumPunkte);
  expP1s.resize(NumPunkte);
  expP2s.resize(NumPunkte);
  expM1s.resize(NumPunkte);
  expM2s.resize(NumPunkte);
  exp_diff.resize(NumPunkte);

  std::ifstream inputfile(inputfileName);

  TGraphErrors* expGraph_init = new TGraphErrors();
  TGraphErrors* expGraph_init_diff = new TGraphErrors();
  TGraphErrors* exp1SGraph_init = new TGraphErrors();
  TGraphErrors* exp2SGraph_init = new TGraphErrors();
  TGraphErrors* obsGraph_init = new TGraphErrors();

  TGraphAsymmErrors * graphmede = new TGraphAsymmErrors();
  TGraphAsymmErrors * graph68up = new TGraphAsymmErrors();
  TGraphAsymmErrors * graph68dn = new TGraphAsymmErrors();
  TGraphAsymmErrors * graph95up = new TGraphAsymmErrors();
  TGraphAsymmErrors * graph95dn = new TGraphAsymmErrors();

  bool use_fb = true;

  bool missmatchFlag = false;
  int point = 0;
  for( int i = 0 ; i < NumPunkte ; ++i ) {
    inputfile >> mass[i] >> obs[i] >> expM2s[i] >> expM1s[i] >> exp[i] >> expP1s[i] >> expP2s[i];
    std::cout << mass[i]<< " " << obs[i]<< " " << expM2s[i]<< " " << expM1s[i]<< " " << exp[i]<< " " << expP1s[i]<< " " << expP2s[i]<<std::endl;

    expGraph_init->SetPoint(i,mass[i],exp[i]);
    expGraph_init_diff->SetPoint(i,mass[i],exp_diff[i]);
    obsGraph_init->SetPoint(i,mass[i],obs[i]);
    exp1SGraph_init->SetPoint(i,mass[i],expM1s[i]);
    exp2SGraph_init->SetPoint(i,mass[i],expM2s[i]);

    graphmede->SetPoint(i,mass[i],exp[i]);
    graph68up->SetPoint(i,mass[i],expP1s[i]);
    graph68dn->SetPoint(i,mass[i],expM1s[i]);
    graph95up->SetPoint(i,mass[i],expP2s[i]);
    graph95dn->SetPoint(i,mass[i],expM2s[i]);
    point++;
  }

  TCanvas *c1 = new TCanvas();
  expGraph_init->Draw("AP");
  c1->Update();
  c1->SaveAs("test.png");
  // TGraph* expGraph = new TGraph(mass.size(), &mass[0], &exp);
  // TGraph* obsGraph = new TGraph(mass.size(), &mass[0],&obs);
  // TGraph* exp1SGraph = new TGraph(mass.size(), &mass[0],&expM1s);
  // TGraph* exp2SGraph = new TGraph(mass.size(), &mass[0],&expM2s);

  for( int i = 0 ; i < point ; ++i ) {
    exp1SGraph_init->SetPoint(point+i,mass[point-1-i],expP1s[point-1-i]);
    exp2SGraph_init->SetPoint(point+i,mass[point-1-i],expP2s[point-1-i]);
  }

  TGraph* expGraph = (TGraph*) expGraph_init->Clone();
  TGraph* expGraph_diff = (TGraph*) expGraph_init_diff->Clone();
  TGraph* exp1SGraph = (TGraph*) exp1SGraph_init->Clone();
  TGraph* exp2SGraph = (TGraph*) exp2SGraph_init->Clone();
  TGraph* obsGraph = (TGraph*) obsGraph_init->Clone();

  //smooth
  TString fitstring = "[0] + [1]*x*x + [2]*x*x*x +[3]*x*x*x*x + [4]*x";
  TF1 *medfunc  = new TF1("medfunc" , fitstring, 500., 8000.);
  TF1 *up68func = new TF1("up68func", fitstring, 500., 8000.);
  TF1 *dn68func = new TF1("dn68func", fitstring, 500., 8000.);
  TF1 *up95func = new TF1("up95func", fitstring, 500., 8000.);
  TF1 *dn95func = new TF1("dn95func", fitstring, 500., 8000.);

  // expGraph->Fit(medfunc,"R,M,EX0","Q");

  graphmede->Fit(medfunc,"R,M,EX0","Q");
  graph68up->Fit(up68func,"R,M,EX0","Q");
  graph68dn->Fit(dn68func,"R,M,EX0","Q");
  graph95up->Fit(up95func,"R,M,EX0","Q");
  graph95dn->Fit(dn95func,"R,M,EX0","Q");

  TCanvas *canv = new TCanvas("canv","Title",800,600);
  canv->SetLogy();
  canv->SetLogx();
  canv->SetRightMargin(0.08);
  canv->SetLeftMargin(0.15);

  exp1SGraph->SetFillColor(kGreen);
  exp2SGraph->SetFillColor(kYellow);
  exp2SGraph->GetXaxis()->SetTitleSize(0.045);
  exp2SGraph->GetYaxis()->SetTitleSize(0.045);

  // exp2SGraph->GetYaxis()->SetRangeUser(0.0001,30);
  exp2SGraph->GetYaxis()->SetRangeUser(0.005,20);
  exp2SGraph->GetYaxis()->SetTitle(signame == "grav" ?  "95% CL limit #sigma(pp#rightarrowG#rightarrow#gamma#gamma) (fb)" : "95% CL limit #sigma(pp#rightarrowS#rightarrow#gamma#gamma) (fb)" );
  exp2SGraph->GetXaxis()->SetTitle(signame == "grav" ? "m_{G} (GeV)" : "m_{S} (GeV)");
  exp2SGraph->GetXaxis()->SetMoreLogLabels();
  exp2SGraph->GetXaxis()->SetRangeUser(600,8000);

  exp2SGraph->Draw("AF");
  exp1SGraph->Draw("F");
  expGraph->SetLineColor(kBlue);
  expGraph->SetLineStyle(7);
  expGraph->SetLineWidth(3);
  // expGraph->Smooth();
  expGraph->Draw("CL");

  obsGraph->SetMarkerColor(1);
  obsGraph->SetMarkerStyle(20);
  obsGraph->SetMarkerSize(0.5);
  obsGraph->SetLineWidth(2);
  obsGraph->SetLineColor(kBlack);
  obsGraph->SetLineStyle(1);
  // obsGraph->Smooth();
  if (unblind) obsGraph->Draw("PL");
  // if (unblind) obsGraph->Draw("L");
  // obsGraph->Draw("LC");

  // graphmede->Draw("same");

  // theoryGraph->SetLineWidth(3);
  // theoryGraph->SetLineColor(kRed);
  // theoryGraph->SetLineStyle(4);
  // theoryGraph->Draw("PL");

  // fm[coupling]->SetLineWidth(3);
  // fm[coupling]->SetLineColor(kRed);
  // fm[coupling]->SetLineStyle(4);
  // fm[coupling]->Draw("same");

  // grxs_spline[coupling]->SetLineWidth(3);
  // grxs_spline[coupling]->SetLineColor(kRed);
  // grxs_spline[coupling]->SetLineStyle(4);
  // grxs_spline[coupling]->Draw("same");

  // grxs[coupling]->SetLineWidth(3);
  // grxs[coupling]->SetLineColor(kRed);
  // grxs[coupling]->SetLineStyle(9);
  // grxs[coupling]->SetMarkerStyle(20);
  // grxs[coupling]->Draw("Lsame");
  // fm[coupling]->SetLineColor(kBlue);
  // fm[coupling]->SetLineStyle(9);
  // fm[coupling]->Draw("same");

  // obsCMSGraph->SetMarkerColor(kViolet);
  // obsCMSGraph->SetMarkerStyle(20);
  // obsCMSGraph->SetMarkerSize(1);
  // obsCMSGraph->SetLineWidth(2);
  // obsCMSGraph->SetLineColor(kViolet);
  // obsCMSGraph->SetLineStyle(1);
  //obsCMSGraph->Draw("PL");

  auto gr_2016  = new TGraph();
  if (coupling=="kMpl001") gr_2016->SetPoint(0,2300, 0.125977);
  if (coupling=="kMpl01") gr_2016->SetPoint(0,4100, 0.0983398);
  if (coupling=="kMpl02") gr_2016->SetPoint(0,4700, 0.1014);
  gr_2016->SetMarkerStyle(30);
  gr_2016->SetMarkerSize(4);
  gr_2016->SetMarkerColor(9);
  gr_2016->Draw("Psame");

  TLegend *leg = new TLegend(0.55,0.6,0.75,0.85,NULL,"brNDC");
  leg->SetBorderSize(1);
  leg->SetTextFont(62);
  leg->SetLineColor(0);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(1001);
  leg->SetTextSize(0.033);
  // leg->AddEntry(theoryGraph,"Theory NNLO","L");

  std::string plabel;
  if ( coupling == "kMpl001" ){ plabel = "#tilde{k}=0.01,J=2"; }
  else if ( coupling == "kMpl01" ){ plabel = "#tilde{k}=0.1,J=2";}
  else if ( coupling == "kMpl02" ){ plabel = "#tilde{k}=0.2,J=2";}
  else if ( coupling == "0p014"){ plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-4},J=0"; }
  else if ( coupling == "1p4"){ plabel = "#frac{#Gamma}{m} = 1.4 #times 10^{-2},J=0"; }
  else if ( coupling == "5p6"){ plabel = "#frac{#Gamma}{m} = 5.6 #times 10^{-2},J=0"; }
  else {
    std::cout << "Only 'kMpl001', 'kMpl01', 'kMpl02', '0p014', '1p4' and '5p6' are allowed. " << std::endl;
    exit(1);
  }

  leg->SetHeader(plabel.c_str(),"C");
  if ( signame == "grav" ) {
    // leg->AddEntry(grxs[coupling],"G_{RS}#rightarrow#gamma#gamma (LO)","l");
    leg->AddEntry(gr_2016,"Published 2016 Mass Limit","P");
  }
  leg->AddEntry(expGraph,"expected Limit","L"); //L_{int}=36.4/pb
  leg->AddEntry(exp1SGraph,"#pm1#sigma","F");
  leg->AddEntry(exp2SGraph,"#pm2#sigma","F");
  // leg->AddEntry(obsGraph,"observed Limit (Asymptotic)","L");
  leg->Draw();

  TLatex* cmsText=new TLatex(0.17,0.90, "CMS");
  cmsText->SetNDC(kTRUE);
  cmsText->SetTextFont(61);
  cmsText->SetLineColor(0);
  cmsText->SetLineStyle(1);
  cmsText->SetLineWidth(1);
  cmsText->SetTextSize(0.035);
  cmsText->Draw();

  TLatex* extraText=new TLatex(0.23,0.90, "Preliminary");
  extraText->SetNDC(kTRUE);
  extraText->SetTextFont(52);
  extraText->SetLineColor(0);
  extraText->SetLineStyle(1);
  extraText->SetLineWidth(1);
  extraText->SetTextSize(0.035);
  extraText->Draw();

  std::map<std::string, int> thelumi;
  thelumi["2016"]=35.9;
  thelumi["2017"]=41.5;
  thelumi["2018"]=59.7;
  thelumi["fullRun2"]=137.1;
  TLatex* lumiText=new TLatex(0.70,0.90, Form("%d fb^{-1} (13 TeV)", thelumi[year] ) );
  lumiText->SetNDC(kTRUE);
  lumiText->SetTextFont(42);
  lumiText->SetLineColor(0);
  lumiText->SetLineStyle(1);
  lumiText->SetLineWidth(1);
  lumiText->SetTextSize(0.035);
  lumiText->Draw();

  canv->SaveAs( Form("./limitplot_%s_%s_%s.png", signame.c_str(), coupling.c_str(), year.c_str()) );

  TFile *outfile = new TFile( Form("./limitplot_%s_%s_%s.root", signame.c_str(), coupling.c_str(), year.c_str()) , "RECREATE");
  canv->Write();
  expGraph->SetName("expGraph");
  obsGraph->SetName("obsGraph");
  exp1SGraph->SetName("exp1SGraph");
  exp2SGraph->SetName("exp2SGraph");
  // grxs[coupling]->SetName("theory");
  expGraph->Write();
  obsGraph->Write();
  exp1SGraph->Write();
  exp2SGraph->Write();
  // grxs[coupling]->Write();

  outfile->Write();
  outfile->Close();

}

/* float cross_sections(){ */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-1000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.01208; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-1250_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.003731; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-1750_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.0005499; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-2000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.0002422; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-2250_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.0001135; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-2500_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.604e-05; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-2750_TuneCUEP8M1_13TeV-pythia8")) xsec = 2.859e-05; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-3000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.501e-05; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-3250_TuneCUEP8M1_13TeV-pythia8")) xsec = 8.03e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-3500_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.384e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-3750_TuneCUEP8M1_13TeV-pythia8")) xsec = 2.443e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-4000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.365e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-4500_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.371e-07; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-5000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.425e-07; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-500_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.3405; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-5500_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.675e-08; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-6000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.556e-08; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-6500_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.193e-09; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-7000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.784e-09; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-740_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.05437; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-750_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.05088; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-755_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.04915; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-760_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.04782; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-765_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.04589; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-770_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.04465; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-1000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.206; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-1250_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.3716; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-1500_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.1348; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-1750_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.0548; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-2000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.02407; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-2250_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.01129; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-2500_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.005536; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-2750_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.002836; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-3000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.001492; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-3500_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.0004361; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-4000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.0001361; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-4500_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.354e-05; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-5000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.439e-05; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-500_TuneCUEP8M1_13TeV-pythia8")) xsec = 34.43; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-5500_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.807e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-6000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.617e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-6500_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.545e-07; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-7000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.991e-07; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-740_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.392; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-745_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.192; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-750_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.092; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-755_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.886; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-760_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.741; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-765_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.585; */
/*     if(sample.Contains("RSGravToGG_kMpl-01_M-770_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.428; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-1000_TuneCUEP8M1_13TeV-pythia8")) xsec = 4.829; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-1500_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.5326; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-2000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.09455; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-3000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.005803; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-4000_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.000536; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-5000_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.879e-05; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-500_TuneCUEP8M1_13TeV-pythia8")) xsec = 142.6; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-6000_TuneCUEP8M1_13TeV-pythia8")) xsec = 7.185e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-7000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.03e-06; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-740_TuneCUEP8M1_13TeV-pythia8")) xsec = 21.32; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-745_TuneCUEP8M1_13TeV-pythia8")) xsec = 20.55; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-750_TuneCUEP8M1_13TeV-pythia8")) xsec = 20.62; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-755_TuneCUEP8M1_13TeV-pythia8")) xsec = 19.33; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-760_TuneCUEP8M1_13TeV-pythia8")) xsec = 18.74; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-765_TuneCUEP8M1_13TeV-pythia8")) xsec = 18.18; */
/*     if(sample.Contains("RSGravToGG_kMpl-02_M-770_TuneCUEP8M1_13TeV-pythia8")) xsec = 17.58; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-1500_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.001357; */
/*     if(sample.Contains("RSGravToGG_kMpl-001_M-745_TuneCUEP8M1_13TeV-pythia8")) xsec = 0.05274; */
/*     // from XSDB (2016) */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-1000_TuneCUEP8M1_13TeV-pythia8")) xsec = 6.917e-12; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-1250_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.389e-12; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-1500_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.157e-13; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-1750_TuneCUEP8M1_13TeV-pythia8")) xsec = 8.162e-14; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-2000_TuneCUEP8M1_13TeV-pythia8")) xsec = 2.358e-14; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-2250_TuneCUEP8M1_13TeV-pythia8")) xsec = 7.401e-15; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-2500_TuneCUEP8M1_13TeV-pythia8")) xsec = 2.514e-15; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-2750_TuneCUEP8M1_13TeV-pythia8")) xsec = 9.032e-16; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-3000_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.401e-16; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-3250_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.324e-16; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-3500_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.448e-17; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-4000_TuneCUEP8M1_13TeV-pythia8")) xsec = 9.839e-18; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-4500_TuneCUEP8M1_13TeV-pythia8")) xsec = 2.027e-18; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-5000_TuneCUEP8M1_13TeV-pythia8")) xsec = 5.081e-19; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-0p014_M-750_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.301e-11; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-1000_TuneCUEP8M1_13TeV-pythia8")) xsec = 7.08e-10; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-1500_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.435e-11; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-2000_TuneCUEP8M1_13TeV-pythia8")) xsec = 2.88e-12; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-3000_TuneCUEP8M1_13TeV-pythia8")) xsec = 7.852e-14; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-4000_TuneCUEP8M1_13TeV-pythia8")) xsec = 8.495e-15; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-5000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.959e-15; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-1p4_M-750_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.318e-09; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-1000_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.045e-09; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-1500_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.713e-10; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-2000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.79e-11; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-3000_TuneCUEP8M1_13TeV-pythia8")) xsec = 8.497e-13; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-4000_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.252e-13; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-5000_TuneCUEP8M1_13TeV-pythia8")) xsec = 3.107e-14; */
/*     if(sample.Contains("GluGluSpin0ToGG_W-5p6_M-750_TuneCUEP8M1_13TeV-pythia8")) xsec = 1.353e-08; */
/*     // From running GenXsecAnalyzer on full sample (2017) */
/*     // We will use 2017 cross section for all three years */
/*     // The ntuples are generated with 2017 xsection weights */
/*     // In the resonant samplelist.hh, prepare all three years with the same naming scheme as below */
/*     // except adding "_{year}" at the bottom */

/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_750_TuneCP2_13TeV_pythia8")) xsec =  3.035e-11; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_1000_TuneCP2_13TeV_pythia8")) xsec =  5.945e-12; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_1250_TuneCP2_13TeV_pythia8")) xsec =  1.132e-12; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_1500_TuneCP2_13TeV_pythia8")) xsec =  2.432e-13; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_1750_TuneCP2_13TeV_pythia8")) xsec = 5.951e-14; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_2000_TuneCP2_13TeV_pythia8")) xsec = 1.624e-14; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_2250_TuneCP2_13TeV_pythia8")) xsec =  4.882e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_2500_TuneCP2_13TeV_pythia8")) xsec =  1.574e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_2750_TuneCP2_13TeV_pythia8")) xsec = 5.413e-16; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_3000_TuneCP2_13TeV_pythia8")) xsec =  1.962e-16; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_3250_TuneCP2_13TeV_pythia8")) xsec = 7.432e-17; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_3500_TuneCP2_13TeV_pythia8")) xsec =  2.933e-17; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_4000_TuneCP2_13TeV_pythia8")) xsec =  5.239e-18; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_4500_TuneCP2_13TeV_pythia8")) xsec = 1.143e-18; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_0p014_M_5000_TuneCP2_13TeV_pythia8")) xsec =  3.283e-19; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_750_TuneCP2_13TeV_pythia8")) xsec =  3.042e-09; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_1000_TuneCP2_13TeV_pythia8")) xsec =  6.140e-10; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_1250_TuneCP2_13TeV_pythia8")) xsec = 1.202e-10; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_1500_TuneCP2_13TeV_pythia8")) xsec =  2.704e-11; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_1750_TuneCP2_13TeV_pythia8")) xsec =  7.066e-12; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_2000_TuneCP2_13TeV_pythia8")) xsec =  2.120e-12; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_2250_TuneCP2_13TeV_pythia8")) xsec =  7.305e-13; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_2500_TuneCP2_13TeV_pythia8")) xsec =  2.835e-13; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_3000_TuneCP2_13TeV_pythia8")) xsec =  6.077e-14; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_3500_TuneCP2_13TeV_pythia8")) xsec = 1.874e-14; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_4000_TuneCP2_13TeV_pythia8")) xsec =  7.510e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_4250_TuneCP2_13TeV_pythia8")) xsec = 5.052e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_4500_TuneCP2_13TeV_pythia8")) xsec = 3.501e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_4750_TuneCP2_13TeV_pythia8")) xsec =  2.501e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_1p4_M_5000_TuneCP2_13TeV_pythia8")) xsec = 1.816e-15; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_750_TuneCP2_13TeV_pythia8")) xsec =  1.247e-08; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_1000_TuneCP2_13TeV_pythia8")) xsec =  2.681e-09; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_1250_TuneCP2_13TeV_pythia8")) xsec =  5.652e-10; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_1500_TuneCP2_13TeV_pythia8")) xsec =  1.406e-10; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_1750_TuneCP2_13TeV_pythia8")) xsec =  4.166e-11; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_2000_TuneCP2_13TeV_pythia8")) xsec =  1.451e-11; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_2250_TuneCP2_13TeV_pythia8")) xsec =  5.826e-12; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_2500_TuneCP2_13TeV_pythia8")) xsec =  2.652e-12; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_3000_TuneCP2_13TeV_pythia8")) xsec =  7.361e-13; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_3500_TuneCP2_13TeV_pythia8")) xsec =  2.657e-13; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_4000_TuneCP2_13TeV_pythia8")) xsec =  1.144e-13; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_4500_TuneCP2_13TeV_pythia8")) xsec =  5.519e-14; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_4750_TuneCP2_13TeV_pythia8")) xsec =  3.954e-14; */
/*     if(sample.Contains("GluGluSpin0ToGammaGamma_W_5p6_M_5000_TuneCP2_13TeV_pythia8")) xsec =  2.890e-14; */


/*     int masslist[] = (750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 4000, 5000); */
/*     int masslist[] = (4.850e-02, 1.133e-02, 3.428e-03, 1.234e-03, 4.981e-04, 2.201e-04, 1.036e-04, 5.074e-05, 2.613e-05, 1.384e-05, 7.548e-06, 4.226e-06, 1.439e-06, 2.150e-07); */
/*  [750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6500, 7000, 8000]; */
/*  [4.870e+00, 1.120e+00, 3.413e-01, 1.224e-01, 4.940e-02, 2.180e-02, 1.025e-02, 5.051e-03, 1.373e-03, 4.229e-04, 1.435e-04, 8.663e-05, 5.367e-05, 3.368e-05, 2.163e-05, 1.398e-05, 9.145e-06, 6.022e-06, 3.967e-06, 1.742e-06, 7.583e-07, 1.269e-07]; */
/*  [750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 3500, 4000, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6500, 7000, 8000]; */
/*  [1.905e+01, 4.403e+00, 1.328e+00, 4.750e-01, 1.919e-01, 8.481e-02, 3.981e-02, 1.967e-02, 5.410e-03, 1.669e-03, 5.707e-04, 2.157e-04, 1.364e-04, 8.732e-05, 5.709e-05, 3.748e-05, 2.479e-05, 1.652e-05, 7.426e-06, 3.360e-06, 6.570e-07]; */




/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_750 _TuneCP2_13TeV_pythia8")) xsec =  4.850e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_1000_TuneCP2_13TeV_pythia8")) xsec =  1.133e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_1250_TuneCP2_13TeV_pythia8")) xsec =  3.428e-03; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_1500_TuneCP2_13TeV_pythia8")) xsec =  1.234e-03; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_1750_TuneCP2_13TeV_pythia8")) xsec =  4.981e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_2000_TuneCP2_13TeV_pythia8")) xsec =  2.201e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_2250_TuneCP2_13TeV_pythia8")) xsec =  1.036e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_2500_TuneCP2_13TeV_pythia8")) xsec =  5.074e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_2750_TuneCP2_13TeV_pythia8")) xsec =  2.613e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_3000_TuneCP2_13TeV_pythia8")) xsec =  1.384e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_3250_TuneCP2_13TeV_pythia8")) xsec =  7.548e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_3500_TuneCP2_13TeV_pythia8")) xsec =  4.226e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_4000_TuneCP2_13TeV_pythia8")) xsec =  1.439e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl001_M_5000_TuneCP2_13TeV_pythia8")) xsec =  2.150e-07; */

/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_750 _TuneCP2_13TeV_pythia8")) xsec =  4.870e+00; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_1000_TuneCP2_13TeV_pythia8")) xsec =  1.120e+00; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_1250_TuneCP2_13TeV_pythia8")) xsec =  3.413e-01; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_1500_TuneCP2_13TeV_pythia8")) xsec =  1.224e-01; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_1750_TuneCP2_13TeV_pythia8")) xsec =  4.940e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_2000_TuneCP2_13TeV_pythia8")) xsec =  2.180e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_2250_TuneCP2_13TeV_pythia8")) xsec =  1.025e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_2500_TuneCP2_13TeV_pythia8")) xsec =  5.051e-03; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_3000_TuneCP2_13TeV_pythia8")) xsec =  1.373e-03; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_3500_TuneCP2_13TeV_pythia8")) xsec =  4.229e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_4000_TuneCP2_13TeV_pythia8")) xsec =  1.435e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_4250_TuneCP2_13TeV_pythia8")) xsec =  8.663e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_4500_TuneCP2_13TeV_pythia8")) xsec =  5.367e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_4750_TuneCP2_13TeV_pythia8")) xsec =  3.368e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_5000_TuneCP2_13TeV_pythia8")) xsec =  2.163e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_5250_TuneCP2_13TeV_pythia8")) xsec =  1.398e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_5500_TuneCP2_13TeV_pythia8")) xsec =  9.145e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_5750_TuneCP2_13TeV_pythia8")) xsec =  6.022e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_6000_TuneCP2_13TeV_pythia8")) xsec =  3.967e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_6500_TuneCP2_13TeV_pythia8")) xsec =  1.742e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_7000_TuneCP2_13TeV_pythia8")) xsec =  7.583e-07; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl01_M_8000_TuneCP2_13TeV_pythia8")) xsec =  1.269e-07; */

/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_750 _TuneCP2_13TeV_pythia8")) xsec =  1.905e+01; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_1000_TuneCP2_13TeV_pythia8")) xsec =  4.403e+00; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_1250_TuneCP2_13TeV_pythia8")) xsec =  1.328e+00; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_1500_TuneCP2_13TeV_pythia8")) xsec =  4.750e-01; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_1750_TuneCP2_13TeV_pythia8")) xsec =  1.919e-01; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_2000_TuneCP2_13TeV_pythia8")) xsec =  8.481e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_2250_TuneCP2_13TeV_pythia8")) xsec =  3.981e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_2500_TuneCP2_13TeV_pythia8")) xsec =  1.967e-02; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_3000_TuneCP2_13TeV_pythia8")) xsec =  5.410e-03; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_3500_TuneCP2_13TeV_pythia8")) xsec =  1.669e-03; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_4000_TuneCP2_13TeV_pythia8")) xsec =  5.707e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_4500_TuneCP2_13TeV_pythia8")) xsec =  2.157e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_4750_TuneCP2_13TeV_pythia8")) xsec =  1.364e-04; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_5000_TuneCP2_13TeV_pythia8")) xsec =  8.732e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_5250_TuneCP2_13TeV_pythia8")) xsec =  5.709e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_5500_TuneCP2_13TeV_pythia8")) xsec =  3.748e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_5750_TuneCP2_13TeV_pythia8")) xsec =  2.479e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_6000_TuneCP2_13TeV_pythia8")) xsec =  1.652e-05; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_6500_TuneCP2_13TeV_pythia8")) xsec =  7.426e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_7000_TuneCP2_13TeV_pythia8")) xsec =  3.360e-06; */
/*     if(sample.Contains("RSGravitonToGammaGamma_kMpl02_M_8000_TuneCP2_13TeV_pythia8")) xsec =  6.570e-07; */
/* } */
