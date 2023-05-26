void EE_L1_prefiring(){

    std::string reweight;
    std::string reweightString1="";
    std::string reweightString2="";

    TFile *corrFile2016 = new TFile("/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/data/EE_L1_prefiring/L1prefiring_photonpt_2016BtoH.root");
    TH2D *corrHist2016 = (TH2D*)corrFile2016->Get("L1prefiring_photonpt_2016BtoH");
    TFile *corrFile2017 = new TFile("/afs/cern.ch/work/h/hsinyeh/public/diphoton-analysis/CMSSW_10_2_13/src/diphoton-analysis/CMSDIJET/DijetRootTreeAnalyzer/data/EE_L1_prefiring/L1prefiring_photonpt_2017BtoF.root");
    TH2D *corrHist2017 = (TH2D*)corrFile2017->Get("L1prefiring_photonpt_2017BtoF");

    int count = 0;
    // int Nbins = (corrHist2016->GetNbinsX()+2)*(corrHist2016->GetNbinsY()+2);
    int Nbins = 340;
    for(int ibin=0; ibin<Nbins; ibin++){
        double weight = 1 - corrHist2016->GetBinContent(ibin); // The content is prefire rate. The weight is non-prefiring probability
        double weightError = -corrHist2016->GetBinError(ibin); // minus sign to give the correct non-prefiring probability uncertainty
        if (weight == 1) continue;
        count++;
        int xbin,ybin,zbin;
        corrHist2016->GetBinXYZ(ibin,xbin,ybin,zbin);
        double etaLow = corrHist2016->GetXaxis()->GetBinLowEdge(xbin);
        double etaUp = corrHist2016->GetXaxis()->GetBinUpEdge(xbin);
        double ptLow = corrHist2016->GetYaxis()->GetBinLowEdge(ybin);
        double ptUp = corrHist2016->GetYaxis()->GetBinUpEdge(ybin);
        std::cout << ibin << " " << xbin << " " << ybin << std::endl;
        std::cout << Form("(ph1pt>=%f && ph1pt<%f && ph1scEta>=%f && ph1scEta<%f)*(%f + %f*%d)",ptLow, ptUp, etaLow, etaUp, weight, weightError, 0) << std::endl;
        reweightString1 += Form("(ph1pt>=%f && ph1pt<%f && ph1scEta>=%f && ph1scEta<%f)*(%f + %f*%d)",ptLow, ptUp, etaLow, etaUp, weight, weightError, 0);
        reweightString2 += Form("(ph2pt>=%f && ph2pt<%f && ph2scEta>=%f && ph2scEta<%f)*(%f + %f*%d)",ptLow, ptUp, etaLow, etaUp, weight, weightError, 0);
        if (ibin != Nbins-1){
            reweightString1 += "+";
            reweightString2 += "+";
        }
    }
    reweightString1.pop_back();
    reweightString2.pop_back();
    reweight = "(" + reweightString1 + ")*(" + reweightString2 + ")";
    std::cout << reweight << std::endl;
    std::cout <<count <<std::endl;


    reweight="";
    reweightString1="";
    reweightString2="";
    count = 0;
    for(int ibin=0; ibin<Nbins; ibin++){
        double weight = 1 - corrHist2017->GetBinContent(ibin); // The content is prefire rate. The weight is non-prefiring probability
        double weightError = -corrHist2017->GetBinError(ibin); // minus sign to give the correct non-prefiring probability uncertainty
        if (weight == 1) continue;
        count++;
        int xbin,ybin,zbin;
        corrHist2017->GetBinXYZ(ibin,xbin,ybin,zbin);
        double etaLow = corrHist2017->GetXaxis()->GetBinLowEdge(xbin);
        double etaUp = corrHist2017->GetXaxis()->GetBinUpEdge(xbin);
        double ptLow = corrHist2017->GetYaxis()->GetBinLowEdge(ybin);
        double ptUp = corrHist2017->GetYaxis()->GetBinUpEdge(ybin);
        std::cout << ibin << " " << xbin << " " << ybin << std::endl;
        std::cout << Form("(ph1pt>=%f && ph1pt<%f && ph1scEta>=%f && ph1scEta<%f)*(%f + %f*%d)",ptLow, ptUp, etaLow, etaUp, weight, weightError, 0) << std::endl;
        reweightString1 += Form("(ph1pt>=%f && ph1pt<%f && ph1scEta>=%f && ph1scEta<%f)*(%f + %f*%d)",ptLow, ptUp, etaLow, etaUp, weight, weightError, 0);
        reweightString2 += Form("(ph2pt>=%f && ph2pt<%f && ph2scEta>=%f && ph2scEta<%f)*(%f + %f*%d)",ptLow, ptUp, etaLow, etaUp, weight, weightError, 0);
        if (ibin != Nbins-1){
            reweightString1 += "+";
            reweightString2 += "+";
        }
    }
    reweightString1.pop_back();
    reweightString2.pop_back();
    reweight = "(" + reweightString1 + ")*(" + reweightString2 + ")";
    std::cout << reweight << std::endl;
    std::cout <<count <<std::endl;

}
