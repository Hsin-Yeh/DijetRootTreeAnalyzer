from ROOT import *

bins = [1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866]

def ModifyHisto(histo):
  Nbin = histo.GetNbinsX()
  NewHisto = TH1D('','',)
  for i in range(Nbin):
    if i <1530:
       NewHisto.SetBinContent(i,0)
    else:
       NewHisto.SetBinContent(i,histo.GetBinContent(i))  
  return NewHisto

Fin = TFile('JetHT_run2017_red_cert_scan_all.root')

Fout = TFile('New.root','recreate')

for i in Fin.GetListOfKeys():
  histo = Fin.Get(i.GetName())
  NewHisto = ModifyHisto(histo)
  NewHisto.Write(i.GetName())

Fin.Close()
Fout.Close()
