#!/usr/bin/env python
import ROOT
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('in_filenames',nargs="+",help='input filenames')
args = parser.parse_args()

def project(tree, h, var, cut):
    print 'projecting var: %s, cut: %s from tree: %s into hist: %s'%(var, cut, tree.GetName(), h.GetName())
    tree.Project(h.GetName(),var,cut)

def main():
    for in_filename in args.in_filenames:
        tfileIn = ROOT.TFile.Open(in_filename)
        basename=in_filename.rsplit("/",1)[1].split("_1.root")[0]
        fTree=tfileIn.Get("diphoton/fTree")
        # h_pt125=tfileIn.Get("diphoton/h_pt125")
        # h_photonID=tfileIn.Get("diphoton/h_photonID")
        # h_eta=tfileIn.Get("diphoton/h_eta")
        h_photonID=ROOT.TH1F("h_photonID","h_photonID",1,0,2)
        h_pt125=ROOT.TH1F("h_pt125","h_pt125",1,0,2)
        h_eta=ROOT.TH1F("h_eta","h_eta",1,0,2)
        h_mass = ROOT.TH1F("h_mass","h_mass",1,0,2)
        h_deltaR = ROOT.TH1F("h_deltaR","h_deltaR",1,0,2)
        h_HLT = ROOT.TH1F("h_HLT","h_HLT",1,0,2)

        project(fTree,h_photonID,"1","isGood")
        project(fTree,h_pt125,"1","isGood*(Photon1.pt>125 && Photon2.pt>125)")
        project(fTree,h_eta,"1","isGood*(Photon1.pt>125 && Photon2.pt>125)*(Diphoton.isEBEB||Diphoton.isEBEE||Diphoton.isEEEB)")
        project(fTree,h_mass,"1","isGood*(Photon1.pt>125 && Photon2.pt>125)*(Diphoton.isEBEB||Diphoton.isEBEE||Diphoton.isEEEB)*(Diphoton.Minv > 500)")
        project(fTree,h_deltaR,"1","isGood*(Photon1.pt>125 && Photon2.pt>125)*(Diphoton.isEBEB||Diphoton.isEBEE||Diphoton.isEEEB)*(Diphoton.Minv > 500)*(Diphoton.deltaR > 0.45)")
        project(fTree,h_HLT,"1","isGood*(Photon1.pt>125 && Photon2.pt>125)*(Diphoton.isEBEB||Diphoton.isEBEE||Diphoton.isEEEB)*(Diphoton.Minv > 500)*(Diphoton.deltaR > 0.45)*(HLT_DoublePhoton70>0 || HLT_ECALHT800>0)")

        h_cutflow = ROOT.TH1F("h_cutflow",basename,6,0,6)
        h_cutflow.GetXaxis().SetBinLabel(1,"photonID")
        h_cutflow.GetXaxis().SetBinLabel(2,"pt125")
        h_cutflow.GetXaxis().SetBinLabel(3,"EBEB||EBEE")
        h_cutflow.GetXaxis().SetBinLabel(4,"M>230(330)")
        h_cutflow.GetXaxis().SetBinLabel(5,"dR>0.45")
        h_cutflow.GetXaxis().SetBinLabel(6,"HLT")
        h_cutflow.GetXaxis().SetLabelSize(0.055)

        h_cutflow.SetBinContent(1,float(h_photonID.Integral()) /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(2,float(h_pt125.Integral())    /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(3,float(h_eta.Integral())      /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(4,float(h_mass.Integral())     /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(5,float(h_deltaR.Integral())   /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(6,float(h_HLT.Integral())      /float(fTree.GetEntries()))

        with open("cutFlow.txt", "a") as f:
            f.write(basename)
            f.write(" %.3f"%((h_pt125.Integral())    /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_photonID.Integral()) /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_eta.Integral())      /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_mass.Integral())     /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_deltaR.Integral())   /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_HLT.Integral())      /float(fTree.GetEntries())))
            f.write("\n")


        ROOT.gStyle.SetOptStat(0)
        c1 = ROOT.TCanvas()
        h_cutflow.Draw("HISTtext00")
        h_cutflow.GetYaxis().SetRangeUser(0.3,1)
        h_cutflow.GetYaxis().SetTitle("Efficiency")
        c1.SaveAs("output/plots/cutFlow/cutFlow_%s.png"%(basename))
        tfileIn.Close()

def main_gen_level():
    for in_filename in args.in_filenames:
        tfileIn = ROOT.TFile.Open(in_filename)
        basename=in_filename.rsplit("/",1)[1].split("_1.root")[0]
        fTree=tfileIn.Get("diphoton/fTree")
        h_pt125=ROOT.TH1F("h_pt125","h_pt125",1,0,2)
        h_eta=ROOT.TH1F("h_eta","h_eta",1,0,2)
        h_mass = ROOT.TH1F("h_mass","h_mass",1,0,2)

        project(fTree,h_pt125,"1","(GenPhoton1.pt>125 && GenPhoton2.pt>125)")
        project(fTree,h_eta,"1","(GenPhoton1.pt>125)*(GenPhoton2.pt>125)*( (abs(GenPhoton2.eta)>1.57 && abs(GenPhoton2.eta)<2.50 && abs(GenPhoton1.eta)<1.44) || (abs(GenPhoton1.eta)>1.57 && abs(GenPhoton1.eta)<2.50 && abs(GenPhoton2.eta)<1.44) )")
        project(fTree,h_mass,"1","(GenPhoton1.pt>125)*(GenPhoton2.pt>125)*( (abs(GenPhoton2.eta)>1.57 && abs(GenPhoton2.eta)<2.50 && abs(GenPhoton1.eta)<1.44) || (abs(GenPhoton1.eta)>1.57 && abs(GenPhoton1.eta)<2.50 && abs(GenPhoton2.eta)<1.44) )*(GenDiphoton.Minv>500)")

        h_cutflow = ROOT.TH1F("h_cutflow",basename,3,0,3)
        h_cutflow.GetXaxis().SetBinLabel(1,"pt125")
        h_cutflow.GetXaxis().SetBinLabel(2,"EBEB||EBEE")
        h_cutflow.GetXaxis().SetBinLabel(3,"M>230(330)")
        h_cutflow.GetXaxis().SetLabelSize(0.055)

        h_cutflow.SetBinContent(1,float(h_pt125.Integral())    /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(2,float(h_eta.Integral())      /float(fTree.GetEntries()))
        h_cutflow.SetBinContent(3,float(h_mass.Integral())     /float(fTree.GetEntries()))

        with open("cutFlow.txt", "a") as f:
            f.write(basename)
            f.write(" %.3f"%((h_pt125.Integral()) /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_eta.Integral())      /float(fTree.GetEntries())))
            f.write(" %.3f"%((h_mass.Integral())     /float(fTree.GetEntries())))
            f.write("\n")


        ROOT.gStyle.SetOptStat(0)
        c1 = ROOT.TCanvas()
        h_cutflow.Draw("HISTtext00")
        h_cutflow.GetYaxis().SetRangeUser(0.3,1)
        h_cutflow.GetYaxis().SetTitle("Efficiency")
        c1.SaveAs("output/plots/cutFlow/cutFlow_%s_gen_level.png"%(basename))
        tfileIn.Close()

if __name__ == "__main__":
    # main()
    main_gen_level()
